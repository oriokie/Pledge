'use client';

import { ReactNode } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { cn } from '@/lib/utils';

interface LayoutProps {
  children: ReactNode;
  className?: string;
}

export default function Layout({ children, className }: LayoutProps) {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main
          className={cn(
            'flex-1 overflow-y-auto bg-gray-100 p-6 dark:bg-gray-900',
            className
          )}
        >
          {children}
        </main>
      </div>
    </div>
  );
} 