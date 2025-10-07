'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import api from '@/lib/api';

interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  stock_quantity: number;
  category_name: string;
  average_rating: number;
  images: Array<{ id: number; image: string; alt_text: string }>;
  videos: Array<{ id: number; video_file: string; thumbnail: string; title: string }>;
}

interface Comment {
  id: number;
  user_id: number;
  username: string;
  content: string;
  parent_comment: number | null;
  is_edited: boolean;
  replies: Comment[];
  created_at: string;
  updated_at: string;
}

interface Rating {
  id: number;
  user_id: number;
  username: string;
  rating: number;
  review: string;
  created_at: string;
  updated_at: string;
}

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const { addToCart } = useCartStore();

  const [product, setProduct] = useState<Product | null>(null);
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [userRating, setUserRating] = useState(0);
  const [userReview, setUserReview] = useState('');
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [editingRatingId, setEditingRatingId] = useState<number | null>(null);
  const [editRating, setEditRating] = useState(0);
  const [editReview, setEditReview] = useState('');
  const [userExistingRating, setUserExistingRating] = useState<Rating | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    if (params.slug) {
      fetchProduct();
      fetchComments();
      fetchRatings();
      connectWebSocket();
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        setWsConnected(false);
      }
    };
  }, [params.slug]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/products/${params.slug}/`);
      setProduct(response.data);
      if (response.data.images?.length > 0) {
        setSelectedImage(response.data.images[0].image);
      }
    } catch (error) {
      console.error('Error fetching product:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await api.get(`/products/${params.slug}/comments/`);
      setComments(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const fetchRatings = async () => {
    try {
      const response = await api.get(`/products/${params.slug}/ratings/`);
      const ratingsData = response.data.results || response.data;
      setRatings(ratingsData);

      // Find if current user has already rated
      if (isAuthenticated && user) {
        const existing = ratingsData.find((r: Rating) => r.user_id === user.id);
        if (existing) {
          setUserExistingRating(existing);
          setUserRating(existing.rating);
          setUserReview(existing.review || '');
        }
      }
    } catch (error) {
      console.error('Error fetching ratings:', error);
    }
  };

  const connectWebSocket = () => {
    // Close existing connection if any
    if (wsRef.current) {
      wsRef.current.close();
    }

    // Get JWT token from localStorage
    const token = localStorage.getItem('access_token');

    // Pass token in query string
    const wsUrl = token
      ? `ws://localhost:8000/ws/comments/${params.slug}/?token=${token}`
      : `ws://localhost:8000/ws/comments/${params.slug}/`;

    console.log('Connecting to WebSocket:', wsUrl);

    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected successfully');
      setWsConnected(true);
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket message received:', data);

      if (data.error) {
        alert(data.error);
        return;
      }

      if (data.action === 'new') {
        // Add new comment to the list
        setComments((prev) => [data.comment, ...prev]);
      } else if (data.action === 'edit') {
        // Update edited comment
        setComments((prev) =>
          prev.map((comment) =>
            comment.id === data.comment.id ? data.comment : comment
          )
        );
      } else if (data.action === 'delete') {
        // Remove deleted comment
        setComments((prev) => prev.filter((comment) => comment.id !== data.comment_id));
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };

    wsRef.current.onclose = (event) => {
      console.log('WebSocket disconnected', event.code, event.reason);
      setWsConnected(false);

      // Attempt to reconnect after 3 seconds if not a normal closure
      if (event.code !== 1000) {
        console.log('Attempting to reconnect in 3 seconds...');
        setTimeout(() => {
          if (params.slug) {
            connectWebSocket();
          }
        }, 3000);
      }
    };
  };

  const handleAddToCart = async () => {
    if (!product) return;

    try {
      await addToCart(product.id, quantity);
      alert('Added to cart!');
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('Failed to add to cart');
    }
  };

  const handleSubmitComment = () => {
    if (!newComment.trim()) {
      alert('Please enter a comment');
      return;
    }

    if (!isAuthenticated) {
      alert('Please log in to comment');
      return;
    }

    if (!wsRef.current) {
      alert('WebSocket not connected. Please refresh the page.');
      return;
    }

    // Check if WebSocket is open
    if (wsRef.current.readyState !== WebSocket.OPEN) {
      alert('WebSocket is not connected. Attempting to reconnect...');
      connectWebSocket();
      return;
    }

    try {
      wsRef.current.send(
        JSON.stringify({
          action: 'new_comment',
          content: newComment.trim(),
        })
      );
      setNewComment('');
    } catch (error) {
      console.error('Error sending comment:', error);
      alert('Failed to send comment. Please try again.');
    }
  };

  const handleSubmitRating = async () => {
    if (userRating === 0) {
      alert('Please select a star rating before submitting.');
      return;
    }

    try {
      await api.post(`/products/${params.slug}/ratings/`, {
        rating: userRating,
        review: userReview,
      });
      await fetchRatings();
      await fetchProduct(); // Refresh to get updated average rating
      alert(userExistingRating ? 'Rating updated!' : 'Rating submitted!');
    } catch (error) {
      console.error('Error submitting rating:', error);
      alert('Failed to submit rating');
    }
  };

  const handleEditRating = (rating: Rating) => {
    setEditingRatingId(rating.id);
    setEditRating(rating.rating);
    setEditReview(rating.review || '');
  };

  const handleUpdateRating = async (ratingId: number) => {
    if (editRating === 0) return;

    try {
      await api.patch(`/products/${params.slug}/ratings/${ratingId}/`, {
        rating: editRating,
        review: editReview,
      });
      setEditingRatingId(null);
      fetchRatings();
      fetchProduct();
      alert('Rating updated!');
    } catch (error) {
      console.error('Error updating rating:', error);
      alert('Failed to update rating');
    }
  };

  const handleDeleteRating = async (ratingId: number) => {
    if (!confirm('Are you sure you want to delete your rating?')) return;

    try {
      await api.delete(`/products/${params.slug}/ratings/${ratingId}/`);
      fetchRatings();
      fetchProduct();
      setUserExistingRating(null);
      setUserRating(0);
      setUserReview('');
      alert('Rating deleted!');
    } catch (error) {
      console.error('Error deleting rating:', error);
      alert('Failed to delete rating');
    }
  };

  const handleCancelEdit = () => {
    setEditingRatingId(null);
    setEditRating(0);
    setEditReview('');
  };

  const renderStars = (
    rating: number,
    interactive: boolean = false,
    setter?: (rating: number) => void
  ) => {
    const stars = [];
    const handleClick = setter || setUserRating;

    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`text-2xl cursor-${interactive ? 'pointer' : 'default'} ${
            i <= rating ? 'text-[--primary-hot-pink]' : 'text-gray-600'
          }`}
          onClick={() => interactive && handleClick(i)}
        >
          ★
        </span>
      );
    }
    return stars;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[--primary-hot-pink] border-t-transparent"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-xl text-gray-400">Product not found</p>
      </div>
    );
  }

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Product Details */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Left: Images */}
          <div>
            <GlassCard className="p-4 mb-4">
              <div className="aspect-square bg-gradient-to-br from-[--primary-hot-pink]/20 to-[--primary-pink-dark]/20 rounded-lg overflow-hidden">
                {selectedImage ? (
                  <img src={selectedImage} alt={product.name} className="w-full h-full object-cover" />
                ) : (
                  <div className="flex items-center justify-center h-full text-6xl opacity-50">🎁</div>
                )}
              </div>
            </GlassCard>

            {/* Thumbnails */}
            {product.images && product.images.length > 1 && (
              <div className="grid grid-cols-4 gap-2">
                {product.images.map((img) => (
                  <div
                    key={img.id}
                    onClick={() => setSelectedImage(img.image)}
                    className={`cursor-pointer rounded-lg overflow-hidden border-2 ${
                      selectedImage === img.image ? 'border-[--primary-hot-pink]' : 'border-transparent'
                    }`}
                  >
                    <img src={img.image} alt={img.alt_text} className="w-full h-full object-cover aspect-square" />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Right: Details */}
          <div>
            <h1 className="text-4xl font-bold mb-4">{product.name}</h1>

            <div className="flex items-center gap-4 mb-4">
              <div className="flex">{renderStars(Math.round(product.average_rating))}</div>
              <span className="text-gray-400">({product.average_rating.toFixed(1)})</span>
            </div>

            <p className="text-3xl font-bold text-[--primary-hot-pink] mb-6">${product.price}</p>

            <p className="text-gray-300 mb-6 leading-relaxed">{product.description}</p>

            <GlassCard className="p-6 mb-6">
              <p className="text-sm text-gray-400 mb-4">Category: {product.category_name}</p>
              <p className="text-sm text-gray-400 mb-4">
                Stock: {product.stock_quantity > 0 ? `${product.stock_quantity} available` : 'Out of stock'}
              </p>

              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm">Quantity:</label>
                <input
                  type="number"
                  min="1"
                  max={product.stock_quantity}
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                  className="w-20 px-3 py-2 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                />
              </div>

              <GlassButton
                fullWidth
                onClick={handleAddToCart}
                disabled={product.stock_quantity === 0}
              >
                {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
              </GlassButton>
            </GlassCard>
          </div>
        </div>

        {/* Videos Section */}
        {product.videos && product.videos.length > 0 && (
          <GlassCard className="p-6 mb-12">
            <h2 className="text-2xl font-bold mb-6">Product Videos</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {product.videos.map((video) => (
                <div
                  key={video.id}
                  onClick={() => setSelectedVideo(video.video_file)}
                  className="cursor-pointer group"
                >
                  <div className="relative rounded-lg overflow-hidden">
                    <img
                      src={video.thumbnail}
                      alt={video.title}
                      className="w-full aspect-video object-cover group-hover:scale-110 transition-transform"
                    />
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="text-white text-4xl">▶</div>
                    </div>
                  </div>
                  <p className="text-sm mt-2">{video.title}</p>
                </div>
              ))}
            </div>
          </GlassCard>
        )}

        {/* Ratings Section */}
        <GlassCard className="p-6 mb-12">
          <h2 className="text-2xl font-bold mb-6">Ratings & Reviews</h2>

          {isAuthenticated && (
            <div className="mb-8 pb-8 border-b border-white/10">
              <h3 className="text-lg font-semibold mb-4">
                {userExistingRating ? 'Update Your Review' : 'Leave a Review'}
              </h3>
              <div className="mb-4">
                <p className="text-sm text-gray-400 mb-2">Your Rating *</p>
                <div className="flex gap-2">{renderStars(userRating, true)}</div>
                {userRating === 0 && (
                  <p className="text-xs text-gray-500 mt-1">Click the stars to rate this product</p>
                )}
              </div>
              <textarea
                value={userReview}
                onChange={(e) => setUserReview(e.target.value)}
                placeholder="Share your thoughts... (optional)"
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none mb-4"
                rows={4}
              />
              <div className="flex gap-3">
                <GlassButton onClick={handleSubmitRating} disabled={userRating === 0}>
                  {userExistingRating ? 'Update Review' : 'Submit Review'}
                </GlassButton>
                {userExistingRating && (
                  <button
                    onClick={() => handleDeleteRating(userExistingRating.id)}
                    className="px-6 py-3 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 transition"
                  >
                    Delete Review
                  </button>
                )}
              </div>
            </div>
          )}

          <div className="space-y-6">
            {ratings.length === 0 ? (
              <p className="text-gray-400 text-center py-8">No reviews yet. Be the first to review!</p>
            ) : (
              ratings.map((rating) => (
                <div key={rating.id} className="pb-6 border-b border-white/10 last:border-0">
                  {editingRatingId === rating.id ? (
                    // Edit mode
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="font-semibold">Edit Your Review</h4>
                        <button
                          onClick={handleCancelEdit}
                          className="text-sm text-gray-400 hover:text-white"
                        >
                          Cancel
                        </button>
                      </div>
                      <div className="flex gap-2">{renderStars(editRating, true, setEditRating)}</div>
                      <textarea
                        value={editReview}
                        onChange={(e) => setEditReview(e.target.value)}
                        placeholder="Update your review..."
                        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none"
                        rows={4}
                      />
                      <GlassButton onClick={() => handleUpdateRating(rating.id)}>
                        Save Changes
                      </GlassButton>
                    </div>
                  ) : (
                    // View mode
                    <>
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className="font-semibold text-lg">{rating.username}</span>
                            <div className="flex text-sm">{renderStars(rating.rating)}</div>
                          </div>
                          <span className="text-sm text-gray-400">
                            {new Date(rating.created_at).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                            })}
                            {rating.updated_at !== rating.created_at && (
                              <span className="ml-2">(edited)</span>
                            )}
                          </span>
                        </div>
                        {user && rating.user_id === user.id && (
                          <button
                            onClick={() => handleEditRating(rating)}
                            className="text-sm text-[--primary-hot-pink] hover:underline"
                          >
                            Edit
                          </button>
                        )}
                      </div>
                      {rating.review && (
                        <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">
                          {rating.review}
                        </p>
                      )}
                    </>
                  )}
                </div>
              ))
            )}
          </div>
        </GlassCard>

        {/* Comments Section */}
        <GlassCard className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Live Comments</h2>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-xs text-gray-400">
                {wsConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>

          {!isAuthenticated && (
            <div className="mb-6 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
              <p className="text-sm text-yellow-400">Please log in to post comments</p>
            </div>
          )}

          {isAuthenticated && (
            <div className="mb-6">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Write a comment..."
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-[--primary-hot-pink] focus:outline-none mb-4"
                rows={3}
                disabled={!wsConnected}
              />
              <div className="flex items-center justify-between">
                <GlassButton
                  onClick={handleSubmitComment}
                  disabled={!wsConnected || !newComment.trim()}
                >
                  Post Comment
                </GlassButton>
                {!wsConnected && (
                  <span className="text-sm text-red-400">Connection lost. Reconnecting...</span>
                )}
              </div>
            </div>
          )}

          <div className="space-y-4">
            {comments.length === 0 ? (
              <p className="text-gray-400 text-center py-8">No comments yet. Be the first to comment!</p>
            ) : (
              comments.map((comment) => (
                <div key={comment.id} className="pb-4 border-b border-white/10 last:border-0">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[--primary-hot-pink] to-[--primary-pink-dark] flex items-center justify-center text-sm font-bold">
                        {comment.username.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <span className="font-semibold">{comment.username}</span>
                        {comment.is_edited && <span className="text-xs text-gray-500 ml-2">(edited)</span>}
                      </div>
                    </div>
                    <span className="text-sm text-gray-400">{new Date(comment.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-gray-300 ml-13">{comment.content}</p>

                  {/* Replies */}
                  {comment.replies && comment.replies.length > 0 && (
                    <div className="ml-13 mt-4 space-y-3 pl-4 border-l-2 border-[--primary-hot-pink]/30">
                      {comment.replies.map((reply) => (
                        <div key={reply.id}>
                          <div className="flex items-center gap-2 mb-1">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[--primary-hot-pink] to-[--primary-pink-dark] flex items-center justify-center text-xs font-bold">
                              {reply.username.charAt(0).toUpperCase()}
                            </div>
                            <span className="font-semibold text-sm">{reply.username}</span>
                            <span className="text-xs text-gray-500">{new Date(reply.created_at).toLocaleString()}</span>
                          </div>
                          <p className="text-gray-300 text-sm ml-10">{reply.content}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </GlassCard>

        {/* Video Modal */}
        {selectedVideo && (
          <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="w-full max-w-4xl">
              <div className="flex justify-end mb-4">
                <button
                  onClick={() => setSelectedVideo(null)}
                  className="text-white text-3xl hover:text-[--primary-hot-pink]"
                >
                  ×
                </button>
              </div>
              <video src={selectedVideo} controls autoPlay className="w-full rounded-lg" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
