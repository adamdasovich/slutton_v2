'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import { useAuthStore } from '@/store/authStore';
import api from '@/lib/api';

interface Question {
  id: number;
  question_text: string;
  question_type: string;
  difficulty: string;
  options?: { [key: string]: string };
  option_a?: string;
  option_b?: string;
  option_c?: string;
  option_d?: string;
  order: number;
  max_points: number;
}

interface TriviaData {
  id: number;
  date: string;
  theme: string;
  description: string;
  questions: Question[];
}

interface LeaderboardEntry {
  rank: number;
  username: string;
  final_score: number;
  time_taken_seconds: number;
}

export default function TriviaPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [gameState, setGameState] = useState<'loading' | 'start' | 'playing' | 'results'>('loading');
  const [triviaData, setTriviaData] = useState<TriviaData | null>(null);
  const [hasPlayed, setHasPlayed] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [score, setScore] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(300); // 5 minutes
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());
  const [results, setResults] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [answerFeedback, setAnswerFeedback] = useState<{show: boolean; correct: boolean; explanation: string} | null>(null);
  const [showQuestionAnimation, setShowQuestionAnimation] = useState(false);

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const gameStartTime = useRef<number>(0);

  // Audio refs for sound effects
  const questionRevealSoundRef = useRef<HTMLAudioElement | null>(null);
  const correctSoundRef = useRef<HTMLAudioElement | null>(null);
  const incorrectSoundRef = useRef<HTMLAudioElement | null>(null);
  const completionSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchTodayTrivia();
    fetchLeaderboard();
    initializeSounds();
  }, [isAuthenticated]);

  // Trigger animation when question changes
  useEffect(() => {
    if (gameState === 'playing') {
      setShowQuestionAnimation(true);
      playQuestionRevealSound();
      setTimeout(() => setShowQuestionAnimation(false), 800);
    }
  }, [currentQuestionIndex, gameState]);

  useEffect(() => {
    if (gameState === 'playing' && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            handleTimeUp();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [gameState, timeRemaining]);

  const fetchTodayTrivia = async () => {
    try {
      const response = await api.get('/trivia/today/');
      setTriviaData(response.data.trivia);
      setHasPlayed(response.data.has_played);
      setGameState(response.data.has_played ? 'results' : 'start');

      if (response.data.has_played) {
        // Fetch their results
        fetchLeaderboard();
      }
    } catch (error) {
      console.error('Error fetching trivia:', error);
      setGameState('start');
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const response = await api.get('/trivia/leaderboard/');
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  const initializeSounds = () => {
    // Initialize Web Audio API with sensual sound effects
    if (typeof window !== 'undefined') {
      questionRevealSoundRef.current = new Audio();
      correctSoundRef.current = new Audio();
      incorrectSoundRef.current = new Audio();
      completionSoundRef.current = new Audio();
    }
  };

  const playQuestionRevealSound = () => {
    // Play a sultry "whoosh" or "shimmer" sound
    if (questionRevealSoundRef.current) {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.5);

      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.5);
    }
  };

  const playCorrectSound = () => {
    // Play a sensual "success" chime
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator1 = audioContext.createOscillator();
    const oscillator2 = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator1.connect(gainNode);
    oscillator2.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator1.frequency.value = 523.25; // C5
    oscillator2.frequency.value = 659.25; // E5

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.8);

    oscillator1.start(audioContext.currentTime);
    oscillator2.start(audioContext.currentTime + 0.1);
    oscillator1.stop(audioContext.currentTime + 0.8);
    oscillator2.stop(audioContext.currentTime + 0.8);
  };

  const playIncorrectSound = () => {
    // Play a playful "oops" sound
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(150, audioContext.currentTime + 0.3);

    gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
  };

  const playCompletionSound = () => {
    // Play a celebratory cascade
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const frequencies = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6

    frequencies.forEach((freq, index) => {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.value = freq;

      const startTime = audioContext.currentTime + (index * 0.15);
      gainNode.gain.setValueAtTime(0.2, startTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.5);

      oscillator.start(startTime);
      oscillator.stop(startTime + 0.5);
    });
  };

  const handleStartGame = async () => {
    try {
      const response = await api.post('/trivia/start/');
      setSessionId(response.data.id);
      setGameState('playing');
      gameStartTime.current = Date.now();
      setQuestionStartTime(Date.now());
    } catch (error: any) {
      alert(error.response?.data?.error || 'Failed to start game');
    }
  };

  const handleSubmitAnswer = async () => {
    if (!userAnswer || !sessionId || !triviaData) return;

    const currentQuestion = triviaData.questions[currentQuestionIndex];
    const timeTaken = Math.floor((Date.now() - questionStartTime) / 1000);

    try {
      const response = await api.post('/trivia/submit_answer/', {
        session_id: sessionId,
        question_id: currentQuestion.id,
        answer: userAnswer,
        time_taken_seconds: timeTaken,
      });

      setScore(response.data.current_score);

      // Play appropriate sound
      if (response.data.is_correct) {
        playCorrectSound();
      } else {
        playIncorrectSound();
      }

      setAnswerFeedback({
        show: true,
        correct: response.data.is_correct,
        explanation: response.data.explanation,
      });

      // Move to next question after showing feedback
      setTimeout(() => {
        setAnswerFeedback(null);
        if (currentQuestionIndex < triviaData.questions.length - 1) {
          setCurrentQuestionIndex(currentQuestionIndex + 1);
          setUserAnswer('');
          setQuestionStartTime(Date.now());
        } else {
          handleCompleteGame();
        }
      }, 3000);
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleCompleteGame = async () => {
    if (!sessionId) return;

    const totalTime = Math.floor((Date.now() - gameStartTime.current) / 1000);

    try {
      const response = await api.post('/trivia/complete/', {
        session_id: sessionId,
        total_time_seconds: totalTime,
      });

      playCompletionSound();
      setResults(response.data);
      setGameState('results');
      fetchLeaderboard();
    } catch (error) {
      console.error('Error completing game:', error);
    }
  };

  const handleTimeUp = () => {
    alert('Time\'s up! Completing your game now...');
    handleCompleteGame();
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'hard': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  if (gameState === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="w-full flex items-center justify-center min-h-screen py-8">
      <div className="w-full max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="accent-pink">Midnight</span> Mysteries
          </h1>
          <p className="text-lg text-gray-300">Daily Adult Trivia Challenge</p>
          {triviaData && (
            <p className="text-[--primary-hot-pink] font-semibold mt-2">
              Today's Theme: {triviaData.theme}
            </p>
          )}
        </div>

        {/* Start Screen */}
        {gameState === 'start' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <GlassCard className="p-8">
              <h2 className="text-2xl font-bold mb-6">Ready to Play?</h2>
              <div className="space-y-4 mb-8">
                <div className="flex items-start gap-3">
                  <span className="text-3xl">🎯</span>
                  <div>
                    <h3 className="font-semibold mb-1">15 Sensual Questions</h3>
                    <p className="text-sm text-gray-400">Test your knowledge with our witty, sexy, challenging adult trivia</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-3xl">⏱️</span>
                  <div>
                    <h3 className="font-semibold mb-1">5 Minute Timer</h3>
                    <p className="text-sm text-gray-400">Beat the clock for bonus points!</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-3xl">🏆</span>
                  <div>
                    <h3 className="font-semibold mb-1">Win Prizes</h3>
                    <p className="text-sm text-gray-400">1st: 100pts, 2nd: 50pts, 3rd: 25pts + 10pts for playing</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-3xl">💰</span>
                  <div>
                    <h3 className="font-semibold mb-1">Earn Discounts</h3>
                    <p className="text-sm text-gray-400">1 point = $0.10 off your purchases!</p>
                  </div>
                </div>
              </div>
              <GlassButton fullWidth onClick={handleStartGame}>
                Start Today's Trivia
              </GlassButton>
            </GlassCard>

            {/* Leaderboard */}
            <GlassCard className="p-8">
              <h2 className="text-2xl font-bold mb-6">Today's Leaderboard</h2>
              {leaderboard.length === 0 ? (
                <p className="text-gray-400 text-center py-8">Be the first to play today!</p>
              ) : (
                <div className="space-y-3">
                  {leaderboard.slice(0, 10).map((entry) => (
                    <div
                      key={entry.rank}
                      className={`flex items-center justify-between p-3 rounded-lg ${
                        entry.rank <= 3 ? 'bg-[--primary-hot-pink]/20' : 'bg-white/5'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{getRankBadge(entry.rank)}</span>
                        <span className="font-semibold">{entry.username}</span>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-[--primary-hot-pink]">{entry.final_score}</div>
                        <div className="text-xs text-gray-400">{formatTime(entry.time_taken_seconds)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </GlassCard>
          </div>
        )}

        {/* Playing Screen */}
        {gameState === 'playing' && triviaData && !answerFeedback && (
          <div className="max-w-3xl mx-auto">
            <GlassCard className={`p-8 transition-all duration-500 ${showQuestionAnimation ? 'scale-105 shadow-2xl shadow-[--primary-hot-pink]/50' : 'scale-100'}`}>
              {/* Timer & Progress */}
              <div className="flex items-center justify-between mb-6">
                <div>
                  <span className="text-sm text-gray-400">Question {currentQuestionIndex + 1} of {triviaData.questions.length}</span>
                  <div className="text-2xl font-bold text-[--primary-hot-pink]">Score: {score}</div>
                </div>
                <div className="text-right">
                  <div className={`text-3xl font-bold ${timeRemaining < 60 ? 'text-red-400 animate-pulse' : 'text-[--primary-hot-pink]'}`}>
                    {formatTime(timeRemaining)}
                  </div>
                  <span className="text-sm text-gray-400">Time Remaining</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-2 bg-white/10 rounded-full mb-8">
                <div
                  className="h-full bg-gradient-to-r from-[--primary-hot-pink] to-[--primary-pink-light] rounded-full transition-all duration-300"
                  style={{ width: `${((currentQuestionIndex + 1) / triviaData.questions.length) * 100}%` }}
                />
              </div>

              {/* Question */}
              {triviaData.questions[currentQuestionIndex] && (
                <>
                  <div className="mb-6">
                    <div className="flex items-center gap-3 mb-4">
                      <span className={`text-sm font-semibold px-3 py-1 rounded-full ${
                        triviaData.questions[currentQuestionIndex].difficulty === 'easy' ? 'bg-green-500/20 text-green-400' :
                        triviaData.questions[currentQuestionIndex].difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {triviaData.questions[currentQuestionIndex].difficulty.toUpperCase()}
                      </span>
                      <span className="text-sm text-gray-400">
                        Worth {triviaData.questions[currentQuestionIndex].max_points} points
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold leading-relaxed">
                      {triviaData.questions[currentQuestionIndex].question_text}
                    </h3>
                  </div>

                  {/* Answer Options */}
                  {triviaData.questions[currentQuestionIndex].question_type === 'multiple_choice' && (
                    <div className="space-y-3 mb-8">
                      {(() => {
                        const currentQ = triviaData.questions[currentQuestionIndex];
                        const options = currentQ.options || {
                          A: currentQ.option_a,
                          B: currentQ.option_b,
                          C: currentQ.option_c,
                          D: currentQ.option_d,
                        };
                        return Object.entries(options)
                          .filter(([letter, optionText]) => optionText && optionText.trim() !== '')
                          .map(([letter, optionText], idx) => (
                            <button
                              key={letter}
                              onClick={() => setUserAnswer(letter)}
                              className={`w-full p-4 rounded-lg text-left transition-all duration-300 transform hover:scale-102 ${
                                userAnswer === letter
                                  ? 'bg-[--primary-hot-pink]/30 border-2 border-[--primary-hot-pink] shadow-lg shadow-[--primary-hot-pink]/30'
                                  : 'bg-white/5 border-2 border-transparent hover:border-[--primary-hot-pink]/50 hover:bg-white/10'
                              }`}
                              style={{
                                animationDelay: `${idx * 100}ms`,
                                animation: showQuestionAnimation ? 'slideInLeft 0.5s ease-out' : 'none'
                              }}
                            >
                              <span className="font-bold mr-3 text-[--primary-hot-pink]">{letter}.</span>
                              {optionText}
                            </button>
                          ));
                      })()}
                    </div>
                  )}

                  {triviaData.questions[currentQuestionIndex].question_type === 'true_false' && (
                    <div className="grid grid-cols-2 gap-4 mb-8">
                      <button
                        onClick={() => setUserAnswer('True')}
                        className={`p-6 rounded-lg font-bold text-lg transition ${
                          userAnswer === 'True'
                            ? 'bg-[--primary-hot-pink]/30 border-2 border-[--primary-hot-pink]'
                            : 'bg-white/5 border-2 border-transparent hover:border-[--primary-hot-pink]/50'
                        }`}
                      >
                        True
                      </button>
                      <button
                        onClick={() => setUserAnswer('False')}
                        className={`p-6 rounded-lg font-bold text-lg transition ${
                          userAnswer === 'False'
                            ? 'bg-[--primary-hot-pink]/30 border-2 border-[--primary-hot-pink]'
                            : 'bg-white/5 border-2 border-transparent hover:border-[--primary-hot-pink]/50'
                        }`}
                      >
                        False
                      </button>
                    </div>
                  )}

                  {triviaData.questions[currentQuestionIndex].question_type === 'fill_blank' && (
                    <input
                      type="text"
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      placeholder="Type your answer..."
                      className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none mb-8 text-lg"
                    />
                  )}

                  <GlassButton fullWidth onClick={handleSubmitAnswer} disabled={!userAnswer}>
                    Submit Answer
                  </GlassButton>
                </>
              )}
            </GlassCard>
          </div>
        )}

        {/* Answer Feedback */}
        {answerFeedback && (
          <div className="max-w-3xl mx-auto animate-fadeIn">
            <GlassCard className={`p-8 ${answerFeedback.correct ? 'border-green-500 bg-green-500/10' : 'border-red-500 bg-red-500/10'} border-2 animate-pulse-once`}>
              <div className="text-center">
                <div className={`text-6xl mb-4 animate-bounce-in ${answerFeedback.correct ? 'animate-spin-slow' : 'animate-shake'}`}>
                  {answerFeedback.correct ? '💋' : '😏'}
                </div>
                <h2 className="text-3xl font-bold mb-4">
                  {answerFeedback.correct ? 'Oh, You Naughty Genius!' : 'Not Quite, Darling...'}
                </h2>
                <p className="text-lg text-gray-300 leading-relaxed italic">{answerFeedback.explanation}</p>
              </div>
            </GlassCard>
          </div>
        )}

        {/* Results Screen */}
        {gameState === 'results' && results && (
          <div className="max-w-3xl mx-auto">
            <GlassCard className="p-8 text-center">
              <div className="text-6xl mb-4">{getRankBadge(results.rank)}</div>
              <h2 className="text-3xl font-bold mb-2">Game Complete!</h2>
              <p className="text-gray-400 mb-8">You finished in {getRankBadge(results.rank)} place</p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-3xl font-bold text-[--primary-hot-pink]">{results.final_score}</div>
                  <div className="text-sm text-gray-400">Final Score</div>
                </div>
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-3xl font-bold text-[--primary-hot-pink]">{results.rank}</div>
                  <div className="text-sm text-gray-400">Your Rank</div>
                </div>
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-3xl font-bold text-[--primary-hot-pink]">{results.placement_points}</div>
                  <div className="text-sm text-gray-400">Placement</div>
                </div>
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-3xl font-bold text-[--primary-hot-pink]">{results.total_bonus_points}</div>
                  <div className="text-sm text-gray-400">Total Points</div>
                </div>
              </div>

              {results.perfect_game && (
                <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-lg p-4 mb-8">
                  <div className="text-4xl mb-2">⭐</div>
                  <p className="font-bold text-yellow-400">PERFECT GAME!</p>
                  <p className="text-sm text-gray-300">You answered all questions correctly!</p>
                </div>
              )}

              <p className="text-gray-300 mb-8">
                Come back tomorrow for a new trivia challenge!
              </p>

              <div className="flex gap-4">
                <GlassButton fullWidth variant="secondary" onClick={() => router.push('/account')}>
                  View Stats
                </GlassButton>
                <GlassButton fullWidth onClick={() => router.push('/products')}>
                  Shop Now
                </GlassButton>
              </div>
            </GlassCard>

            {/* Show Leaderboard */}
            <GlassCard className="p-8 mt-6">
              <h2 className="text-2xl font-bold mb-6">Today's Leaderboard</h2>
              <div className="space-y-3">
                {leaderboard.map((entry) => (
                  <div
                    key={entry.rank}
                    className={`flex items-center justify-between p-3 rounded-lg ${
                      entry.rank <= 3 ? 'bg-[--primary-hot-pink]/20' : 'bg-white/5'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{getRankBadge(entry.rank)}</span>
                      <span className="font-semibold">{entry.username}</span>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-[--primary-hot-pink]">{entry.final_score}</div>
                      <div className="text-xs text-gray-400">{formatTime(entry.time_taken_seconds)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </div>
        )}
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes slideInLeft {
          from {
            opacity: 0;
            transform: translateX(-30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes pulse-once {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }

        @keyframes bounce-in {
          0% {
            transform: scale(0);
            opacity: 0;
          }
          50% {
            transform: scale(1.2);
          }
          100% {
            transform: scale(1);
            opacity: 1;
          }
        }

        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-10px) rotate(-5deg); }
          75% { transform: translateX(10px) rotate(5deg); }
        }

        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }

        .animate-pulse-once {
          animation: pulse-once 0.6s ease-out;
        }

        .animate-bounce-in {
          animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .animate-shake {
          animation: shake 0.5s ease-in-out;
        }

        .animate-spin-slow {
          animation: spin-slow 1s ease-in-out;
        }
      `}</style>
    </div>
  );
}
