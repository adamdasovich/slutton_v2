'use client';

import Link from 'next/link';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import GlassButton from '../ui/GlassButton';

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const { cart } = useCartStore();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-card rounded-none border-x-0 border-t-0 backdrop-blur-xl">
      <div className="container mx-auto px-4 md:px-8 py-5 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="text-3xl font-bold">
          <span className="accent-pink">Louis</span>
          <span className="text-white"> Slutton</span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <Link href="/products" className="hover:text-[--primary-hot-pink] transition px-4">
            Products
          </Link>
          <Link href="/games" className="hover:text-[--primary-hot-pink] transition px-4">
            Games
          </Link>
          <Link href="/categories" className="hover:text-[--primary-hot-pink] transition px-4">
            Categories
          </Link>
        </nav>

        {/* Right Side */}
        <div className="flex items-center space-x-4">
          {/* Cart */}
          <Link href="/cart" className="relative">
            <svg
              className="w-6 h-6 hover:text-[--primary-hot-pink] transition"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            {cart && cart.total_items > 0 && (
              <span className="absolute -top-2 -right-2 bg-[--primary-hot-pink] text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {cart.total_items}
              </span>
            )}
          </Link>

          {/* Auth Buttons */}
          {isAuthenticated ? (
            <>
              <Link href="/account">
                <GlassButton variant="secondary">
                  {user?.username}
                </GlassButton>
              </Link>
              <GlassButton onClick={logout}>Logout</GlassButton>
            </>
          ) : (
            <>
              <Link href="/login">
                <GlassButton variant="secondary">Login</GlassButton>
              </Link>
              <Link href="/register">
                <GlassButton>Sign Up</GlassButton>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
