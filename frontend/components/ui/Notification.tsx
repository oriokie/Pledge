'use client';

import { Fragment } from 'react';
import { Transition } from '@headlessui/react';
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  XCircleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface NotificationProps {
  type: NotificationType;
  title: string;
  message: string;
  isOpen: boolean;
  onClose: () => void;
  duration?: number;
}

const icons = {
  success: CheckCircleIcon,
  error: XCircleIcon,
  warning: ExclamationCircleIcon,
  info: InformationCircleIcon,
};

const colors = {
  success: {
    bg: 'bg-green-50 dark:bg-green-900/50',
    text: 'text-green-800 dark:text-green-200',
    icon: 'text-green-400',
  },
  error: {
    bg: 'bg-red-50 dark:bg-red-900/50',
    text: 'text-red-800 dark:text-red-200',
    icon: 'text-red-400',
  },
  warning: {
    bg: 'bg-yellow-50 dark:bg-yellow-900/50',
    text: 'text-yellow-800 dark:text-yellow-200',
    icon: 'text-yellow-400',
  },
  info: {
    bg: 'bg-blue-50 dark:bg-blue-900/50',
    text: 'text-blue-800 dark:text-blue-200',
    icon: 'text-blue-400',
  },
};

export default function Notification({
  type,
  title,
  message,
  isOpen,
  onClose,
  duration = 5000,
}: NotificationProps) {
  const Icon = icons[type];
  const colorScheme = colors[type];

  // Auto-close after duration
  React.useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isOpen, duration, onClose]);

  return (
    <div
      aria-live="assertive"
      className="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6"
    >
      <div className="flex w-full flex-col items-center space-y-4 sm:items-end">
        <Transition
          show={isOpen}
          as={Fragment}
          enter="transform ease-out duration-300 transition"
          enterFrom="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
          enterTo="translate-y-0 opacity-100 sm:translate-x-0"
          leave="transition ease-in duration-100"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div
            className={`pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 ${colorScheme.bg}`}
          >
            <div className="p-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <Icon className={`h-6 w-6 ${colorScheme.icon}`} aria-hidden="true" />
                </div>
                <div className="ml-3 w-0 flex-1 pt-0.5">
                  <p className={`text-sm font-medium ${colorScheme.text}`}>
                    {title}
                  </p>
                  <p className={`mt-1 text-sm ${colorScheme.text}`}>
                    {message}
                  </p>
                </div>
                <div className="ml-4 flex flex-shrink-0">
                  <button
                    type="button"
                    className="inline-flex rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:hover:text-gray-300"
                    onClick={onClose}
                  >
                    <span className="sr-only">Close</span>
                    <XMarkIcon className="h-5 w-5" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  );
} 