'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import { useCartStore } from '@/store/cartStore';
import { useAuthStore } from '@/store/authStore';
import CheckoutForm from '@/components/checkout/CheckoutForm';
import GlassCard from '@/components/ui/GlassCard';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export default function CheckoutPage() {
  const router = useRouter();
  const { cart, fetchCart } = useCartStore();
  const { isAuthenticated } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/checkout');
      return;
    }

    fetchCart().finally(() => setLoading(false));
  }, [isAuthenticated, fetchCart, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <GlassCard className="p-8 text-center">
          <p className="text-xl text-gray-400 mb-6">Your cart is empty</p>
          <button
            onClick={() => router.push('/products')}
            className="px-6 py-3 bg-gradient-to-r from-[--primary-hot-pink] to-[--primary-pink-dark] rounded-lg font-semibold hover:opacity-90 transition"
          >
            Continue Shopping
          </button>
        </GlassCard>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-4xl font-bold mb-8">Checkout</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Checkout Form */}
        <div className="lg:col-span-2">
          <Elements stripe={stripePromise}>
            <CheckoutForm />
          </Elements>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <GlassCard className="p-6 sticky top-8">
            <h2 className="text-2xl font-bold mb-6">Order Summary</h2>

            <div className="space-y-4 mb-6">
              {cart.items.map((item) => (
                <div key={item.id} className="flex justify-between text-sm">
                  <span className="text-gray-400">
                    {item.product.name} × {item.quantity}
                  </span>
                  <span className="font-semibold">${parseFloat(item.subtotal).toFixed(2)}</span>
                </div>
              ))}
            </div>

            <div className="border-t border-white/10 pt-4 space-y-2">
              <div className="flex justify-between text-gray-400">
                <span>Subtotal</span>
                <span>${parseFloat(cart.total_price).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-gray-400">
                <span>Shipping</span>
                <span>$0.00</span>
              </div>
              <div className="flex justify-between text-xl font-bold pt-2">
                <span>Total</span>
                <span className="text-[--primary-hot-pink]">${parseFloat(cart.total_price).toFixed(2)}</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
