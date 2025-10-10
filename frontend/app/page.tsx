import Link from "next/link";
import GlassButton from "@/components/ui/GlassButton";
import GlassCard from "@/components/ui/GlassCard";

export default function Home() {
  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col gap-24">
        {/* Hero Section - Centered */}
        <section className="relative w-full">
          {/* Decorative background elements */}
          <div className="absolute top-20 -left-20 w-72 h-72 bg-[--primary-hot-pink] rounded-full opacity-10 blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 -right-20 w-96 h-96 bg-[--primary-pink-light] rounded-full opacity-10 blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>

          <div className="relative z-10 text-center space-y-8">
            <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold leading-tight">
              <span className="accent-pink drop-shadow-lg">Louis</span>
              <span className="text-white"> Slutton</span>
            </h1>

            <p className="text-2xl sm:text-3xl md:text-4xl text-gray-200 font-light tracking-wide">
              Where Pleasure Meets Luxury
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <p className="text-base md:text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
              Discover our exquisite collection of adult novelty products and games,
              carefully curated to elevate your intimate experiences to new heights.
            </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link href="/products" className="w-full sm:w-auto">
                <GlassButton className="text-base px-10 py-4 w-full sm:w-auto">
                  Shop Now
                </GlassButton>
              </Link>
              <Link href="/categories" className="w-full sm:w-auto">
                <GlassButton variant="secondary" className="text-base px-10 py-4 w-full sm:w-auto">
                  Browse Categories
                </GlassButton>
              </Link>
              <Link href="/games" className="w-full sm:w-auto">
                <GlassButton variant="secondary" className="text-base px-10 py-4 w-full sm:w-auto">
                  Games
                </GlassButton>
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section - Centered with MORE spacing */}
        <section className="w-full space-y-12">
          <div className="text-center space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold">
              Why Choose <span className="accent-pink">Louis Slutton</span>?
            </h2>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <p className="text-gray-400 max-w-2xl mx-auto">
              Experience the difference with our commitment to quality, privacy, and customer satisfaction
            </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <GlassCard className="p-8 text-center space-y-4">
              <div className="text-6xl accent-pink">✨</div>
              <h3 className="text-xl font-bold">Premium Quality</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Handpicked products from the world's finest brands, ensuring excellence in every detail
              </p>
            </GlassCard>

            <GlassCard className="p-8 text-center space-y-4">
              <div className="text-6xl accent-pink">🔒</div>
              <h3 className="text-xl font-bold">Discreet Shipping</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Your privacy is our priority with secure, unmarked packaging and confidential delivery
              </p>
            </GlassCard>

            <GlassCard className="p-8 text-center space-y-4">
              <div className="text-6xl accent-pink">💳</div>
              <h3 className="text-xl font-bold">Secure Checkout</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Shop with confidence using our encrypted payment system powered by Stripe
              </p>
            </GlassCard>
          </div>
        </section>

        {/* CTA Section - Centered */}
        <section className="w-full">
          <GlassCard className="max-w-3xl mx-auto p-12 text-center space-y-8">
            <h2 className="text-3xl md:text-4xl font-bold">
              Ready to Explore?
            </h2>
            <p className="text-lg md:text-xl text-gray-300 leading-relaxed">
              Join thousands of satisfied customers discovering pleasure redefined
            </p>
            <div>
              <Link href="/register">
                <GlassButton className="text-base md:text-lg px-12 py-4">
                  Create Your Account
                </GlassButton>
              </Link>
            </div>

            {/* Age Warning */}
            <div className="pt-6 border-t border-gray-700">
              <p className="text-gray-500 text-xs md:text-sm flex flex-col sm:flex-row items-center justify-center gap-2">
                <span className="text-base">⚠️</span>
                <span>Must be 18 years or older to purchase. Age verification required.</span>
              </p>
            </div>
          </GlassCard>
        </section>
      </div>
    </div>
  );
}
