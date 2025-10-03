export default function Footer() {
  return (
    <footer className="glass-card rounded-none border-x-0 border-b-0 mt-auto backdrop-blur-xl">
      <div className="container mx-auto px-4 md:px-8 py-8 md:py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-2xl font-bold mb-4">
              <span className="accent-pink">Louis</span> Slutton
            </h3>
            <p className="text-gray-400 leading-relaxed">
              Your premier destination for adult novelty products and games. Elevating pleasure since 2025.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4 text-lg">Quick Links</h4>
            <ul className="space-y-3 text-gray-400">
              <li><a href="/products" className="hover:text-[--primary-hot-pink] transition-colors">Products</a></li>
              <li><a href="/categories" className="hover:text-[--primary-hot-pink] transition-colors">Categories</a></li>
              <li><a href="/about" className="hover:text-[--primary-hot-pink] transition-colors">About Us</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4 text-lg">Legal</h4>
            <ul className="space-y-3 text-gray-400">
              <li><a href="/privacy" className="hover:text-[--primary-hot-pink] transition-colors">Privacy Policy</a></li>
              <li><a href="/terms" className="hover:text-[--primary-hot-pink] transition-colors">Terms of Service</a></li>
              <li><a href="/shipping" className="hover:text-[--primary-hot-pink] transition-colors">Shipping & Returns</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-800 text-center text-gray-400">
          <p className="text-sm">&copy; 2025 Louis Slutton. All rights reserved. Must be 18+ to purchase.</p>
        </div>
      </div>
    </footer>
  );
}
