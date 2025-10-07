from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import DailyTrivia, TriviaQuestion, TriviaGameSession, TriviaAnswer, UserTriviaStats


class TriviaQuestionInline(admin.TabularInline):
    model = TriviaQuestion
    extra = 1
    fields = ['order', 'question_text', 'question_type', 'difficulty', 'correct_answer']


@admin.register(DailyTrivia)
class DailyTriviaAdmin(admin.ModelAdmin):
    list_display = ['date', 'theme', 'is_active', 'question_count', 'session_count', 'created_at']
    list_filter = ['is_active', 'date']
    search_fields = ['theme', 'description']
    inlines = [TriviaQuestionInline]
    date_hierarchy = 'date'
    actions = ['regenerate_questions', 'reset_all_sessions']

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

    def session_count(self, obj):
        count = obj.sessions.count()
        if count > 0:
            return format_html('<span style="color: orange;">{} sessions</span>', count)
        return count
    session_count.short_description = 'Sessions'

    def regenerate_questions(self, request, queryset):
        """Regenerate questions for selected trivia dates (DESTRUCTIVE!)"""
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can regenerate trivia.", level=messages.ERROR)
            return

        from datetime import date

        for trivia in queryset:
            # Count existing sessions
            session_count = trivia.sessions.count()

            if session_count > 0:
                self.message_user(
                    request,
                    f"⚠️ Cannot regenerate {trivia.date} - {session_count} users have already played! "
                    f"Use 'Reset all sessions' first if you really want to override.",
                    level=messages.WARNING
                )
                continue

            # Delete existing questions
            trivia.questions.all().delete()

            # Try to generate new questions with Claude
            try:
                from .claude_service import ClaudeTriviaGenerator
                generator = ClaudeTriviaGenerator()
                trivia_data = generator.generate_daily_trivia(trivia.date)

                # Update theme and description
                trivia.theme = trivia_data['theme']
                trivia.description = trivia_data['description']
                trivia.save()

                # Create new questions
                for q_data in trivia_data['questions']:
                    generator.validate_question_structure(q_data)

                    options_json = None
                    if q_data['question_type'] == 'multiple_choice':
                        options_json = q_data['options']

                    TriviaQuestion.objects.create(
                        daily_trivia=trivia,
                        order=q_data['order'],
                        question_text=q_data['question_text'],
                        question_type=q_data['question_type'],
                        difficulty=q_data['difficulty'],
                        options=options_json,
                        correct_answer=q_data['correct_answer'],
                        explanation=q_data['explanation']
                    )

                self.message_user(
                    request,
                    f"✅ Successfully regenerated {trivia.date} with Claude AI: {trivia.theme} ({trivia.questions.count()} questions)",
                    level=messages.SUCCESS
                )

            except Exception as e:
                self.message_user(
                    request,
                    f"❌ Error regenerating {trivia.date} with Claude: {str(e)}. Questions were deleted but not replaced!",
                    level=messages.ERROR
                )

    regenerate_questions.short_description = "🔄 Regenerate questions with Claude AI (if no sessions)"

    def reset_all_sessions(self, request, queryset):
        """Reset all game sessions for selected trivia (DESTRUCTIVE!)"""
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can reset sessions.", level=messages.ERROR)
            return

        total_sessions = 0
        total_answers = 0

        for trivia in queryset:
            sessions = trivia.sessions.all()
            session_count = sessions.count()

            # Delete all answers for these sessions
            for session in sessions:
                answer_count = session.answers.count()
                session.answers.all().delete()
                total_answers += answer_count

            # Delete all sessions
            sessions.delete()
            total_sessions += session_count

            self.message_user(
                request,
                f"⚠️ Reset {trivia.date}: Deleted {session_count} sessions and their answers",
                level=messages.WARNING
            )

        self.message_user(
            request,
            f"🗑️ Total: Deleted {total_sessions} sessions and {total_answers} answers. Users can now replay!",
            level=messages.SUCCESS
        )

    reset_all_sessions.short_description = "🗑️ Reset all sessions (allow replays) - DESTRUCTIVE!"


@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ['daily_trivia', 'order', 'question_text_short', 'question_type', 'difficulty', 'max_points']
    list_filter = ['question_type', 'difficulty', 'daily_trivia__date']
    search_fields = ['question_text', 'correct_answer']
    ordering = ['daily_trivia', 'order']

    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(TriviaGameSession)
class TriviaGameSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_trivia', 'status', 'score', 'final_score', 'time_taken_seconds', 'completed_at']
    list_filter = ['status', 'daily_trivia__date']
    search_fields = ['user__username']
    readonly_fields = ['started_at', 'completed_at', 'final_score']
    date_hierarchy = 'started_at'


@admin.register(TriviaAnswer)
class TriviaAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'is_correct', 'points_earned', 'time_taken_seconds', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['session__user__username', 'question__question_text']
    readonly_fields = ['answered_at']


@admin.register(UserTriviaStats)
class UserTriviaStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_games_played', 'available_points', 'current_streak', 'first_place_finishes', 'perfect_games']
    list_filter = ['last_played_date']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    ordering = ['-available_points']
