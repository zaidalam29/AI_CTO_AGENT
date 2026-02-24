import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '3000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'backend',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()',
          },
        ],
      },
    ];
  },

  // Rewrites
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },

  // ✅ Next.js 16.1.6 - valid options
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
    // serverComponentsExternalPackages: ['axios'],  // ❌ Ye nahi chalega
    // proxyTimeout: 120000,  // ❌ Ye bhi nahi chalega
  },

  // ✅ Next.js 16.1.6 - valid root options
  output: 'standalone',
  poweredByHeader: false,
  trailingSlash: false,
  compress: true,
  generateEtags: true,
  
  // Agar inhe use karna hai to is tarah use karo:
  // serverExternalPackages abhi support nahi hai 16.1.6 mein
  // proxyTimeout abhi support nahi hai
};

export default nextConfig;