import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// API functions
export const authAPI = {
  register: (data: any) => api.post('/auth/register/', data),
  login: (data: any) => api.post('/auth/login/', data),
  verifyAge: (data: any) => api.post('/auth/verify-age/', data),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data: any) => api.patch('/auth/profile/update/', data),
};

export const productsAPI = {
  getAll: (params?: any) => api.get('/products/', { params }),
  getBySlug: (slug: string) => api.get(`/products/${slug}/`),
  getCategories: () => api.get('/categories/'),
  getVideos: (slug: string) => api.get(`/products/${slug}/videos/`),
};

export const cartAPI = {
  get: () => api.get('/cart/'),
  addItem: (productId: number, quantity: number) =>
    api.post('/cart/add_item/', { product_id: productId, quantity }),
  updateItem: (itemId: number, quantity: number) =>
    api.patch('/cart/update_item/', { item_id: itemId, quantity }),
  removeItem: (itemId: number) =>
    api.delete(`/cart/remove_item/?item_id=${itemId}`),
  clear: () => api.delete('/cart/clear/'),
};

export const ordersAPI = {
  getAll: () => api.get('/orders/'),
  getByNumber: (orderNumber: string) => api.get(`/orders/${orderNumber}/`),
  createPaymentIntent: () => api.post('/orders/create_payment_intent/'),
  confirmOrder: (data: any) => api.post('/orders/confirm_order/', data),
};

export const ratingsAPI = {
  getForProduct: (slug: string) => api.get(`/products/${slug}/ratings/`),
  create: (slug: string, rating: number) =>
    api.post(`/products/${slug}/ratings/`, { rating }),
  update: (slug: string, ratingId: number, rating: number) =>
    api.patch(`/products/${slug}/ratings/${ratingId}/`, { rating }),
};

export const commentsAPI = {
  getForProduct: (slug: string) => api.get(`/products/${slug}/comments/`),
  create: (slug: string, content: string, parentId?: number) =>
    api.post(`/products/${slug}/comments/`, { content, parent_comment: parentId }),
  update: (slug: string, commentId: number, content: string) =>
    api.patch(`/products/${slug}/comments/${commentId}/`, { content }),
  delete: (slug: string, commentId: number) =>
    api.delete(`/products/${slug}/comments/${commentId}/`),
};
