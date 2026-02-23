# 🚀 AI CTO Agent - Frontend

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-cyan)
![License](https://img.shields.io/badge/license-MIT-red)

**Modern Next.js frontend for AI CTO Agent - Your Artificial Intelligence Chief Technology Officer**

[Features](#-features) • [Quick Start](#-quick-start) • [API Integration](#-api-integration) • [Security](#-security) • [Deployment](#-deployment)

</div>

---

## ✨ Features

### 🎨 **Modern UI/UX**
- Beautiful gradient designs
- Responsive layout (mobile, tablet, desktop)
- Smooth animations with Framer Motion
- Dark mode ready
- Loading skeletons and spinners

### 🤖 **AI Agent Integration**
- Real-time analysis with typing effect
- 6 specialized AI agents display
- Progress tracking with animations
- Agent status indicators
- Streaming text simulation

### 🛡️ **Security**
- Input sanitization
- XSS protection
- Rate limiting
- Security headers (CSP, X-Frame-Options, etc.)
- Environment variables
- Request validation

### 📊 **Features**
- Project form with validation
- Sweet alerts for errors
- Toast notifications
- Export analysis as JSON
- Share functionality
- Print support
- Copy to clipboard

### 📱 **Pages & Components**
- Landing page with hero section
- Project analysis form
- Loading animation
- Results display with tabs
- Agent status dashboard
- Metrics and stats

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend API running (AI CTO Agent backend)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-cto-frontend.git
cd ai-cto-frontend

# 2. Install dependencies
npm install

# 3. Copy environment variables
cp .env.example .env.local

# 4. Edit .env.local with your values
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 5. Run development server
npm run dev

# 6. Open browser
open http://localhost:3000
```

---

## 🔧 Environment Variables

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=120000
NEXT_PUBLIC_MAX_REQUIREMENTS_LENGTH=10000
NEXT_PUBLIC_MIN_REQUIREMENTS_LENGTH=10
NEXT_PUBLIC_APP_NAME="AI CTO Agent"
NEXT_PUBLIC_APP_VERSION="1.0.0"

# Security
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL=http://localhost:3000

# Rate Limiting
NEXT_PUBLIC_RATE_LIMIT_REQUESTS=10
NEXT_PUBLIC_RATE_LIMIT_WINDOW=60000

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=false
```

---

## 📁 Project Structure

```
ai-cto-frontend/
│
├── src/
│   ├── app/                    # Next.js app router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── globals.css         # Global styles
│   │
│   ├── components/              # React components
│   │   ├── project/             # Project-related
│   │   │   ├── ProjectForm.tsx
│   │   │   ├── ProjectResult.tsx
│   │   │   └── LoadingAnimation.tsx
│   │   ├── common/              # Shared components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   └── ui/                  # UI components
│   │       ├── Loader.tsx
│   │       └── TypingEffect.tsx
│   │
│   ├── services/                 # API services
│   │   ├── api.ts
│   │   └── projectService.ts
│   │
│   ├── hooks/                     # Custom hooks
│   │   ├── useProjectAnalysis.ts
│   │   └── useDebounce.ts
│   │
│   ├── utils/                      # Utilities
│   │   ├── validators.ts
│   │   └── formatters.ts
│   │
│   ├── types/                       # TypeScript types
│   │   └── project.types.ts
│   │
│   ├── config/                       # Configuration
│   │   └── api.config.ts
│   │
│   └── middleware.ts                  # Security middleware
│
├── public/                            # Static files
├── .env.local                         # Environment variables
├── next.config.js                      # Next.js config
├── tailwind.config.js                   # Tailwind config
└── package.json                         # Dependencies
```

---

## 🔌 API Integration

### Base URL
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/projects/analyze` | POST | Analyze project |
| `/api/v1/projects/health` | GET | Health check |
| `/api/v1/projects/metrics` | GET | Get metrics |
| `/api/v1/projects/agents` | GET | List agents |
| `/api/v1/projects/agent/{name}` | GET | Get agent info |
| `/api/v1/projects/config` | GET | Get config |
| `/api/v1/projects/ping` | GET | Ping test |

### API Service Example
```typescript
import api from '@/services/api';

// Analyze project
const result = await api.analyzeProject({
  name: "E-commerce Platform",
  requirements: "Build an e-commerce platform...",
  project_type: "web_app"
});

// Check health
const health = await api.healthCheck();

// Get metrics
const metrics = await api.getMetrics();
```

---

## 🛡️ Security Features

### 1. **Input Validation**
```typescript
// Sanitize user input
const sanitized = sanitizeInput(userInput);

// Validate form data
const { isValid, errors } = validateProjectRequest(formData);
```

### 2. **Security Headers**
```typescript
// Added automatically via middleware
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'...
```

### 3. **Rate Limiting**
```typescript
// 60 requests per minute per IP
if (userRate.count > maxRequests) {
  return new NextResponse('Too Many Requests', { status: 429 });
}
```

### 4. **Environment Variables**
```bash
# Never commit .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key
```

---

## 🎨 Styling

### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: { ... },
        secondary: { ... },
      },
      animation: {
        typing: 'typing 3.5s steps(40, end)',
        blink: 'blink 1s step-end infinite',
      },
    },
  },
};
```

### CSS Modules
```css
/* Custom animations */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse-slow {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

---

## 📱 Responsive Design

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

```typescript
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Content */}
</div>

// Responsive padding
<div className="px-4 sm:px-6 lg:px-8">
  {/* Content */}
</div>
```

---

## 🚦 State Management

### Custom Hook Example
```typescript
const {
  analyze,
  loading,
  progress,
  response,
  error,
  streamingText,
  cancelAnalysis,
  reset,
} = useProjectAnalysis();

// Use in component
<button onClick={() => analyze(formData)} disabled={loading}>
  {loading ? 'Analyzing...' : 'Analyze'}
</button>
```

---

## 🧪 Testing

```bash
# Run tests
npm test

# Run e2e tests
npm run test:e2e

# Check types
npm run type-check

# Lint
npm run lint
```

---

## 🚢 Deployment

### Build for Production
```bash
npm run build
npm start
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Vercel
```bash
# Deploy to Vercel
vercel --prod
```

### Environment Variables on Vercel
```
NEXT_PUBLIC_API_URL=https://your-backend.com
NEXTAUTH_SECRET=your-secret
```

---

## 📊 Performance Optimization

- Image optimization with Next.js Image
- Code splitting
- Lazy loading components
- Memoization with React.memo
- Debounced inputs
- Progressive loading

---

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| API connection refused | Check if backend is running on port 8000 |
| CORS errors | Add CORS middleware in backend |
| Build errors | Run `npm install` again |
| Environment variables | Copy `.env.example` to `.env.local` |
| Rate limiting | Wait 1 minute before next request |

---

## 📈 Performance Metrics

- **First Contentful Paint**: < 1s
- **Time to Interactive**: < 2s
- **Lighthouse Score**: 95+
- **Bundle Size**: < 200KB (gzipped)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

### Development Guidelines
- Use TypeScript
- Add comments for complex logic
- Write tests
- Update documentation
- Follow ESLint rules

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Next.js team for amazing framework
- Tailwind CSS for utility-first CSS
- Framer Motion for animations
- React Hot Toast for notifications
- SweetAlert2 for beautiful alerts

---

## 📞 Support

- 📧 Email: support@aictoagent.com
- 💬 Discord: [Join server](https://discord.gg/aictoagent)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-cto-frontend/issues)

---

<div align="center">
  
**Made with ❤️ for developers**

</div>