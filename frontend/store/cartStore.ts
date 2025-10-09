import { create } from 'zustand';
import api from '@/lib/api';

interface CartItem {
  id: number;
  product: any;
  quantity: number;
  subtotal: number;
}

interface Cart {
  id: number;
  items: CartItem[];
  total_price: number;
  total_items: number;
}

interface CartState {
  cart: Cart | null;
  loading: boolean;
  setCart: (cart: Cart) => void;
  fetchCart: () => Promise<void>;
  addToCart: (productId: number, quantity: number) => Promise<void>;
  updateCartItem: (itemId: number, quantity: number) => Promise<void>;
  removeCartItem: (itemId: number) => Promise<void>;
  clearCart: () => Promise<void>;
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  loading: false,

  setCart: (cart) => set({ cart }),

  fetchCart: async () => {
    try {
      set({ loading: true });
      const response = await api.get('/cart/');
      set({ cart: response.data, loading: false });
    } catch (error) {
      console.error('Error fetching cart:', error);
      set({ loading: false });
    }
  },

  addToCart: async (productId: number, quantity: number = 1) => {
    try {
      set({ loading: true });
      const response = await api.post('/cart/add_item/', {
        product_id: productId,
        quantity,
      });
      set({ cart: response.data, loading: false });
    } catch (error) {
      console.error('Error adding to cart:', error);
      set({ loading: false });
      throw error;
    }
  },

  updateCartItem: async (itemId: number, quantity: number) => {
    try {
      set({ loading: true });
      const response = await api.patch('/cart/update_item/', {
        item_id: itemId,
        quantity,
      });
      set({ cart: response.data, loading: false });
    } catch (error) {
      console.error('Error updating cart item:', error);
      set({ loading: false });
      throw error;
    }
  },

  removeCartItem: async (itemId: number) => {
    try {
      set({ loading: true });
      const response = await api.delete(`/cart/remove_item/?item_id=${itemId}`);
      set({ cart: response.data, loading: false });
    } catch (error) {
      console.error('Error removing cart item:', error);
      set({ loading: false });
      throw error;
    }
  },

  clearCart: async () => {
    try {
      set({ loading: true });
      const response = await api.delete('/cart/clear/');
      set({ cart: response.data, loading: false });
    } catch (error) {
      console.error('Error clearing cart:', error);
      set({ loading: false });
      throw error;
    }
  },
}));
