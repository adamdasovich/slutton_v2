'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import api from '@/lib/api';

interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image: string | null;
  product_count: number;
}

interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  stock_quantity: number;
  category_name: string;
  main_image: string | null;
  average_rating: number;
}

export default function CategoryDetailPage() {
  const params = useParams();
  const [category, setCategory] = useState<Category | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<string>('name');

  useEffect(() => {
    if (params.slug) {
      fetchCategory();
      fetchProducts();
    }
  }, [params.slug, sortBy]);

  const fetchCategory = async () => {
    try {
      const response = await api.get(`/categories/${params.slug}/`);
      setCategory(response.data);
    } catch (error) {
      console.error('Error fetching category:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/products/', {
        params: {
          category: category?.id,
          ordering: sortBy,
        },
      });
      setProducts(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
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

  if (!category) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Category Header */}
        <div className="mb-12">
          <GlassCard className="overflow-hidden">
            <div className="relative h-64 bg-gradient-to-br from-[--primary-hot-pink]/30 to-[--primary-pink-dark]/30">
              {category.image ? (
                <img src={category.image} alt={category.name} className="w-full h-full object-cover" />
              ) : (
                <div className="flex items-center justify-center h-full text-8xl opacity-50">📦</div>
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent"></div>
              <div className="absolute bottom-0 left-0 right-0 p-8">
                <h1 className="text-4xl md:text-5xl font-bold mb-3">{category.name}</h1>
                <p className="text-lg text-gray-200 max-w-3xl">
                  {category.description || 'Explore our collection of premium products.'}
                </p>
                <p className="text-sm text-gray-300 mt-2">
                  {category.product_count} {category.product_count === 1 ? 'Product' : 'Products'} Available
                </p>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Sort Options */}
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">Products in this Category</h2>
          <div className="flex items-center gap-3">
            <label className="text-sm text-gray-400">Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none cursor-pointer"
            >
              <option value="name">Name</option>
              <option value="-created_at">Newest</option>
              <option value="price">Price: Low to High</option>
              <option value="-price">Price: High to Low</option>
              <option value="-average_rating">Highest Rated</option>
            </select>
          </div>
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
            <p className="mt-4 text-gray-400">Loading products...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <GlassCard className="p-12 max-w-md mx-auto">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-xl text-gray-400 mb-2">No products in this category yet.</p>
              <p className="text-sm text-gray-500">Check back soon for new arrivals!</p>
              <Link href="/products" className="mt-6 inline-block">
                <GlassButton>Browse All Products</GlassButton>
              </Link>
            </GlassCard>
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

        {/* Related Categories */}
        {!loading && products.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold mb-6">Looking for something else?</h2>
            <GlassCard className="p-6 text-center">
              <p className="text-gray-400 mb-4">
                Browse our other categories to find exactly what you're looking for.
              </p>
              <Link href="/categories">
                <GlassButton>View All Categories</GlassButton>
              </Link>
            </GlassCard>
          </div>
        )}
      </div>
    </div>
  );
}
