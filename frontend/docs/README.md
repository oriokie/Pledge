# Frontend Documentation

## Overview
The frontend of the Pledge application is built using Next.js, React, and TypeScript. It features a modern, responsive design with a focus on user experience and performance.

## Core Components

### Dashboard

#### Dashboard Page (`/app/dashboard/page.tsx`)
The main dashboard page provides a customizable interface for displaying various widgets and analytics.

**Features:**
- Customizable widget layout
- Date range filtering
- Persistent widget configuration
- Real-time data updates
- Responsive grid layout

**Widgets:**
1. Contribution Trends
   - Displays contribution data over time
   - Supports date range filtering
   - Visualizes trends using area charts

2. Member Distribution
   - Shows member distribution across groups
   - Interactive chart visualization
   - Real-time data updates

3. Top Contributors
   - Lists top contributing members
   - Displays contribution amounts
   - Updates based on selected date range

4. Upcoming Events
   - Shows scheduled events
   - Displays event details and dates
   - Real-time updates

### Components

#### DateRangeSelector (`/components/dashboard/DateRangeSelector.tsx`)
A reusable component for selecting date ranges with preset options.

**Props:**
```typescript
interface DateRangeSelectorProps {
  onChange: (range: DateRange) => void;
  className?: string;
}
```

**Features:**
- Preset date range options (7, 30, 90, 365 days)
- Custom date range selection
- Responsive design
- Dark mode support

#### DashboardCustomizer (`/components/dashboard/DashboardCustomizer.tsx`)
A component for customizing the dashboard layout and widget settings.

**Props:**
```typescript
interface DashboardCustomizerProps {
  widgets: WidgetConfig[];
  onWidgetsChange: (widgets: WidgetConfig[]) => void;
}
```

**Features:**
- Drag and drop widget reordering
- Widget visibility toggle
- Widget size customization
- Persistent layout settings

### API Integration

#### Custom Hooks

##### useApiQuery
A custom hook for handling API queries with React Query.

```typescript
interface QueryConfig<TData = unknown> {
  queryKey: unknown[];
  queryFn: () => Promise<TData>;
  options?: Omit<UseQueryOptions<TData, Error>, 'queryKey' | 'queryFn'>;
}
```

**Features:**
- Automatic error handling
- Caching
- Loading states
- Type safety

##### useApiMutation
A custom hook for handling API mutations.

```typescript
interface MutationConfig<T, V> {
  mutationFn: (variables: V) => Promise<T>;
  options?: Omit<UseMutationOptions<T, APIError, V>, 'mutationFn'>;
}
```

**Features:**
- Optimistic updates
- Error handling
- Loading states
- Type safety

## State Management

### Local Storage
The application uses localStorage for persisting user preferences:
- Dashboard widget configuration
- User settings
- UI preferences

### React Query
Used for server state management:
- Automatic caching
- Background updates
- Optimistic updates
- Error handling

## Styling

### Tailwind CSS
The application uses Tailwind CSS for styling with:
- Responsive design
- Dark mode support
- Custom color schemes
- Utility-first approach

### Component Library
Custom UI components built on top of Tailwind CSS:
- Button
- Card
- Input
- Select
- Modal
- Toast

## Error Handling

### API Error Handling
Centralized error handling for API calls:
- Network errors
- Validation errors
- Server errors
- User-friendly error messages

### Error Boundaries
React Error Boundaries for graceful error handling:
- Component-level error catching
- Fallback UI
- Error reporting

## Performance Optimization

### Code Splitting
- Dynamic imports for large components
- Route-based code splitting
- Lazy loading of non-critical components

### Caching
- API response caching with React Query
- Static page generation where applicable
- Image optimization

## Accessibility

### ARIA Attributes
- Proper heading hierarchy
- Descriptive labels
- Keyboard navigation
- Screen reader support

### Color Contrast
- WCAG 2.1 compliant color schemes
- Dark mode support
- High contrast mode

## Development Guidelines

### Code Style
- TypeScript for type safety
- ESLint for code quality
- Prettier for code formatting
- Consistent naming conventions

### Component Structure
- Functional components with hooks
- Props interface definitions
- Clear component hierarchy
- Reusable components

### Testing
- Unit tests for components
- Integration tests for features
- E2E tests for critical paths
- Accessibility testing

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn
- Git

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables
Create a `.env.local` file with:
```
NEXT_PUBLIC_API_URL=your_api_url
```

### Available Scripts
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint
- `npm run test`: Run tests

## Contributing

### Development Workflow
1. Create feature branch
2. Make changes
3. Write tests
4. Submit pull request
5. Code review
6. Merge

### Code Review Guidelines
- Type safety
- Component reusability
- Performance considerations
- Accessibility compliance
- Test coverage

## Deployment

### Build Process
1. Environment setup
2. Dependency installation
3. Type checking
4. Linting
5. Testing
6. Build
7. Deployment

### Deployment Platforms
- Vercel (recommended)
- Netlify
- AWS
- Custom server 