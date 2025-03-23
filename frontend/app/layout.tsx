'use client';

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { MainLayout } from "@/components/layout/main-layout";
import { QueryClientProvider } from '@tanstack/react-query';
import { ToastProvider } from '@/contexts/ToastContext';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { queryClient } from '@/lib/queryClient';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Pledge - Church Management System",
  description: "A modern church management system for handling contributions and pledges",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorBoundary>
          <QueryClientProvider client={queryClient}>
            <ToastProvider>
              <MainLayout>{children}</MainLayout>
            </ToastProvider>
          </QueryClientProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
} 