'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import { useAuthStore } from '@/store/authStore';
import api from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const { setUser } = useAuthStore();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Login
      const loginResponse = await api.post('/auth/login/', {
        username: formData.username,
        password: formData.password,
      });

      // Store tokens
      localStorage.setItem('access_token', loginResponse.data.access);
      localStorage.setItem('refresh_token', loginResponse.data.refresh);

      // Get user profile
      const profileResponse = await api.get('/auth/profile/');
      setUser(profileResponse.data);

      // Redirect to home
      router.push('/');
    } catch (err: any) {
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object') {
          const errorMessages = Object.entries(errorData)
            .map(([key, value]) => `${key}: ${value}`)
            .join(', ');
          setError(errorMessages);
        } else {
          setError(errorData);
        }
      } else {
        setError('Login failed. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex items-center justify-center min-h-[calc(100vh-160px)]">
      <div className="w-full max-w-md mx-auto px-4 py-8">
        <GlassCard className="p-8">
          <h1 className="text-3xl font-bold text-center mb-8">
            Welcome Back
          </h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-sm text-red-200">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="username" className="block text-sm font-medium mb-2">
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                required
                value={formData.username}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none transition"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none transition"
              />
            </div>

            <GlassButton type="submit" fullWidth disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </GlassButton>
          </form>

          <p className="text-center mt-6 text-sm text-gray-400">
            Don't have an account?{' '}
            <Link href="/register" className="text-[--primary-hot-pink] hover:underline">
              Sign Up
            </Link>
          </p>
        </GlassCard>
      </div>
    </div>
  );
}
