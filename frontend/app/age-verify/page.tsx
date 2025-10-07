'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import { useAuthStore } from '@/store/authStore';
import api from '@/lib/api';

export default function AgeVerifyPage() {
  const router = useRouter();
  const { user, isAuthenticated, setUser } = useAuthStore();
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [confirmOver18, setConfirmOver18] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Redirect if not authenticated
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    // Redirect if already verified
    if (user?.age_verified) {
      router.push('/');
    }
  }, [isAuthenticated, user]);

  const calculateAge = (birthDate: string) => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }

    return age;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!dateOfBirth) {
      setError('Please enter your date of birth');
      return;
    }

    if (!confirmOver18) {
      setError('You must confirm you are 18 years or older');
      return;
    }

    const age = calculateAge(dateOfBirth);

    if (age < 18) {
      setError('You must be at least 18 years old to access this site');
      return;
    }

    setLoading(true);

    try {
      const response = await api.post('/auth/verify-age/', {
        date_of_birth: dateOfBirth,
        confirm_over_18: confirmOver18,
      });

      // Update user in store
      setUser(response.data.user);

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
        setError('Age verification failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDecline = () => {
    // Redirect away from the site
    router.push('https://www.google.com');
  };

  return (
    <div className="w-full min-h-screen flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-2xl">
        <GlassCard className="p-8 md:p-12">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🔞</div>
            <h1 className="text-3xl md:text-4xl font-bold mb-4">
              <span className="accent-pink">Age</span> Verification Required
            </h1>
            <p className="text-gray-300 text-lg">
              You must be 18 years or older to access this website
            </p>
          </div>

          {/* Warning Box */}
          <div className="bg-[--primary-hot-pink]/10 border border-[--primary-hot-pink]/30 rounded-lg p-6 mb-8">
            <h2 className="font-bold mb-2 text-lg">⚠️ Adult Content Warning</h2>
            <p className="text-sm text-gray-300 leading-relaxed">
              This website contains age-restricted materials including adult products and content.
              By entering this website, you confirm that you are at least 18 years of age and agree
              to view adult-oriented content. If you are not of legal age or find such material
              offensive, please leave now.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-sm text-red-200">
                {error}
              </div>
            )}

            {/* Date of Birth */}
            <div>
              <label htmlFor="dateOfBirth" className="block text-sm font-medium mb-2">
                Date of Birth <span className="text-[--primary-hot-pink]">*</span>
              </label>
              <input
                type="date"
                id="dateOfBirth"
                required
                value={dateOfBirth}
                onChange={(e) => setDateOfBirth(e.target.value)}
                max={new Date().toISOString().split('T')[0]}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none transition text-lg"
              />
              <p className="text-xs text-gray-400 mt-2">
                Please enter your actual date of birth. This information is used for age verification only.
              </p>
            </div>

            {/* Confirmation Checkbox */}
            <div className="flex items-start gap-3 p-4 bg-white/5 rounded-lg border border-white/10">
              <input
                type="checkbox"
                id="confirmOver18"
                checked={confirmOver18}
                onChange={(e) => setConfirmOver18(e.target.checked)}
                className="mt-1 w-5 h-5 rounded border-white/20 bg-white/5 accent-[--primary-hot-pink] cursor-pointer"
              />
              <label htmlFor="confirmOver18" className="text-sm cursor-pointer select-none">
                <span className="font-semibold">I certify that I am 18 years of age or older</span>
                <br />
                <span className="text-gray-400">
                  I understand that this website contains adult content and I am willingly choosing to view such content.
                </span>
              </label>
            </div>

            {/* Legal Disclaimer */}
            <div className="text-xs text-gray-500 leading-relaxed">
              By clicking "Enter Site", you acknowledge that you have read and understood our{' '}
              <span className="text-[--primary-hot-pink] cursor-pointer hover:underline">Terms of Service</span> and{' '}
              <span className="text-[--primary-hot-pink] cursor-pointer hover:underline">Privacy Policy</span>.
              You also confirm that you are legally allowed to view adult content in your jurisdiction.
            </div>

            {/* Buttons */}
            <div className="grid grid-cols-2 gap-4 pt-4">
              <GlassButton
                type="button"
                variant="secondary"
                onClick={handleDecline}
                disabled={loading}
              >
                I'm Under 18
              </GlassButton>
              <GlassButton
                type="submit"
                disabled={loading || !dateOfBirth || !confirmOver18}
              >
                {loading ? 'Verifying...' : 'Enter Site'}
              </GlassButton>
            </div>
          </form>

          {/* Additional Info */}
          <div className="mt-8 pt-8 border-t border-white/10">
            <h3 className="font-semibold mb-3 text-center">Why do we ask for this?</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="p-4 bg-white/5 rounded-lg">
                <div className="text-3xl mb-2">🔒</div>
                <p className="text-sm text-gray-400">Legal compliance and safety</p>
              </div>
              <div className="p-4 bg-white/5 rounded-lg">
                <div className="text-3xl mb-2">🛡️</div>
                <p className="text-sm text-gray-400">Protecting minors from adult content</p>
              </div>
              <div className="p-4 bg-white/5 rounded-lg">
                <div className="text-3xl mb-2">✅</div>
                <p className="text-sm text-gray-400">Ensuring responsible access</p>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Footer Note */}
        <div className="text-center mt-6 text-sm text-gray-500">
          <p>This verification is performed once per account.</p>
          <p className="mt-1">Your information is kept private and secure.</p>
        </div>
      </div>
    </div>
  );
}
