'use client';

import { Fragment, useState } from 'react';
import { Menu, Transition } from '@headlessui/react';
import {
  BellIcon,
  SunIcon,
  MoonIcon,
  UserCircleIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '@/contexts/AuthContext';
import { cn } from '@/lib/utils';

interface HeaderProps {
  className?: string;
}

export default function Header({ className }: HeaderProps) {
  const { user, logout } = useAuth();
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <header
      className={cn(
        'flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 dark:border-gray-700 dark:bg-gray-800',
        className
      )}
    >
      <div className="flex items-center">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
          Pledge
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-700"
        >
          {isDarkMode ? (
            <SunIcon className="h-5 w-5" />
          ) : (
            <MoonIcon className="h-5 w-5" />
          )}
        </button>

        <button className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-700">
          <BellIcon className="h-5 w-5" />
        </button>

        <Menu as="div" className="relative">
          <Menu.Button className="flex items-center rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:bg-gray-800">
            <span className="sr-only">Open user menu</span>
            <UserCircleIcon className="h-8 w-8 text-gray-400" />
          </Menu.Button>

          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800">
              <Menu.Item>
                {({ active }) => (
                  <div className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300">
                    {user?.name}
                  </div>
                )}
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <button
                    onClick={logout}
                    className={cn(
                      'block w-full px-4 py-2 text-left text-sm',
                      active
                        ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                        : 'text-gray-700 dark:text-gray-300'
                    )}
                  >
                    Sign out
                  </button>
                )}
              </Menu.Item>
            </Menu.Items>
          </Transition>
        </Menu>
      </div>
    </header>
  );
} 