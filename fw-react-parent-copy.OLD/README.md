# Family Wallet - Frontend

React + TypeScript frontend for Family Wallet Telegram Mini App.

## 🚀 Tech Stack

- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Routing:** React Router v6
- **State Management:** Zustand + TanStack React Query
- **Animations:** Framer Motion + Canvas Confetti
- **Icons:** Lucide React
- **HTTP Client:** Axios
- **Validation:** Zod
- **Telegram:** @telegram-apps/sdk

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                  # App-level configuration
│   │   ├── providers/        # Context providers
│   │   ├── App.tsx          # Main app component
│   │   └── Router.tsx       # Route configuration
│   ├── features/            # Feature-based modules
│   │   ├── auth/           # Authentication
│   │   ├── wallet/         # Child wallet view
│   │   ├── tasks/          # Tasks management
│   │   ├── rewards/        # Rewards catalog
│   │   ├── admin/          # Parent dashboard
│   │   └── goals/          # Savings goals
│   ├── shared/             # Shared resources
│   │   ├── ui/            # Reusable UI components
│   │   ├── hooks/         # Custom hooks
│   │   ├── utils/         # Utility functions
│   │   └── types/         # TypeScript types
│   └── assets/            # Static assets
└── public/                # Public files
```

## 🛠️ Development

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see ../backend/README.md)

### Installation

```bash
npm install
```

### Environment Setup

Copy `.env.example` to `.env.local` and configure:

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
VITE_API_URL=http://localhost:8787
```

### Running Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 🎨 Design System

### Colors (Neon Family Theme)

```css
/* Base */
--bg-primary: #0a0a0f
--bg-card: #1a1a2e
--bg-elevated: #16213e

/* Neon Accents */
--neon-cyan: #00f5ff
--neon-pink: #ff006e
--neon-purple: #8338ec
--neon-green: #06ffa5
```

### Typography

- Font: Inter
- Balance display: 48px (extra bold)
- Headings: 24px - 32px (bold)
- Body: 16px (regular/medium)
- Small: 12px - 14px

### Components

All components use Tailwind CSS with custom utilities:
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.input-field` - Form inputs
- `.card-hover` - Hoverable cards with scale effect
- `.neon-glow` - Neon glow effect

## 🔌 API Integration

### Authentication

All API requests automatically include Telegram WebApp initData:

```typescript
headers: {
  'x-telegram-init-data': window.Telegram.WebApp.initData
}
```

### API Client

Uses Axios with interceptors for auth and error handling.

```typescript
import apiClient from '@/shared/utils/api';

// Example usage
const data = await apiClient.get('/api/endpoint');
```

### React Query

All API calls use TanStack React Query for caching and state management:

```typescript
const { data, isLoading } = useQuery({
  queryKey: ['key'],
  queryFn: () => apiClient.get('/endpoint')
});
```

## 🎭 User Modes

### Child Mode

- Wallet dashboard with balance
- Available tasks list
- Rewards catalog
- Transaction history
- Savings goals (v1)

### Parent Mode

- Family dashboard
- Children management
- Task creation and moderation
- Reward management
- Purchase approval
- Transaction history

## ✨ Animations

### Balance Count-Up

Uses `react-countup` for number animations when balance changes.

### Confetti

Canvas confetti triggers on:
- Earning coins
- Task completion approval
- Purchase approval

### Transitions

Framer Motion for:
- Modal animations
- Page transitions
- Card hover effects

## 🧪 Testing

```bash
# Run tests (when implemented)
npm test

# Type check
npm run type-check

# Lint
npm run lint
```

## 📱 Telegram Mini App

### Integration

The app uses Telegram WebApp SDK for:
- User authentication
- Haptic feedback
- Theme colors
- Main/Back buttons
- Alerts and confirmations

### Development Testing

For testing outside Telegram:
1. Mock Telegram WebApp object
2. Use browser DevTools mobile view
3. Test with actual Telegram Bot (recommended)

## 🚀 Deployment

### Cloudflare Pages

```bash
# Build
npm run build

# Deploy
npx wrangler pages deploy dist
```

Configuration:
- Build command: `npm run build`
- Build output: `dist`
- Node version: 18+

## 📄 License

Private - Family Wallet Project

## 👥 Contributors

Family Wallet Team
