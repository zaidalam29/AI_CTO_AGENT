import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const rateLimit = new Map<string, { count: number; timestamp: number }>();

export function proxy(request: NextRequest) {
  const response = NextResponse.next();
  
  const securityHeaders = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  };

  Object.entries(securityHeaders).forEach(([key, value]) => {
    response.headers.set(key, value);
  });

  // Rate limiting for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {

    const ip = request.headers.get('x-forwarded-for')?.split(',')[0] ?? 
               request.headers.get('x-real-ip') ?? 
               'unknown';
    
    const now = Date.now();
    const windowMs = 60000; // 1 minute
    const maxRequests = 60;

    const userRate = rateLimit.get(ip) || { count: 0, timestamp: now };

    if (now - userRate.timestamp > windowMs) {
      // Reset window
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
  matcher: '/api/:path*',
};