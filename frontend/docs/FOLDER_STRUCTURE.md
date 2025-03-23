# Frontend Folder Structure Documentation

## Root Directory Structure

```
frontend/
├── app/                    # Next.js 13+ App Router pages and layouts
├── components/            # Reusable React components
├── contexts/             # React Context providers
├── docs/                 # Documentation files
├── lib/                  # Utility functions and shared code
├── public/              # Static assets
├── styles/              # Global styles and Tailwind configuration
└── types/               # TypeScript type definitions
```

## Detailed Folder Documentation

### `/app` Directory
The main application directory using Next.js 13+ App Router.

```
app/
├── (auth)/              # Authentication-related pages
│   ├── login/          # Login page and components
│   └── register/       # Registration page and components
├── dashboard/          # Dashboard pages and components
├── members/           # Member management pages
├── projects/          # Project management pages
├── settings/          # User settings pages
├── layout.tsx         # Root layout component
└── page.tsx           # Home page
```

**Key Files:**
- `layout.tsx`: Root layout with providers and global styles
- `page.tsx`: Home page component
- `loading.tsx`: Loading state components
- `error.tsx`: Error boundary components

### `/components` Directory
Reusable React components organized by feature and type.

```
components/
├── dashboard/          # Dashboard-specific components
│   ├── ContributionTrends.tsx
│   ├── DateRangeSelector.tsx
│   ├── DashboardCustomizer.tsx
│   ├── MemberDistribution.tsx
│   ├── ProjectProgress.tsx
│   ├── TopContributors.tsx
│   └── UpcomingEvents.tsx
├── layout/            # Layout components
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   └── Footer.tsx
├── members/           # Member-related components
│   ├── MemberCard.tsx
│   ├── MemberForm.tsx
│   └── MemberList.tsx
├── projects/          # Project-related components
│   ├── ProjectCard.tsx
│   ├── ProjectForm.tsx
│   └── ProjectList.tsx
└── ui/                # Base UI components
    ├── Button.tsx
    ├── Card.tsx
    ├── Input.tsx
    ├── Modal.tsx
    ├── Select.tsx
    └── Toast.tsx
```

### `/contexts` Directory
React Context providers for global state management.

```
contexts/
├── AuthContext.tsx    # Authentication state
├── ThemeContext.tsx   # Theme preferences
└── ToastContext.tsx   # Toast notifications
```

### `/lib` Directory
Utility functions, API clients, and shared code.

```
lib/
├── api/               # API integration
│   ├── contributions.ts
│   ├── events.ts
│   ├── members.ts
│   ├── projects.ts
│   └── error.ts
├── hooks/             # Custom React hooks
│   ├── useApiQuery.ts
│   └── useApiMutation.ts
└── utils/             # Utility functions
    ├── date.ts
    ├── format.ts
    └── validation.ts
```

### `/public` Directory
Static assets served by Next.js.

```
public/
├── images/            # Image assets
├── icons/             # Icon assets
└── fonts/             # Custom fonts
```

### `/styles` Directory
Global styles and Tailwind CSS configuration.

```
styles/
├── globals.css        # Global styles
└── tailwind.config.js # Tailwind configuration
```

### `/types` Directory
TypeScript type definitions and interfaces.

```
types/
├── api.ts            # API-related types
├── components.ts     # Component prop types
└── models.ts         # Data model types
```

## Component Documentation

### Dashboard Components

#### `ContributionTrends.tsx`
Displays contribution data trends using area charts.

**Props:**
```typescript
interface ContributionTrendsProps {
  data?: Array<{
    date: string;
    amount: number;
    count: number;
  }>;
  isLoading?: boolean;
}
```

#### `DateRangeSelector.tsx`
Date range selection component with preset options.

**Props:**
```typescript
interface DateRangeSelectorProps {
  onChange: (range: DateRange) => void;
  className?: string;
}
```

#### `DashboardCustomizer.tsx`
Dashboard layout customization component.

**Props:**
```typescript
interface DashboardCustomizerProps {
  widgets: WidgetConfig[];
  onWidgetsChange: (widgets: WidgetConfig[]) => void;
}
```

### UI Components

#### `Button.tsx`
Reusable button component with variants.

**Props:**
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}
```

#### `Card.tsx`
Container component for content sections.

**Props:**
```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
}
```

## API Integration

### API Client Structure

```typescript
// Example API client structure
const api = {
  contributions: {
    getAll: () => fetch('/api/contributions'),
    getById: (id: string) => fetch(`/api/contributions/${id}`),
    create: (data: ContributionCreateInput) => 
      fetch('/api/contributions', { method: 'POST', body: JSON.stringify(data) }),
  },
  // ... other API endpoints
};
```

### Error Handling

```typescript
// Example error handling
const handleAPIError = (error: unknown) => {
  if (error instanceof APIError) {
    // Handle specific API errors
  } else {
    // Handle generic errors
  }
};
```

## State Management

### Context Usage

```typescript
// Example context usage
const { user, login, logout } = useAuth();
const { theme, toggleTheme } = useTheme();
const { showToast } = useToast();
```

### Local Storage

```typescript
// Example localStorage usage
const saveWidgetConfig = (config: WidgetConfig[]) => {
  localStorage.setItem('dashboard-widgets', JSON.stringify(config));
};

const loadWidgetConfig = () => {
  const saved = localStorage.getItem('dashboard-widgets');
  return saved ? JSON.parse(saved) : defaultWidgets;
};
```

## Styling Guidelines

### Tailwind Classes

```typescript
// Example component with Tailwind classes
const Card = ({ children, className }: CardProps) => (
  <div className={cn(
    'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
    'dark:border-gray-700 dark:bg-gray-800',
    className
  )}>
    {children}
  </div>
);
```

### Dark Mode Support

```typescript
// Example dark mode class usage
const Button = ({ children, variant }: ButtonProps) => (
  <button className={cn(
    'rounded-md px-4 py-2',
    variant === 'primary' && 'bg-indigo-600 text-white hover:bg-indigo-700',
    variant === 'outline' && 'border border-gray-300 hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-700',
  )}>
    {children}
  </button>
);
``` 