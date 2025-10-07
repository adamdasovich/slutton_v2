'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import api from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

interface Card {
  id: number;
  imageUrl: string;
  isFlipped: boolean;
  isMatched: boolean;
}

export default function MemoryMatchGame() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [cards, setCards] = useState<Card[]>([]);
  const [flippedCards, setFlippedCards] = useState<number[]>([]);
  const [moves, setMoves] = useState(0);
  const [matches, setMatches] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameCompleted, setGameCompleted] = useState(false);
  const [timer, setTimer] = useState(0);
  const [score, setScore] = useState(0);
  const [dailyImages, setDailyImages] = useState<string[]>([]);
  const [theme, setTheme] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    fetchDailyImages();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  useEffect(() => {
    if (dailyImages.length > 0 && matches === dailyImages.length) {
      completeGame();
    }
  }, [matches, dailyImages]);

  const fetchDailyImages = async () => {
    try {
      const response = await api.get('/games/memory-images/today/');
      setDailyImages(response.data.images);
      setTheme(response.data.theme);
      setLoading(false);
      // Initialize game after images are fetched
      initializeGameWithImages(response.data.images);
    } catch (error) {
      console.error('Error fetching daily images:', error);
      // Fallback to default images
      const fallbackImages = [
        'https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=400&q=80',
        'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80',
        'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80',
        'https://images.unsplash.com/photo-1469122312224-c5846569feb1?w=400&q=80',
        'https://images.unsplash.com/photo-1612464409289-6de8b8c0e8a3?w=400&q=80',
        'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80',
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&q=80',
        'https://images.unsplash.com/photo-1603400521630-9f2de124b33b?w=400&q=80',
      ];
      setDailyImages(fallbackImages);
      setTheme('Sensual Classics');
      setLoading(false);
      initializeGameWithImages(fallbackImages);
    }
  };

  const initializeGameWithImages = (images: string[]) => {
    // Create pairs of cards
    const cardPairs = images.flatMap((imageUrl, index) => [
      { id: index * 2, imageUrl, isFlipped: false, isMatched: false },
      { id: index * 2 + 1, imageUrl, isFlipped: false, isMatched: false },
    ]);

    // Shuffle cards
    const shuffled = cardPairs.sort(() => Math.random() - 0.5);
    setCards(shuffled);
    setFlippedCards([]);
    setMoves(0);
    setMatches(0);
    setTimer(0);
    setGameStarted(false);
    setGameCompleted(false);
    setScore(0);
  };

  const initializeGame = () => {
    if (dailyImages.length > 0) {
      initializeGameWithImages(dailyImages);
    }
  };

  const startTimer = () => {
    if (!gameStarted) {
      setGameStarted(true);
      timerRef.current = setInterval(() => {
        setTimer((prev) => prev + 1);
      }, 1000);
    }
  };

  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const playSound = (frequency: number, duration: number, type: OscillatorType = 'sine') => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }

    const audioContext = audioContextRef.current;
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = frequency;
    oscillator.type = type;

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration);
  };

  const playFlipSound = () => {
    playSound(523.25, 0.1, 'sine'); // C5 note
  };

  const playMatchSound = () => {
    // Sensual success chime
    playSound(523.25, 0.2, 'sine'); // C5
    setTimeout(() => playSound(659.25, 0.2, 'sine'), 100); // E5
    setTimeout(() => playSound(783.99, 0.3, 'sine'), 200); // G5
  };

  const playMismatchSound = () => {
    playSound(200, 0.15, 'square'); // Low playful buzz
  };

  const playCompletionSound = () => {
    // Victory cascade
    const notes = [523.25, 587.33, 659.25, 783.99, 880.00];
    notes.forEach((freq, index) => {
      setTimeout(() => playSound(freq, 0.3, 'sine'), index * 100);
    });
  };

  const handleCardClick = (cardId: number) => {
    if (!gameStarted) startTimer();

    const card = cards.find((c) => c.id === cardId);
    if (!card || card.isFlipped || card.isMatched || flippedCards.length === 2) {
      return;
    }

    playFlipSound();

    const newFlippedCards = [...flippedCards, cardId];
    setFlippedCards(newFlippedCards);

    // Update card flip state
    setCards((prev) =>
      prev.map((c) => (c.id === cardId ? { ...c, isFlipped: true } : c))
    );

    // Check for match when 2 cards are flipped
    if (newFlippedCards.length === 2) {
      setMoves(moves + 1);

      const [firstId, secondId] = newFlippedCards;
      const firstCard = cards.find((c) => c.id === firstId);
      const secondCard = cards.find((c) => c.id === secondId);

      if (firstCard && secondCard && firstCard.imageUrl === secondCard.imageUrl) {
        // Match found!
        playMatchSound();
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              c.id === firstId || c.id === secondId ? { ...c, isMatched: true } : c
            )
          );
          setMatches((prev) => prev + 1);
          setFlippedCards([]);
        }, 500);
      } else {
        // No match
        playMismatchSound();
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              c.id === firstId || c.id === secondId ? { ...c, isFlipped: false } : c
            )
          );
          setFlippedCards([]);
        }, 1000);
      }
    }
  };

  const completeGame = async () => {
    stopTimer();
    setGameCompleted(true);
    playCompletionSound();

    // Calculate score: base 1000 points - (moves * 10) - (seconds * 2)
    const calculatedScore = Math.max(100, 1000 - moves * 10 - timer * 2);
    setScore(calculatedScore);

    // Save completion to backend if authenticated
    if (isAuthenticated) {
      try {
        await api.post('/games/games/memory-match/complete/', {
          score: calculatedScore,
          time_taken: timer,
          moves: moves,
          completed_at: new Date().toISOString(),
        });
      } catch (error) {
        console.error('Error saving game completion:', error);
      }
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="w-full flex items-center justify-center min-h-screen">
      <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <button
            onClick={() => router.back()}
            className="absolute left-8 top-8 text-gray-400 hover:text-white transition"
          >
            ← Back
          </button>

          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="accent-pink">Sensual</span> Memory Match
          </h1>
          {theme && (
            <p className="text-xl text-[--primary-hot-pink] mb-2">Today's Theme: {theme}</p>
          )}
          <p className="text-gray-300 max-w-2xl mx-auto">
            Test your memory with a sexy twist. Match pairs of sensual and provocative images!
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
          </div>
        ) : (
          <>
        {/* Game Stats */}
        <GlassCard className="p-6 mb-8">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-[--primary-hot-pink]">{moves}</div>
              <div className="text-sm text-gray-400">Moves</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[--primary-hot-pink]">
                {matches}/{dailyImages.length || 8}
              </div>
              <div className="text-sm text-gray-400">Matches</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-[--primary-hot-pink]">
                {formatTime(timer)}
              </div>
              <div className="text-sm text-gray-400">Time</div>
            </div>
          </div>
        </GlassCard>

        {/* Game Board */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          {cards.map((card) => (
            <div
              key={card.id}
              onClick={() => handleCardClick(card.id)}
              className={`
                aspect-square cursor-pointer relative
                transform transition-all duration-300
                ${card.isFlipped || card.isMatched ? 'rotate-y-180' : ''}
                ${card.isMatched ? 'scale-95 opacity-70' : 'hover:scale-105'}
              `}
              style={{ perspective: '1000px' }}
            >
              <div
                className={`
                  w-full h-full relative
                  transform-style-3d transition-transform duration-500
                  ${card.isFlipped || card.isMatched ? '[transform:rotateY(180deg)]' : ''}
                `}
              >
                {/* Card Back */}
                <div
                  className={`
                    absolute inset-0 rounded-xl overflow-hidden
                    bg-gradient-to-br from-[--primary-hot-pink]/30 to-[--primary-pink-dark]/30
                    border-2 border-[--primary-hot-pink]/50
                    flex items-center justify-center
                    backface-hidden
                    ${card.isFlipped || card.isMatched ? 'hidden' : ''}
                  `}
                >
                  <div className="text-6xl opacity-30">💋</div>
                </div>

                {/* Card Front */}
                <div
                  className={`
                    absolute inset-0 rounded-xl overflow-hidden
                    border-2 border-[--primary-hot-pink]
                    [transform:rotateY(180deg)]
                    backface-hidden
                    ${card.isFlipped || card.isMatched ? 'block' : 'hidden'}
                    ${card.isMatched ? 'opacity-70' : ''}
                  `}
                >
                  <img
                    src={card.imageUrl}
                    alt="Memory card"
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                  {card.isMatched && (
                    <div className="absolute inset-0 bg-[--primary-hot-pink]/30 backdrop-blur-sm flex items-center justify-center">
                      <div className="text-6xl animate-pulse">✓</div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Game Completed Modal */}
        {gameCompleted && (
          <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4">
            <GlassCard className="w-full max-w-md p-8 text-center animate-bounce-in">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-3xl font-bold mb-4">
                <span className="accent-pink">Congratulations!</span>
              </h2>
              <p className="text-gray-300 mb-6">
                You've completed the game with style and sensuality!
              </p>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="text-2xl font-bold text-[--primary-hot-pink]">{moves}</div>
                  <div className="text-xs text-gray-400">Moves</div>
                </div>
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="text-2xl font-bold text-[--primary-hot-pink]">
                    {formatTime(timer)}
                  </div>
                  <div className="text-xs text-gray-400">Time</div>
                </div>
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="text-2xl font-bold text-[--primary-hot-pink]">{score}</div>
                  <div className="text-xs text-gray-400">Score</div>
                </div>
              </div>

              <div className="space-y-3">
                <GlassButton fullWidth onClick={initializeGame}>
                  Play Again
                </GlassButton>
                <button
                  onClick={() => router.back()}
                  className="w-full px-6 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition"
                >
                  Back to Games
                </button>
              </div>
            </GlassCard>
          </div>
        )}

        {/* Reset Button */}
        <div className="text-center">
          <button
            onClick={initializeGame}
            className="px-6 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition text-sm"
          >
            Reset Game
          </button>
        </div>
        </>
        )}
      </div>
    </div>
  );
}
