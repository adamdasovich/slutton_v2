'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import { useAuthStore } from '@/store/authStore';
import api from '@/lib/api';

interface Order {
  id: number;
  order_number: string;
  status: string;
  total_amount: string;
  created_at: string;
  items_count: number;
}

interface GameProgress {
  id: number;
  game: number;
  game_name: string;
  completed: boolean;
  last_played: string;
  play_time_minutes: number;
}

interface TriviaStats {
  username: string;
  total_games_played: number;
  total_points_earned: number;
  available_points: number;
  discount_amount: number;
  first_place_finishes: number;
  second_place_finishes: number;
  third_place_finishes: number;
  current_streak: number;
  longest_streak: number;
  last_played_date: string | null;
  perfect_games: number;
}

interface UserProfile {
  id: number;
  username: string;
  email: string;
  date_of_birth: string | null;
  phone_number: string;
  age_verified: boolean;
  created_at: string;
}

export default function AccountPage() {
  const router = useRouter();
  const { user, isAuthenticated, setUser } = useAuthStore();
  const [activeTab, setActiveTab] = useState<'overview' | 'orders' | 'games' | 'settings'>('overview');
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [gameProgress, setGameProgress] = useState<GameProgress[]>([]);
  const [triviaStats, setTriviaStats] = useState<TriviaStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [editedProfile, setEditedProfile] = useState({
    email: '',
    phone_number: '',
    date_of_birth: '',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchProfile();
    fetchOrders();
    fetchGameProgress();
    fetchTriviaStats();
  }, [isAuthenticated]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await api.get('/auth/profile/');
      setProfile(response.data);
      setEditedProfile({
        email: response.data.email || '',
        phone_number: response.data.phone_number || '',
        date_of_birth: response.data.date_of_birth || '',
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders/');
      setOrders(response.data.results || response.data);
    } catch (error: any) {
      // Orders endpoint may not exist yet - just log and continue
      if (error.response?.status !== 404) {
        console.error('Error fetching orders:', error);
      }
      setOrders([]);
    }
  };

  const fetchGameProgress = async () => {
    try {
      const response = await api.get('/games/progress/');
      setGameProgress(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching game progress:', error);
    }
  };

  const fetchTriviaStats = async () => {
    try {
      const response = await api.get('/trivia/my_stats/');
      setTriviaStats(response.data);
    } catch (error) {
      console.error('Error fetching trivia stats:', error);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      const response = await api.patch('/auth/profile/update/', editedProfile);
      setProfile(response.data);
      setUser(response.data);
      setEditMode(false);
      alert('Profile updated successfully!');
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'text-green-400';
      case 'pending':
        return 'text-yellow-400';
      case 'processing':
        return 'text-blue-400';
      case 'cancelled':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">
            Welcome back, <span className="accent-pink">{profile?.username}</span>
          </h1>
          <p className="text-gray-400">Manage your account, orders, and preferences</p>
        </div>

        {/* Tabs */}
        <div className="mb-8 flex gap-4 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-3 rounded-lg transition whitespace-nowrap ${
              activeTab === 'overview'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('orders')}
            className={`px-6 py-3 rounded-lg transition whitespace-nowrap ${
              activeTab === 'orders'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            Order History
          </button>
          <button
            onClick={() => setActiveTab('games')}
            className={`px-6 py-3 rounded-lg transition whitespace-nowrap ${
              activeTab === 'games'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            Game Progress
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`px-6 py-3 rounded-lg transition whitespace-nowrap ${
              activeTab === 'settings'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            Settings
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Account Info */}
            <GlassCard className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[--primary-hot-pink] to-[--primary-pink-dark] flex items-center justify-center text-2xl font-bold">
                  {profile?.username.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h3 className="text-xl font-bold">{profile?.username}</h3>
                  <p className="text-sm text-gray-400">{profile?.email}</p>
                </div>
              </div>
              <div className="space-y-2 text-sm">
                <p className="text-gray-400">
                  Member since: {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'N/A'}
                </p>
                <p className="text-gray-400">
                  Age Verified: {profile?.age_verified ? '✅ Yes' : '❌ No'}
                </p>
              </div>
            </GlassCard>

            {/* Quick Stats */}
            <GlassCard className="p-6">
              <h3 className="text-xl font-bold mb-4">Quick Stats</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Total Orders</span>
                  <span className="text-2xl font-bold text-[--primary-hot-pink]">{orders.length}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Games Played</span>
                  <span className="text-2xl font-bold text-[--primary-hot-pink]">
                    {gameProgress.length + (triviaStats?.total_games_played || 0)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Trivia Points</span>
                  <span className="text-2xl font-bold text-[--primary-hot-pink]">
                    {triviaStats?.available_points || 0}
                  </span>
                </div>
              </div>
            </GlassCard>

            {/* Recent Activity */}
            <GlassCard className="p-6">
              <h3 className="text-xl font-bold mb-4">Recent Activity</h3>
              <div className="space-y-3">
                {orders.slice(0, 3).map((order) => (
                  <div key={order.id} className="text-sm">
                    <p className="font-semibold">Order #{order.order_number}</p>
                    <p className="text-gray-400">${order.total_amount}</p>
                  </div>
                ))}
                {orders.length === 0 && <p className="text-gray-400 text-sm">No orders yet</p>}
              </div>
            </GlassCard>
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <GlassCard className="p-6">
            <h2 className="text-2xl font-bold mb-6">Order History</h2>
            {orders.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🛍️</div>
                <p className="text-xl text-gray-400 mb-4">No orders yet</p>
                <Link href="/products">
                  <GlassButton>Start Shopping</GlassButton>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {orders.map((order) => (
                  <div key={order.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <h3 className="font-bold">Order #{order.order_number}</h3>
                        <p className="text-sm text-gray-400">
                          {new Date(order.created_at).toLocaleDateString()} • {order.items_count} items
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-[--primary-hot-pink]">${order.total_amount}</p>
                        <p className={`text-sm font-semibold ${getStatusColor(order.status)}`}>
                          {order.status.toUpperCase()}
                        </p>
                      </div>
                    </div>
                    <Link href={`/orders/${order.order_number}`}>
                      <GlassButton size="small">View Details</GlassButton>
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>
        )}

        {/* Games Tab */}
        {activeTab === 'games' && (
          <div className="space-y-6">
            {/* Trivia Stats - Featured */}
            {triviaStats && triviaStats.total_games_played > 0 && (
              <GlassCard className="p-6 border-2 border-[--primary-hot-pink]">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <span className="text-4xl">🎯</span>
                    <div>
                      <h2 className="text-2xl font-bold">Midnight Mysteries Trivia</h2>
                      <p className="text-sm text-gray-400">Your trivia journey</p>
                    </div>
                  </div>
                  <Link href="/trivia">
                    <GlassButton size="small">Play Today</GlassButton>
                  </Link>
                </div>

                {/* Points & Discount */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold text-[--primary-hot-pink]">{triviaStats.available_points}</div>
                    <div className="text-xs text-gray-400 mt-1">Available Points</div>
                  </div>
                  <div className="bg-gradient-to-br from-green-500/20 to-green-700/20 rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold text-green-400">${triviaStats.discount_amount.toFixed(2)}</div>
                    <div className="text-xs text-gray-400 mt-1">Discount Value</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold">{triviaStats.total_games_played}</div>
                    <div className="text-xs text-gray-400 mt-1">Games Played</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold">{triviaStats.current_streak}</div>
                    <div className="text-xs text-gray-400 mt-1">Day Streak</div>
                  </div>
                </div>

                {/* Achievements */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-3 bg-white/5 rounded-lg">
                    <div className="text-2xl mb-1">🥇</div>
                    <div className="font-bold text-yellow-400">{triviaStats.first_place_finishes}</div>
                    <div className="text-xs text-gray-400">1st Place</div>
                  </div>
                  <div className="text-center p-3 bg-white/5 rounded-lg">
                    <div className="text-2xl mb-1">🥈</div>
                    <div className="font-bold text-gray-300">{triviaStats.second_place_finishes}</div>
                    <div className="text-xs text-gray-400">2nd Place</div>
                  </div>
                  <div className="text-center p-3 bg-white/5 rounded-lg">
                    <div className="text-2xl mb-1">🥉</div>
                    <div className="font-bold text-orange-400">{triviaStats.third_place_finishes}</div>
                    <div className="text-xs text-gray-400">3rd Place</div>
                  </div>
                  <div className="text-center p-3 bg-white/5 rounded-lg">
                    <div className="text-2xl mb-1">⭐</div>
                    <div className="font-bold text-[--primary-hot-pink]">{triviaStats.perfect_games}</div>
                    <div className="text-xs text-gray-400">Perfect Games</div>
                  </div>
                </div>

                {triviaStats.last_played_date && (
                  <p className="text-sm text-gray-400 mt-4 text-center">
                    Last played: {new Date(triviaStats.last_played_date).toLocaleDateString()}
                  </p>
                )}
              </GlassCard>
            )}

            {/* Other Games */}
            <GlassCard className="p-6">
              <h2 className="text-2xl font-bold mb-6">Other Games Progress</h2>
              {gameProgress.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🎮</div>
                  <p className="text-xl text-gray-400 mb-4">No other games played yet</p>
                  <Link href="/games">
                    <GlassButton>Browse Games</GlassButton>
                  </Link>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {gameProgress.map((progress) => (
                    <div key={progress.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <h3 className="font-bold mb-2">{progress.game_name}</h3>
                      <div className="space-y-1 text-sm">
                        <p className="text-gray-400">
                          Status: {progress.completed ? '✅ Completed' : '⏳ In Progress'}
                        </p>
                        <p className="text-gray-400">
                          Play Time: {Math.floor(progress.play_time_minutes / 60)}h {progress.play_time_minutes % 60}m
                        </p>
                        <p className="text-gray-400">
                          Last Played: {new Date(progress.last_played).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </GlassCard>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <GlassCard className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Profile Settings</h2>
              {!editMode ? (
                <GlassButton size="small" onClick={() => setEditMode(true)}>
                  Edit Profile
                </GlassButton>
              ) : (
                <div className="flex gap-2">
                  <GlassButton size="small" onClick={handleUpdateProfile}>
                    Save
                  </GlassButton>
                  <GlassButton size="small" variant="secondary" onClick={() => setEditMode(false)}>
                    Cancel
                  </GlassButton>
                </div>
              )}
            </div>

            <div className="space-y-6 max-w-2xl">
              {/* Username (read-only) */}
              <div>
                <label className="block text-sm font-medium mb-2">Username</label>
                <input
                  type="text"
                  value={profile?.username || ''}
                  disabled
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 opacity-50 cursor-not-allowed"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={editMode ? editedProfile.email : profile?.email || ''}
                  onChange={(e) => setEditedProfile({ ...editedProfile, email: e.target.value })}
                  disabled={!editMode}
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none disabled:opacity-50"
                />
              </div>

              {/* Phone Number */}
              <div>
                <label className="block text-sm font-medium mb-2">Phone Number</label>
                <input
                  type="tel"
                  value={editMode ? editedProfile.phone_number : profile?.phone_number || ''}
                  onChange={(e) => setEditedProfile({ ...editedProfile, phone_number: e.target.value })}
                  disabled={!editMode}
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none disabled:opacity-50"
                />
              </div>

              {/* Date of Birth */}
              <div>
                <label className="block text-sm font-medium mb-2">Date of Birth</label>
                <input
                  type="date"
                  value={editMode ? editedProfile.date_of_birth : profile?.date_of_birth || ''}
                  onChange={(e) => setEditedProfile({ ...editedProfile, date_of_birth: e.target.value })}
                  disabled={!editMode}
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none disabled:opacity-50"
                />
              </div>
            </div>
          </GlassCard>
        )}
      </div>
    </div>
  );
}
