'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import api from '@/lib/api';

interface Game {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description: string;
  category: number;
  category_name: string;
  game_url: string;
  thumbnail_url: string | null;
  preview_gif_url: string | null;
  difficulty: string;
  play_count: number;
  average_rating: number;
  duration_minutes: number;
  is_featured: boolean;
  requires_account: boolean;
}

interface GameCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  game_count: number;
}

export default function GamesPage() {
  const router = useRouter();
  const [games, setGames] = useState<Game[]>([]);
  const [categories, setCategories] = useState<GameCategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedGame, setSelectedGame] = useState<Game | null>(null);
  const [loading, setLoading] = useState(true);
  const [triviaData, setTriviaData] = useState<any>(null);

  useEffect(() => {
    fetchGames();
    fetchCategories();
    fetchTriviaInfo();
  }, [selectedCategory]);

  const fetchGames = async () => {
    try {
      setLoading(true);
      const params = selectedCategory !== 'all' ? { category: selectedCategory } : {};
      const response = await api.get('/games/games/', { params });
      setGames(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/games/categories/');
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTriviaInfo = async () => {
    try {
      const response = await api.get('/trivia/today/');
      setTriviaData(response.data);
    } catch (error) {
      console.error('Error fetching trivia info:', error);
    }
  };

  const handlePlayGame = async (game: Game) => {
    try {
      // Increment play count
      await api.post(`/games/games/${game.slug}/play/`);

      // Check if game URL is internal (starts with /)
      if (game.game_url.startsWith('/')) {
        router.push(game.game_url);
      } else {
        // External URL - open in modal
        setSelectedGame(game);
      }
    } catch (error) {
      console.error('Error starting game:', error);
      // Still navigate/open even if play count fails
      if (game.game_url.startsWith('/')) {
        router.push(game.game_url);
      } else {
        setSelectedGame(game);
      }
    }
  };

  const closeGameModal = () => {
    setSelectedGame(null);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'text-green-400';
      case 'medium':
        return 'text-yellow-400';
      case 'hard':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="accent-pink">Interactive</span> Games
          </h1>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            Explore our collection of enticing adult games. Immerse yourself in interactive experiences designed for pleasure.
          </p>
        </div>

        {/* Category Filter */}
        <div className="mb-8 flex flex-wrap gap-3 justify-center">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-6 py-2 rounded-lg transition ${
              selectedCategory === 'all'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            All Games
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id.toString())}
              className={`px-6 py-2 rounded-lg transition ${
                selectedCategory === category.id.toString()
                  ? 'bg-[--primary-hot-pink] text-white'
                  : 'bg-white/5 hover:bg-white/10'
              }`}
            >
              {category.icon && <span className="mr-2">{category.icon}</span>}
              {category.name}
              <span className="ml-2 text-sm opacity-70">({category.game_count})</span>
            </button>
          ))}
        </div>

        {/* Featured: Daily Trivia */}
        {triviaData && (
          <div className="mb-8">
            <GlassCard className="overflow-hidden border-2 border-[--primary-hot-pink]">
              <div className="grid md:grid-cols-2 gap-6 p-6">
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-5xl">🎯</span>
                    <div>
                      <div className="text-xs uppercase tracking-wider text-[--primary-hot-pink] font-bold mb-1">
                        Featured Daily Game
                      </div>
                      <h2 className="text-3xl font-bold">Midnight Mysteries Trivia</h2>
                    </div>
                  </div>

                  <p className="text-gray-300 mb-4">
                    <span className="font-semibold text-[--primary-hot-pink]">Today's Theme:</span> {triviaData.trivia.theme}
                  </p>

                  <p className="text-gray-400 mb-6">
                    Test your knowledge with 15 witty, sexy, challenging questions. Compete daily for top spots and earn points for discounts!
                  </p>

                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-2xl font-bold text-[--primary-hot-pink]">15</div>
                      <div className="text-xs text-gray-400">Questions</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-2xl font-bold text-[--primary-hot-pink]">5min</div>
                      <div className="text-xs text-gray-400">Time Limit</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-2xl font-bold text-[--primary-hot-pink]">1x/day</div>
                      <div className="text-xs text-gray-400">Play Limit</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-3">
                      <div className="text-2xl font-bold text-[--primary-hot-pink]">100pts</div>
                      <div className="text-xs text-gray-400">1st Place</div>
                    </div>
                  </div>

                  <GlassButton
                    fullWidth
                    onClick={() => router.push('/trivia')}
                    disabled={triviaData.has_played}
                  >
                    {triviaData.has_played ? 'Already Played Today' : 'Play Now'}
                  </GlassButton>

                  {triviaData.has_played && (
                    <p className="text-sm text-center text-gray-400 mt-3">
                      Come back tomorrow for a new challenge!
                    </p>
                  )}
                </div>

                <div className="flex flex-col justify-center items-center bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 rounded-lg p-6">
                  <div className="text-6xl mb-4">💋</div>
                  <h3 className="text-xl font-bold mb-2 text-center">How It Works</h3>
                  <ul className="space-y-2 text-sm text-gray-300">
                    <li>✓ Answer 15 sensual questions</li>
                    <li>✓ Earn points for correct answers</li>
                    <li>✓ Compete on live leaderboard</li>
                    <li>✓ Win bonus points for top 3</li>
                    <li>✓ Convert points to discounts</li>
                  </ul>
                  <div className="mt-4 text-center text-xs text-gray-400">
                    1 point = $0.10 off your purchases
                  </div>
                </div>
              </div>
            </GlassCard>
          </div>
        )}

        {/* Games Grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
            <p className="mt-4 text-gray-400">Loading games...</p>
          </div>
        ) : games.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-400">No games found in this category.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {games.map((game) => (
              <GlassCard key={game.id} className="overflow-hidden group cursor-pointer">
                {/* Thumbnail */}
                <div
                  className="relative h-48 bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 overflow-hidden"
                  onClick={() => handlePlayGame(game)}
                >
                  {game.preview_gif_url || game.thumbnail_url ? (
                    <img
                      src={game.preview_gif_url || game.thumbnail_url || ''}
                      alt={game.name}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <div className="text-6xl opacity-50">🎮</div>
                    </div>
                  )}

                  {/* Play Overlay */}
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="text-white text-6xl">▶</div>
                  </div>

                  {/* Featured Badge */}
                  {game.is_featured && (
                    <div className="absolute top-3 right-3 bg-[--primary-hot-pink] text-white text-xs font-bold px-3 py-1 rounded-full">
                      FEATURED
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2 group-hover:text-[--primary-hot-pink] transition">
                    {game.name}
                  </h3>

                  <p className="text-sm text-gray-400 mb-4 line-clamp-2">
                    {game.short_description}
                  </p>

                  {/* Metadata */}
                  <div className="flex items-center justify-between text-sm mb-4">
                    <span className="text-gray-400">{game.category_name}</span>
                    <span className={`font-semibold ${getDifficultyColor(game.difficulty)}`}>
                      {game.difficulty.toUpperCase()}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-400 mb-4">
                    <div className="flex items-center gap-1">
                      <span>⭐</span>
                      <span>{game.average_rating > 0 ? game.average_rating.toFixed(1) : 'New'}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>👥</span>
                      <span>{game.play_count.toLocaleString()} plays</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>⏱️</span>
                      <span>{game.duration_minutes}min</span>
                    </div>
                  </div>

                  <GlassButton
                    fullWidth
                    onClick={() => handlePlayGame(game)}
                  >
                    Play Now
                  </GlassButton>
                </div>
              </GlassCard>
            ))}
          </div>
        )}

        {/* Game Modal */}
        {selectedGame && (
          <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="w-full max-w-6xl bg-[--bg-dark] rounded-2xl border border-[--primary-hot-pink]/30 overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-white/10">
                <div>
                  <h2 className="text-2xl font-bold">{selectedGame.name}</h2>
                  <p className="text-sm text-gray-400">{selectedGame.category_name}</p>
                </div>
                <button
                  onClick={closeGameModal}
                  className="text-gray-400 hover:text-white text-3xl leading-none"
                >
                  ×
                </button>
              </div>

              {/* Game iframe */}
              <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
                <iframe
                  src={selectedGame.game_url}
                  className="absolute inset-0 w-full h-full"
                  frameBorder="0"
                  allowFullScreen
                  allow="autoplay; fullscreen"
                />
              </div>

              {/* Description */}
              <div className="p-6 border-t border-white/10">
                <p className="text-gray-300">{selectedGame.description}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
