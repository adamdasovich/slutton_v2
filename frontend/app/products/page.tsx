'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import api from '@/lib/api';

interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  stock_quantity: number;
  category: number;
  category_name: string;
  main_image: string | null;
  average_rating: number;
  created_at: string;
}

interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, [selectedCategory, searchQuery]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (selectedCategory !== 'all') {
        params.category = selectedCategory;
      }
      if (searchQuery) {
        params.search = searchQuery;
      }
      const response = await api.get('/products/', { params });
      setProducts(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories/');
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const renderStars = (rating: number) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={i <= rating ? 'text-[--primary-hot-pink]' : 'text-gray-600'}>
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="accent-pink">Luxury</span> Products
          </h1>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            Discover our exclusive collection of premium adult products. Quality, discretion, and pleasure guaranteed.
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full max-w-md mx-auto block px-6 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none transition"
          />
        </div>

        {/* Category Filter */}
        <div className="mb-8 flex flex-wrap gap-3 justify-center">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-6 py-2 rounded-lg transition ${
              selectedCategory === 'all'
                ? 'bg-[--primary-hot-pink] text-white'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            All Products
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id.toString())}
              className={`px-6 py-2 rounded-lg transition ${
                selectedCategory === category.id.toString()
                  ? 'bg-[--primary-hot-pink] text-white'
                  : 'bg-white/5 hover:bg-white/10'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
            <p className="mt-4 text-gray-400">Loading products...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-400">No products found.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <Link href={`/products/${product.slug}`} key={product.id}>
                <GlassCard className="overflow-hidden group cursor-pointer h-full flex flex-col">
                  {/* Product Image */}
                  <div className="relative h-64 bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 overflow-hidden">
                    {product.main_image ? (
                      <img
                        src={product.main_image}
                        alt={product.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full">
                        <div className="text-6xl opacity-50">🎁</div>
                      </div>
                    )}

                    {/* Stock Badge */}
                    {product.stock_quantity === 0 && (
                      <div className="absolute top-3 right-3 bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                        OUT OF STOCK
                      </div>
                    )}
                  </div>

                  {/* Content */}
                  <div className="p-6 flex-1 flex flex-col">
                    <h3 className="text-lg font-bold mb-2 group-hover:text-[--primary-hot-pink] transition line-clamp-2">
                      {product.name}
                    </h3>

                    <p className="text-sm text-gray-400 mb-3 line-clamp-2 flex-1">
                      {product.description}
                    </p>

                    {/* Category */}
                    <div className="text-xs text-gray-500 mb-3">
                      {product.category_name}
                    </div>

                    {/* Rating */}
                    <div className="flex items-center gap-2 mb-4">
                      <div className="flex">
                        {renderStars(Math.round(product.average_rating))}
                      </div>
                      <span className="text-sm text-gray-400">
                        ({product.average_rating > 0 ? product.average_rating.toFixed(1) : 'New'})
                      </span>
                    </div>

                    {/* Price */}
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-[--primary-hot-pink]">
                        ${product.price}
                      </span>
                      <GlassButton size="small">View</GlassButton>
                    </div>
                  </div>
                </GlassCard>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
