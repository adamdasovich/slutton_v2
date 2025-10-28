'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import api from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

// Board letter positions arranged in classic Ouija layout
const BOARD_LETTERS = [
  { char: 'A', x: 10, y: 25 },
  { char: 'B', x: 17, y: 25 },
  { char: 'C', x: 24, y: 25 },
  { char: 'D', x: 31, y: 25 },
  { char: 'E', x: 38, y: 25 },
  { char: 'F', x: 45, y: 25 },
  { char: 'G', x: 52, y: 25 },
  { char: 'H', x: 59, y: 25 },
  { char: 'I', x: 66, y: 25 },
  { char: 'J', x: 73, y: 25 },
  { char: 'K', x: 80, y: 25 },
  { char: 'L', x: 87, y: 25 },
  { char: 'M', x: 94, y: 25 },
  { char: 'N', x: 13, y: 40 },
  { char: 'O', x: 20, y: 40 },
  { char: 'P', x: 27, y: 40 },
  { char: 'Q', x: 34, y: 40 },
  { char: 'R', x: 41, y: 40 },
  { char: 'S', x: 48, y: 40 },
  { char: 'T', x: 55, y: 40 },
  { char: 'U', x: 62, y: 40 },
  { char: 'V', x: 69, y: 40 },
  { char: 'W', x: 76, y: 40 },
  { char: 'X', x: 83, y: 40 },
  { char: 'Y', x: 90, y: 40 },
  { char: 'Z', x: 97, y: 40 },
];

const BOARD_NUMBERS = [
  { char: '1', x: 15, y: 55 },
  { char: '2', x: 25, y: 55 },
  { char: '3', x: 35, y: 55 },
  { char: '4', x: 45, y: 55 },
  { char: '5', x: 55, y: 55 },
  { char: '6', x: 65, y: 55 },
  { char: '7', x: 75, y: 55 },
  { char: '8', x: 85, y: 55 },
  { char: '9', x: 92, y: 55 },
  { char: '0', x: 50, y: 65 },
];

const SPECIAL_POSITIONS = {
  YES: { x: 15, y: 10 },
  NO: { x: 85, y: 10 },
  GOODBYE: { x: 50, y: 80 },
};

// Sensual, mysterious messages for the Ouija board
const OUIJA_MESSAGES = [
  "DESIRE",
  "PLEASURE",
  "TEMPTATION",
  "SECRETS",
  "PASSION",
  "FANTASY",
  "MYSTERY",
  "SEDUCE",
  "ENCHANT",
  "ALLURE",
  "FORBIDDEN",
  "INTIMATE",
  "SENSUAL",
  "DIVINE",
  "IRRESISTIBLE",
];

interface Position {
  x: number;
  y: number;
}

