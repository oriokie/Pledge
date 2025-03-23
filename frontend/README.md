# Pledge Frontend

A modern, responsive frontend for the Pledge church management system built with Next.js, Tailwind CSS, and TypeScript.

## Features

- 🎨 Modern and responsive design
- 🌙 Dark mode support
- 📱 Mobile-first approach
- ⚡ Fast page loads with Next.js
- 🎯 Type-safe development with TypeScript
- 🎭 Beautiful UI components with Tailwind CSS
- 📊 Interactive charts and data visualization
- 🔒 Secure authentication
- 🌐 Internationalization ready

## Pages

### Dashboard
- Overview of key metrics
- Contribution trends
- Recent activity
- Project progress

### Members
- Member management
- Search and filter functionality
- Member details and history
- Status tracking

### Contributions
- Contribution tracking
- Filtering by status
- Detailed contribution history
- Group-based contributions

### Projects
- Project management
- Progress tracking
- Fundraising goals
- Member participation

### Settings
- User preferences
- System configuration
- Backup and restore
- Security settings

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pledge.git
cd pledge/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
# or
yarn build
```

```bash
npm start
# or
yarn start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── dashboard/         # Dashboard page
│   ├── members/          # Members management
│   ├── contributions/    # Contributions tracking
│   ├── projects/        # Project management
│   └── settings/        # Settings and configuration
├── components/           # Reusable components
│   ├── layout/          # Layout components
│   └── ui/              # UI components
├── lib/                  # Utility functions and hooks
├── styles/              # Global styles
└── types/               # TypeScript type definitions
```

## Technologies Used

- [Next.js](https://nextjs.org/) - React framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [Heroicons](https://heroicons.com/) - Beautiful icons
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Recharts](https://recharts.org/) - Charting library
- [React Hook Form](https://react-hook-form.com/) - Form handling
- [Zod](https://zod.dev/) - Schema validation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) 