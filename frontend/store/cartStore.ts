import { create } from 'zustand';

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
  setCart: (cart: Cart) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  cart: null,
  setCart: (cart) => set({ cart }),
  clearCart: () => set({ cart: null }),
}));