export default function OuijaGame() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const boardRef = useRef<HTMLDivElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  const [planchettePos, setPlanchettePos] = useState<Position>({ x: 50, y: 50 });
  const [isInteracting, setIsInteracting] = useState(false);
  const [gameState, setGameState] = useState<'idle' | 'asking' | 'revealing' | 'complete'>('idle');
  const [currentMessage, setCurrentMessage] = useState('');
  const [revealedChars, setRevealedChars] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [particles, setParticles] = useState<Array<{ id: number; x: number; y: number }>>([]);

  // Initialize audio context
  useEffect(() => {
    if (typeof window !== 'undefined') {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    return () => {
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  // Ambient sound effect
  const playAmbientSound = (frequency: number, duration: number, volume: number = 0.1) => {
    if (!audioContextRef.current) return;

    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, ctx.currentTime);
    gainNode.gain.setValueAtTime(0, ctx.currentTime);
    gainNode.gain.linearRampToValueAtTime(volume, ctx.currentTime + 0.1);
    gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + duration);

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + duration);
  };

  // Whisper effect for planchette movement
  const playWhisperEffect = () => {
    playAmbientSound(200 + Math.random() * 100, 0.3, 0.05);
  };

  // Letter selection sound
  const playLetterSound = () => {
    playAmbientSound(400 + Math.random() * 200, 0.5, 0.08);
  };

  // Game start sound
  const playStartSound = () => {
    if (!audioContextRef.current) return;

    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.type = 'triangle';
    oscillator.frequency.setValueAtTime(150, ctx.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 1);

    gainNode.gain.setValueAtTime(0, ctx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.15, ctx.currentTime + 0.1);
    gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 1);

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + 1);
  };

  // Completion sound
  const playCompletionSound = () => {
    if (!audioContextRef.current) return;

    const ctx = audioContextRef.current;

    // Play a chord
    [261.63, 329.63, 392.00].forEach((freq, index) => {
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();

      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(freq, ctx.currentTime);

      gainNode.gain.setValueAtTime(0, ctx.currentTime + index * 0.1);
      gainNode.gain.linearRampToValueAtTime(0.1, ctx.currentTime + index * 0.1 + 0.1);
      gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 1.5);

      oscillator.connect(gainNode);
      gainNode.connect(ctx.destination);

      oscillator.start(ctx.currentTime + index * 0.1);
      oscillator.stop(ctx.currentTime + 1.5);
    });
  };

  // Particle effect for atmosphere
  useEffect(() => {
    const interval = setInterval(() => {
      const newParticle = {
        id: Date.now(),
        x: Math.random() * 100,
        y: Math.random() * 100,
      };
      setParticles(prev => [...prev.slice(-20), newParticle]);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // Mouse/Touch tracking for planchette
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isInteracting || gameState === 'revealing') return;

    const rect = boardRef.current?.getBoundingClientRect();
    if (!rect) return;

    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    setPlanchettePos({ x: Math.max(5, Math.min(95, x)), y: Math.max(5, Math.min(95, y)) });
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    if (!isInteracting || gameState === 'revealing') return;

    const rect = boardRef.current?.getBoundingClientRect();
    if (!rect) return;

    const touch = e.touches[0];
    const x = ((touch.clientX - rect.left) / rect.width) * 100;
    const y = ((touch.clientY - rect.top) / rect.height) * 100;

    setPlanchettePos({ x: Math.max(5, Math.min(95, x)), y: Math.max(5, Math.min(95, y)) });
  };

  const startGame = async () => {
    playStartSound();

    setGameState('asking');
    setIsInteracting(true);
    setStartTime(Date.now());
    setScore(0);
    setRevealedChars([]);

    // Select random message
    const message = OUIJA_MESSAGES[Math.floor(Math.random() * OUIJA_MESSAGES.length)];
    setCurrentMessage(message);

    // Track game play
    if (isAuthenticated) {
      try {
        await api.post('/games/games/ouija/play/');
      } catch (error) {
        console.error('Error tracking game play:', error);
      }
    }

    // Start revealing after a dramatic pause
    setTimeout(() => {
      revealMessage(message);
    }, 2000);
  };

  const revealMessage = async (message: string) => {
    setGameState('revealing');
    setIsInteracting(false);

    const chars = message.split('');

    for (let i = 0; i < chars.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1500)); // Slow, dramatic reveal

      const char = chars[i];
      let targetPos: Position;

      // Find position for this character
      const letterPos = BOARD_LETTERS.find(l => l.char === char);
      const numberPos = BOARD_NUMBERS.find(n => n.char === char);

      if (letterPos) {
        targetPos = { x: letterPos.x, y: letterPos.y };
      } else if (numberPos) {
        targetPos = { x: numberPos.x, y: numberPos.y };
      } else {
        targetPos = { x: 50, y: 50 };
      }

      // Animate planchette to position
      animatePlanchette(targetPos);
      playWhisperEffect();

      // Add character to revealed list
      setTimeout(() => {
        setRevealedChars(prev => [...prev, char]);
        playLetterSound();
      }, 800);
    }

    // Move to GOODBYE
    setTimeout(() => {
      animatePlanchette(SPECIAL_POSITIONS.GOODBYE);
      playWhisperEffect();
      setTimeout(() => {
        completeGame();
      }, 2000);
    }, (chars.length * 1500) + 1000);
  };

  const animatePlanchette = (targetPos: Position) => {
    const steps = 30;
    const currentPos = planchettePos;

    for (let i = 0; i <= steps; i++) {
      setTimeout(() => {
        const progress = i / steps;
        const easeProgress = 1 - Math.pow(1 - progress, 3); // Ease out cubic

        setPlanchettePos({
          x: currentPos.x + (targetPos.x - currentPos.x) * easeProgress,
          y: currentPos.y + (targetPos.y - currentPos.y) * easeProgress,
        });
      }, i * 20);
    }
  };

  const completeGame = async () => {
    setGameState('complete');
    playCompletionSound();

    // Calculate score based on message length and time
    const timeTaken = startTime ? (Date.now() - startTime) / 1000 : 0;
    const baseScore = currentMessage.length * 100;
    const timeBonus = Math.max(0, 1000 - timeTaken * 10);
    const finalScore = Math.round(baseScore + timeBonus);
    setScore(finalScore);

    // Save game completion
    if (isAuthenticated) {
      try {
        await api.post('/games/games/ouija/complete/', {
          score: finalScore,
          time_taken: timeTaken,
          completed_at: new Date().toISOString(),
        });
      } catch (error) {
        console.error('Error saving game:', error);
      }
    }
  };

  const resetGame = () => {
    setGameState('idle');
    setIsInteracting(false);
    setPlanchettePos({ x: 50, y: 50 });
    setCurrentMessage('');
    setRevealedChars([]);
    setScore(0);
    setStartTime(null);
  };

  return (
    <div className="w-full flex items-center justify-center min-h-screen bg-gradient-to-br from-black via-gray-900 to-black">
      <div className="w-full max-w-6xl mx-auto px-4 py-8">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-5xl md:text-7xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-500 via-amber-400 to-yellow-600">
            OUIJA BOARD
          </h1>
          <p className="text-gray-400 text-lg md:text-xl italic">
            Dare to ask the spirits...
          </p>
        </div>

        {/* Game Board */}
        <GlassCard className="relative p-8 md:p-12 bg-black/80 border-2 border-yellow-600/50 shadow-2xl">
          {/* Atmospheric particles */}
          {particles.map(particle => (
            <div
              key={particle.id}
              className="absolute w-1 h-1 bg-yellow-500/30 rounded-full animate-pulse"
              style={{
                left: `${particle.x}%`,
                top: `${particle.y}%`,
                animation: 'float 4s ease-in-out infinite',
              }}
            />
          ))}

          {/* Board Container */}
          <div
            ref={boardRef}
            className="relative w-full aspect-[4/3] bg-gradient-to-br from-gray-900 via-black to-gray-900 rounded-xl border-4 border-yellow-700 shadow-[0_0_50px_rgba(234,179,8,0.3)]"
            onMouseMove={handleMouseMove}
            onTouchMove={handleTouchMove}
            style={{ touchAction: 'none' }}
          >
            {/* YES and NO */}
            <div
              className="absolute text-yellow-500 font-bold text-2xl md:text-4xl tracking-wider"
              style={{ left: `${SPECIAL_POSITIONS.YES.x}%`, top: `${SPECIAL_POSITIONS.YES.y}%`, transform: 'translate(-50%, -50%)' }}
            >
              <div className="relative">
                <span className="text-shadow-glow">YES</span>
                <div className="absolute inset-0 blur-md bg-yellow-500/30 -z-10"></div>
              </div>
            </div>

            <div
              className="absolute text-yellow-500 font-bold text-2xl md:text-4xl tracking-wider"
              style={{ left: `${SPECIAL_POSITIONS.NO.x}%`, top: `${SPECIAL_POSITIONS.NO.y}%`, transform: 'translate(-50%, -50%)' }}
            >
              <div className="relative">
                <span className="text-shadow-glow">NO</span>
                <div className="absolute inset-0 blur-md bg-yellow-500/30 -z-10"></div>
              </div>
            </div>

            {/* Letters */}
            {BOARD_LETTERS.map((letter) => (
              <div
                key={letter.char}
                className="absolute text-yellow-600 font-serif text-lg md:text-2xl font-bold tracking-wide transition-all duration-300 hover:text-yellow-400 hover:scale-110"
                style={{ left: `${letter.x}%`, top: `${letter.y}%`, transform: 'translate(-50%, -50%)' }}
              >
                <div className="relative">
                  <span className={revealedChars.includes(letter.char) ? 'text-yellow-300 animate-pulse' : ''}>
                    {letter.char}
                  </span>
                  {revealedChars.includes(letter.char) && (
                    <div className="absolute inset-0 blur-lg bg-yellow-400/50 -z-10 animate-pulse"></div>
                  )}
                </div>
              </div>
            ))}

            {/* Numbers */}
            {BOARD_NUMBERS.map((number) => (
              <div
                key={number.char}
                className="absolute text-yellow-600 font-serif text-lg md:text-2xl font-bold transition-all duration-300 hover:text-yellow-400 hover:scale-110"
                style={{ left: `${number.x}%`, top: `${number.y}%`, transform: 'translate(-50%, -50%)' }}
              >
                {number.char}
              </div>
            ))}

            {/* GOODBYE */}
            <div
              className="absolute text-yellow-500 font-bold text-2xl md:text-4xl tracking-wider italic"
              style={{ left: `${SPECIAL_POSITIONS.GOODBYE.x}%`, top: `${SPECIAL_POSITIONS.GOODBYE.y}%`, transform: 'translate(-50%, -50%)' }}
            >
              <div className="relative">
                <span className="text-shadow-glow">GOODBYE</span>
                <div className="absolute inset-0 blur-md bg-yellow-500/30 -z-10"></div>
              </div>
            </div>

            {/* Planchette */}
            <div
              className="absolute w-16 h-16 md:w-20 md:h-20 transition-all duration-75"
              style={{
                left: `${planchettePos.x}%`,
                top: `${planchettePos.y}%`,
                transform: 'translate(-50%, -50%)',
              }}
            >
              {/* Planchette glow */}
              <div className="absolute inset-0 bg-yellow-500/20 rounded-full blur-xl animate-pulse"></div>

              {/* Planchette body */}
              <div className="relative w-full h-full">
                {/* Heart-shaped planchette (sensual design) */}
                <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-2xl">
                  {/* Outer glow */}
                  <defs>
                    <filter id="glow">
                      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                      <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                    <radialGradient id="planchetteGradient">
                      <stop offset="0%" stopColor="#FCD34D" />
                      <stop offset="50%" stopColor="#F59E0B" />
                      <stop offset="100%" stopColor="#B45309" />
                    </radialGradient>
                  </defs>

                  {/* Heart shape */}
                  <path
                    d="M 50,30 C 50,25 45,20 37,20 C 25,20 20,30 20,35 C 20,50 50,70 50,70 C 50,70 80,50 80,35 C 80,30 75,20 63,20 C 55,20 50,25 50,30 Z"
                    fill="url(#planchetteGradient)"
                    stroke="#854D0E"
                    strokeWidth="2"
                    filter="url(#glow)"
                  />

                  {/* Center viewing hole */}
                  <circle
                    cx="50"
                    cy="40"
                    r="8"
                    fill="rgba(0,0,0,0.8)"
                    stroke="#FCD34D"
                    strokeWidth="1.5"
                  />

                  {/* Decorative accents */}
                  <circle cx="50" cy="40" r="3" fill="#FCD34D" opacity="0.6" className="animate-pulse" />
                </svg>
              </div>
            </div>

            {/* Message Display */}
            {gameState !== 'idle' && (
              <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/80 px-6 py-3 rounded-lg border border-yellow-600/50">
                <p className="text-yellow-400 text-xl md:text-2xl font-bold tracking-widest">
                  {revealedChars.join('')}
                  {gameState === 'revealing' && <span className="animate-pulse">_</span>}
                </p>
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="mt-8 flex flex-col items-center gap-4">
            {gameState === 'idle' && (
              <GlassButton
                onClick={startGame}
                size="large"
                className="bg-gradient-to-r from-yellow-600 to-amber-700 hover:from-yellow-500 hover:to-amber-600 text-white font-bold text-xl px-12 py-4"
              >
                Summon the Spirits
              </GlassButton>
            )}

            {gameState === 'asking' && (
              <div className="text-center">
                <p className="text-yellow-400 text-lg md:text-xl italic animate-pulse">
                  The spirits are gathering...
                </p>
                <p className="text-gray-500 text-sm mt-2">
                  Move the planchette to explore the board
                </p>
              </div>
            )}

            {gameState === 'revealing' && (
              <p className="text-yellow-400 text-lg md:text-xl italic animate-pulse">
                The spirits speak...
              </p>
            )}

            {gameState === 'complete' && (
              <div className="text-center space-y-4">
                <div className="bg-gradient-to-r from-yellow-600/20 to-amber-700/20 px-8 py-6 rounded-lg border border-yellow-600/50">
                  <p className="text-yellow-400 text-2xl md:text-3xl font-bold mb-2">
                    Message: {currentMessage}
                  </p>
                  <p className="text-yellow-500 text-xl md:text-2xl font-bold">
                    Score: {score}
                  </p>
                </div>
                <div className="flex gap-4 justify-center">
                  <GlassButton
                    onClick={resetGame}
                    size="large"
                    className="bg-gradient-to-r from-yellow-600 to-amber-700 hover:from-yellow-500 hover:to-amber-600 text-white font-bold"
                  >
                    Consult Again
                  </GlassButton>
                  <GlassButton
                    onClick={() => router.push('/games')}
                    size="large"
                    className="bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white font-bold"
                  >
                    Back to Games
                  </GlassButton>
                </div>
              </div>
            )}
          </div>

          {/* Instructions */}
          <div className="mt-8 text-center text-gray-400 text-sm md:text-base">
            <p className="italic">
              Place your fingers on the planchette and let the spirits guide you through the darkness...
            </p>
          </div>
        </GlassCard>
      </div>

      {/* Custom CSS for additional effects */}
      <style jsx>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0px);
            opacity: 0;
          }
          50% {
            opacity: 0.3;
          }
          100% {
            transform: translateY(-100px);
            opacity: 0;
          }
        }

        .text-shadow-glow {
          text-shadow: 0 0 10px rgba(234, 179, 8, 0.8),
                       0 0 20px rgba(234, 179, 8, 0.5),
                       0 0 30px rgba(234, 179, 8, 0.3);
        }
      `}</style>
    </div>
  );
}
