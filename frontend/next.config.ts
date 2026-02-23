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
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; connect-src 'self' http://localhost:8000 https://localhost:8000;".replace(/\s+/g, ' ').trim(),
          },
        ],
      },
    ];
  },

  // Rewrites with increased timeouts
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
        // Add timeout configuration
        has: [],
        missing: [],
      },
    ];
  },

  // Increase server timeout
  serverRuntimeConfig: {
    // This will be merged with the default config
    api: {
      bodyParser: {
        sizeLimit: '10mb',
      },
      responseLimit: false,
    },
  },

  // Increase timeout for API routes
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
    serverComponentsExternalPackages: ['axios'],
    // Increase proxy timeout
    proxyTimeout: 120000, // 2 minutes
  },

  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? {
      exclude: ['error', 'warn'],
    } : false,
  },

  output: 'standalone',
  generateEtags: true,
  compress: true,
  trailingSlash: false,
  assetPrefix: process.env.ASSET_PREFIX || '',
  poweredByHeader: false,
};

export default nextConfig;