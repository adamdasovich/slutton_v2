'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useCartStore } from '@/store/cartStore';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';

export default function CartPage() {
  const router = useRouter();
  const { cart, loading, fetchCart, updateCartItem, removeCartItem } = useCartStore();

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const handleQuantityChange = async (itemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    try {
      await updateCartItem(itemId, newQuantity);
    } catch (error) {
      alert('Failed to update quantity');
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await removeCartItem(itemId);
    } catch (error) {
      alert('Failed to remove item');
    }
  };

  const handleCheckout = () => {
    router.push('/checkout');
  };

  if (loading && !cart) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-4xl font-bold mb-8">Shopping Cart</h1>

      {!cart || cart.items.length === 0 ? (
        <GlassCard className="p-8 text-center">
          <p className="text-xl text-gray-400 mb-6">Your cart is empty</p>
          <GlassButton onClick={() => router.push('/products')}>
            Continue Shopping
          </GlassButton>
        </GlassCard>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cart.items.map((item) => (
              <GlassCard key={item.id} className="p-6">
                <div className="flex gap-6">
                  {/* Product Image */}
                  <div className="w-24 h-24 flex-shrink-0">
                    {item.product.images && item.product.images.length > 0 ? (
                      <img
                        src={item.product.images[0].image}
                        alt={item.product.name}
                        className="w-full h-full object-cover rounded-lg"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 rounded-lg flex items-center justify-center text-4xl">
                        🎁
                      </div>
                    )}
                  </div>

                  {/* Product Details */}
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold mb-2">{item.product.name}</h3>
                    <p className="text-gray-400 mb-4">${parseFloat(item.product.price).toFixed(2)} each</p>

                    <div className="flex items-center gap-4">
                      {/* Quantity Controls */}
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                          className="w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 flex items-center justify-center transition"
                          disabled={loading}
                        >
                          −
                        </button>
                        <span className="w-12 text-center">{item.quantity}</span>
                        <button
                          onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                          className="w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 flex items-center justify-center transition"
                          disabled={loading}
                        >
                          +
                        </button>
                      </div>

                      {/* Remove Button */}
                      <button
                        onClick={() => handleRemoveItem(item.id)}
                        className="text-red-400 hover:text-red-300 transition"
                        disabled={loading}
                      >
                        Remove
                      </button>
                    </div>
                  </div>

                  {/* Subtotal */}
                  <div className="text-right">
                    <p className="text-xl font-bold text-[--primary-hot-pink]">
                      ${parseFloat(item.subtotal).toFixed(2)}
                    </p>
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <GlassCard className="p-6 sticky top-8">
              <h2 className="text-2xl font-bold mb-6">Order Summary</h2>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-400">
                  <span>Subtotal ({cart.total_items} items)</span>
                  <span>${parseFloat(cart.total_price).toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-400">
                  <span>Shipping</span>
                  <span>Calculated at checkout</span>
                </div>
                <div className="border-t border-white/10 pt-4 flex justify-between text-xl font-bold">
                  <span>Total</span>
                  <span className="text-[--primary-hot-pink]">${parseFloat(cart.total_price).toFixed(2)}</span>
                </div>
              </div>

              <GlassButton fullWidth onClick={handleCheckout}>
                Proceed to Checkout
              </GlassButton>

              <button
                onClick={() => router.push('/products')}
                className="w-full mt-4 py-3 text-center text-gray-400 hover:text-white transition"
              >
                Continue Shopping
              </button>
            </GlassCard>
          </div>
        </div>
      )}
    </div>
  );
}
