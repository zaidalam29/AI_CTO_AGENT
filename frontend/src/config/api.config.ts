// src/config/api.config.ts
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: Number(process.env.NEXT_PUBLIC_API_TIMEOUT) || 120000,
  retryAttempts: 3,
  retryDelay: 1000,
  
  endpoints: {
    analyze: '/api/v1/projects/analyze',
    health: '/api/v1/projects/health',
    metrics: '/api/v1/projects/metrics',
    agents: '/api/v1/projects/agents',
    agent: (name: string) => `/api/v1/projects/agent/${name}`,
    config: '/api/v1/projects/config',
    ping: '/api/v1/projects/ping',
  },
  
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
};

export const RATE_LIMIT = {
  requests: Number(process.env.NEXT_PUBLIC_RATE_LIMIT_REQUESTS) || 10,
  window: Number(process.env.NEXT_PUBLIC_RATE_LIMIT_WINDOW) || 60000,
};

export const VALIDATION = {
  minRequirementsLength: Number(process.env.NEXT_PUBLIC_MIN_REQUIREMENTS_LENGTH) || 10,
  maxRequirementsLength: Number(process.env.NEXT_PUBLIC_MAX_REQUIREMENTS_LENGTH) || 10000,
  minProjectNameLength: 3,
  maxProjectNameLength: 100,
};