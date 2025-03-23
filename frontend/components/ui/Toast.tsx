'use client';

import { useEffect, useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { cn } from '@/lib/utils';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastProps {
  message: string;
  type: ToastType;
  duration?: number;
  onClose: () => void;
}

const toastStyles = {
  success: 'bg-green-50 text-green-800 dark:bg-green-900 dark:text-green-200',
  error: 'bg-red-50 text-red-800 dark:bg-red-900 dark:text-red-200',
  info: 'bg-blue-50 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  warning: 'bg-yellow-50 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
};

export function Toast({ message, type, duration = 5000, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 300); // Wait for fade out animation
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div
      className={cn(
        'fixed bottom-4 right-4 z-50 rounded-lg p-4 shadow-lg transition-all duration-300',
        toastStyles[type],
        isVisible ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'
      )}
    >
      <div className="flex items-center space-x-2">
        <p className="text-sm font-medium">{message}</p>
        <button
          onClick={() => {
            setIsVisible(false);
            setTimeout(onClose, 300);
          }}
          className="ml-2 rounded-full p-1 hover:bg-black/10 dark:hover:bg-white/10"
        >
          <XMarkIcon className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
} 