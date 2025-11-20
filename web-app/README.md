# Financial Analysis Tool - Frontend

React 18+ frontend application with Material-UI for the Financial Analysis Tool.

## Tech Stack

- **React 18.3+** - UI framework
- **TypeScript 5+** - Type safety
- **Vite** - Build tool and dev server
- **Material-UI (MUI) v5** - UI component library
- **React Router v6** - Client-side routing
- **TanStack Query (React Query)** - Server state management
- **Axios** - HTTP client
- **Recharts** - Charting library
- **React Hook Form** - Form management
- **date-fns** - Date utilities

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server (runs on http://localhost:5173)
npm run dev
```

The dev server includes a proxy configuration that forwards `/api` requests to the backend at `http://localhost:8000`.

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Linting

```bash
# Run ESLint
npm run lint
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   ├── components/     # React components
│   │   ├── common/     # Shared components (Layout, Header, Sidebar)
│   │   ├── Dashboard/  # Dashboard components
│   │   ├── Transactions/ # Transaction management
│   │   ├── Analysis/   # Analysis and reports
│   │   ├── Projections/ # Forecasting
│   │   ├── Classifications/ # Classification management
│   │   └── Settings/   # Settings
│   ├── contexts/       # React contexts
│   ├── hooks/          # Custom React hooks
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── styles/         # Global styles
│   ├── theme.ts        # Material-UI theme configuration
│   ├── App.tsx         # Root component
│   └── main.tsx        # Application entry point
├── index.html          # HTML template
├── vite.config.ts      # Vite configuration
├── tsconfig.json       # TypeScript configuration
└── package.json        # Dependencies and scripts
```

## Features

### Phase 4: Frontend Foundation (Current)

- ✅ React project setup with Vite and TypeScript
- ✅ Material-UI theme and styling
- ✅ React Router navigation
- ✅ React Query for API state management
- ✅ Application layout (header, sidebar, main content)
- ✅ Basic Dashboard component
- ✅ Basic Transaction List component
- ✅ Loading states and error handling components
- ✅ Responsive design foundation

### Upcoming Features

- Transaction filtering and detail views
- Charts and visualizations with Recharts
- Analysis and reporting interfaces
- Import functionality
- Classification management
- Projections and forecasting

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api`. The Vite dev server proxies API requests to avoid CORS issues during development.

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000/api
```

## Development Guidelines

- Use TypeScript for all new files
- Follow Material-UI design patterns
- Use React Query for server state
- Use React Hook Form for forms
- Keep components small and focused
- Write reusable components in `components/common/`
- Define types in `types/` directory

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Private project

