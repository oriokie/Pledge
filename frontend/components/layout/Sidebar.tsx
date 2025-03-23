'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  HomeIcon,
  UsersIcon,
  CurrencyDollarIcon,
  FolderIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  ChevronDownIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';
import { cn } from '@/lib/utils';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  children?: NavItem[];
}

const navigation: NavItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: HomeIcon,
  },
  {
    name: 'Members',
    href: '/members',
    icon: UsersIcon,
  },
  {
    name: 'Contributions',
    href: '/contributions',
    icon: CurrencyDollarIcon,
  },
  {
    name: 'Projects',
    href: '/projects',
    icon: FolderIcon,
  },
  {
    name: 'Groups',
    href: '/groups',
    icon: UserGroupIcon,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Cog6ToothIcon,
  },
];

interface SidebarProps {
  className?: string;
}

export default function Sidebar({ className }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);
  const pathname = usePathname();

  const toggleItem = (name: string) => {
    setExpandedItems((current) =>
      current.includes(name)
        ? current.filter((item) => item !== name)
        : [...current, name]
    );
  };

  const isActive = (href: string) => pathname === href;

  return (
    <div
      className={cn(
        'flex h-full flex-col bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700',
        isCollapsed ? 'w-16' : 'w-64',
        className
      )}
    >
      <div className="flex h-16 items-center justify-between px-4">
        {!isCollapsed && (
          <span className="text-xl font-semibold text-gray-900 dark:text-white">
            Pledge
          </span>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-700"
        >
          {isCollapsed ? (
            <ChevronRightIcon className="h-5 w-5" />
          ) : (
            <ChevronDownIcon className="h-5 w-5" />
          )}
        </button>
      </div>

      <nav className="flex-1 space-y-1 px-2 py-4">
        {navigation.map((item) => (
          <div key={item.name}>
            {item.children ? (
              <>
                <button
                  onClick={() => toggleItem(item.name)}
                  className={cn(
                    'flex w-full items-center rounded-md px-3 py-2 text-sm font-medium',
                    isActive(item.href)
                      ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                  )}
                >
                  <item.icon
                    className={cn(
                      'mr-3 h-5 w-5 flex-shrink-0',
                      isActive(item.href)
                        ? 'text-gray-500 dark:text-gray-300'
                        : 'text-gray-400 group-hover:text-gray-500 dark:text-gray-400 dark:group-hover:text-gray-300'
                    )}
                  />
                  {!isCollapsed && (
                    <>
                      <span className="flex-1">{item.name}</span>
                      {expandedItems.includes(item.name) ? (
                        <ChevronDownIcon className="h-4 w-4" />
                      ) : (
                        <ChevronRightIcon className="h-4 w-4" />
                      )}
                    </>
                  )}
                </button>
                {!isCollapsed && expandedItems.includes(item.name) && (
                  <div className="ml-4 mt-1 space-y-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.name}
                        href={child.href}
                        className={cn(
                          'flex items-center rounded-md px-3 py-2 text-sm font-medium',
                          isActive(child.href)
                            ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                        )}
                      >
                        <child.icon
                          className={cn(
                            'mr-3 h-5 w-5 flex-shrink-0',
                            isActive(child.href)
                              ? 'text-gray-500 dark:text-gray-300'
                              : 'text-gray-400 group-hover:text-gray-500 dark:text-gray-400 dark:group-hover:text-gray-300'
                          )}
                        />
                        {child.name}
                      </Link>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <Link
                href={item.href}
                className={cn(
                  'flex items-center rounded-md px-3 py-2 text-sm font-medium',
                  isActive(item.href)
                    ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                )}
              >
                <item.icon
                  className={cn(
                    'mr-3 h-5 w-5 flex-shrink-0',
                    isActive(item.href)
                      ? 'text-gray-500 dark:text-gray-300'
                      : 'text-gray-400 group-hover:text-gray-500 dark:text-gray-400 dark:group-hover:text-gray-300'
                  )}
                />
                {!isCollapsed && item.name}
              </Link>
            )}
          </div>
        ))}
      </nav>
    </div>
  );
} 