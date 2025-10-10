'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { useCartStore } from '@/store/cartStore';
import api from '@/lib/api';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';

interface CheckoutFormProps {
  clientSecret: string;
}

export default function CheckoutForm({ clientSecret }: CheckoutFormProps) {
  const router = useRouter();
  const stripe = useStripe();
  const elements = useElements();
  const { clearCart } = useCartStore();

  const [processing, setProcessing] = useState(false);

  // Shipping Address
  const [shippingAddress, setShippingAddress] = useState({
    line1: '',
    line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'US',
  });

  // Billing Address
  const [billingAddress, setBillingAddress] = useState({
    line1: '',
    line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'US',
  });

  const [sameAsShipping, setSameAsShipping] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);

    try {
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        redirect: 'if_required',
      });

      if (error) {
        alert(error.message);
        setProcessing(false);
        return;
      }

      if (paymentIntent && paymentIntent.status === 'succeeded') {
        // Confirm order with backend
        const orderData = {
          payment_intent_id: paymentIntent.id,
          shipping_address_line1: shippingAddress.line1,
          shipping_address_line2: shippingAddress.line2,
          shipping_city: shippingAddress.city,
          shipping_state: shippingAddress.state,
          shipping_postal_code: shippingAddress.postal_code,
          shipping_country: shippingAddress.country,
          billing_address_line1: sameAsShipping ? shippingAddress.line1 : billingAddress.line1,
          billing_address_line2: sameAsShipping ? shippingAddress.line2 : billingAddress.line2,
          billing_city: sameAsShipping ? shippingAddress.city : billingAddress.city,
          billing_state: sameAsShipping ? shippingAddress.state : billingAddress.state,
          billing_postal_code: sameAsShipping ? shippingAddress.postal_code : billingAddress.postal_code,
          billing_country: sameAsShipping ? shippingAddress.country : billingAddress.country,
        };

        await api.post('/orders/confirm_order/', orderData);
        await clearCart();

        alert('Order placed successfully!');
        router.push('/account');
      }
    } catch (error: any) {
      console.error('Error confirming order:', error);
      alert(error.response?.data?.error || 'Failed to complete order');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Shipping Address */}
      <GlassCard className="p-6 mb-6">
        <h2 className="text-2xl font-bold mb-6">Shipping Address</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-2">Street Address</label>
            <input
              type="text"
              value={shippingAddress.line1}
              onChange={(e) => setShippingAddress({ ...shippingAddress, line1: e.target.value })}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">Apartment, suite, etc. (optional)</label>
            <input
              type="text"
              value={shippingAddress.line2}
              onChange={(e) => setShippingAddress({ ...shippingAddress, line2: e.target.value })}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">City</label>
              <input
                type="text"
                value={shippingAddress.city}
                onChange={(e) => setShippingAddress({ ...shippingAddress, city: e.target.value })}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">State</label>
              <input
                type="text"
                value={shippingAddress.state}
                onChange={(e) => setShippingAddress({ ...shippingAddress, state: e.target.value })}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                required
              />
            </div>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">ZIP Code</label>
            <input
              type="text"
              value={shippingAddress.postal_code}
              onChange={(e) => setShippingAddress({ ...shippingAddress, postal_code: e.target.value })}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
              required
            />
          </div>
        </div>
      </GlassCard>

      {/* Billing Address */}
      <GlassCard className="p-6 mb-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">Billing Address</h2>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={sameAsShipping}
              onChange={(e) => setSameAsShipping(e.target.checked)}
              className="w-4 h-4 rounded border-white/10"
            />
            <span className="text-sm text-gray-400">Same as shipping</span>
          </label>
        </div>

        {!sameAsShipping && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Street Address</label>
              <input
                type="text"
                value={billingAddress.line1}
                onChange={(e) => setBillingAddress({ ...billingAddress, line1: e.target.value })}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Apartment, suite, etc. (optional)</label>
              <input
                type="text"
                value={billingAddress.line2}
                onChange={(e) => setBillingAddress({ ...billingAddress, line2: e.target.value })}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">City</label>
                <input
                  type="text"
                  value={billingAddress.city}
                  onChange={(e) => setBillingAddress({ ...billingAddress, city: e.target.value })}
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">State</label>
                <input
                  type="text"
                  value={billingAddress.state}
                  onChange={(e) => setBillingAddress({ ...billingAddress, state: e.target.value })}
                  className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">ZIP Code</label>
              <input
                type="text"
                value={billingAddress.postal_code}
                onChange={(e) => setBillingAddress({ ...billingAddress, postal_code: e.target.value })}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                required
              />
            </div>
          </div>
        )}
      </GlassCard>

      {/* Payment */}
      <GlassCard className="p-6 mb-6">
        <h2 className="text-2xl font-bold mb-6">Payment Information</h2>
        <PaymentElement />
      </GlassCard>

      <GlassButton
        type="submit"
        disabled={!stripe || processing}
        fullWidth
      >
        {processing ? 'Processing...' : 'Place Order'}
      </GlassButton>
    </form>
  );
}
