import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { Toaster } from 'react-hot-toast';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Louis Slutton - Adult Novelty Products",
  description: "Your premier destination for adult novelty products and games",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}
      >
        <Header />
        <main className="flex-1 w-full" style={{ marginTop: '80px' }}>
          {children}
        </main>
        <Footer />
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: 'rgba(255, 20, 147, 0.1)',
              backdropFilter: 'blur(16px)',
              border: '1px solid rgba(255, 20, 147, 0.2)',
              color: '#fff',
            },
          }}
        />
      </body>
    </html>
  );
}
