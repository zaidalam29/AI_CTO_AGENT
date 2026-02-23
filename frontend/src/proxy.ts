// src/proxy.ts - Fix export name
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Rate limiting store
const rateLimit = new Map<string, { count: number; timestamp: number }>();

// 👇 FUNCTION NAME MUST BE 'proxy' (not 'middleware')
export function proxy(request: NextRequest) {
  const response = NextResponse.next();
  
  // Add security headers
  const securityHeaders = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; font-src 'self' data: https:; img-src 'self' data: https:;",
  };

  Object.entries(securityHeaders).forEach(([key, value]) => {
    response.headers.set(key, value);
  });

  // Rate limiting for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const ip = request.ip ?? 'unknown';
    const now = Date.now();
    const windowMs = 60000;
    const maxRequests = 60;

    const userRate = rateLimit.get(ip) || { count: 0, timestamp: now };

    if (now - userRate.timestamp > windowMs) {
      userRate.count = 1;
      userRate.timestamp = now;
    } else {
      userRate.count++;
    }

    rateLimit.set(ip, userRate);

    if (userRate.count > maxRequests) {
      return new NextResponse('Too Many Requests', { status: 429 });
    }

    response.headers.set('X-RateLimit-Limit', maxRequests.toString());
    response.headers.set('X-RateLimit-Remaining', (maxRequests - userRate.count).toString());
  }

  return response;
}

export const config = {
  matcher: '/:path*',
};