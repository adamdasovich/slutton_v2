'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import GlassCard from '@/components/ui/GlassCard';
import api from '@/lib/api';

interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image: string | null;
  product_count: number;
  created_at: string;
}

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const response = await api.get('/categories/');
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="accent-pink">Browse</span> Categories
          </h1>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            Explore our curated collections of premium adult products, organized by category for your convenience.
          </p>
        </div>

        {/* Categories Grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
            <p className="mt-4 text-gray-400">Loading categories...</p>
          </div>
        ) : categories.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-400">No categories found.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category) => (
              <Link href={`/categories/${category.slug}`} key={category.id}>
                <GlassCard className="overflow-hidden group cursor-pointer h-full transition-all duration-300 hover:scale-105">
                  {/* Category Image */}
                  <div className="relative h-48 bg-gradient-to-br from-[--primary-hot-pink]/30 to-[--primary-pink-dark]/30 overflow-hidden">
                    {category.image ? (
                      <img
                        src={category.image}
                        alt={category.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full">
                        <div className="text-7xl opacity-50">📦</div>
                      </div>
                    )}

                    {/* Overlay Gradient */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>

                    {/* Product Count Badge */}
                    <div className="absolute top-4 right-4 bg-[--primary-hot-pink]/90 backdrop-blur-sm text-white text-sm font-bold px-4 py-2 rounded-full shadow-lg">
                      {category.product_count} {category.product_count === 1 ? 'Product' : 'Products'}
                    </div>

                    {/* Category Name on Image */}
                    <div className="absolute bottom-4 left-4 right-4">
                      <h2 className="text-2xl font-bold text-white drop-shadow-lg group-hover:text-[--primary-hot-pink] transition-colors">
                        {category.name}
                      </h2>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    <p className="text-gray-300 leading-relaxed line-clamp-3">
                      {category.description || 'Explore our collection of premium products in this category.'}
                    </p>

                    <div className="mt-4 flex items-center justify-between">
                      <span className="text-sm text-gray-400">
                        View Collection
                      </span>
                      <svg
                        className="w-5 h-5 text-[--primary-hot-pink] group-hover:translate-x-2 transition-transform"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </div>
                  </div>
                </GlassCard>
              </Link>
            ))}
          </div>
        )}

        {/* Featured Categories Section */}
        {!loading && categories.length > 0 && (
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-8">
              Why Shop by <span className="accent-pink">Category</span>?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <GlassCard className="p-6 text-center">
                <div className="text-5xl mb-4">🎯</div>
                <h3 className="text-xl font-bold mb-2">Curated Selection</h3>
                <p className="text-gray-400 text-sm">
                  Each category features hand-picked products chosen for quality and satisfaction.
                </p>
              </GlassCard>

              <GlassCard className="p-6 text-center">
                <div className="text-5xl mb-4">🔍</div>
                <h3 className="text-xl font-bold mb-2">Easy Discovery</h3>
                <p className="text-gray-400 text-sm">
                  Find exactly what you're looking for with our organized collections.
                </p>
              </GlassCard>

              <GlassCard className="p-6 text-center">
                <div className="text-5xl mb-4">✨</div>
                <h3 className="text-xl font-bold mb-2">Expert Picks</h3>
                <p className="text-gray-400 text-sm">
                  Explore trending items and bestsellers in each category.
                </p>
              </GlassCard>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
