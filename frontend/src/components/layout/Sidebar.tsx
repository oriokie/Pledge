'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  HomeIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ClipboardDocumentListIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '@/contexts/AuthContext';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Members', href: '/members', icon: UserGroupIcon },
  { name: 'Contributions', href: '/contributions', icon: CurrencyDollarIcon },
  { name: 'Pledges', href: '/pledges', icon: ClipboardDocumentListIcon },
  { name: 'Reports', href: '/reports', icon: ChartBarIcon },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuth();

  return (
    <div className="flex min-h-0 flex-1 flex-col bg-gray-800">
      <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
        <div className="flex flex-shrink-0 items-center px-4">
          <img
            className="h-8 w-auto"
            src="/logo.png"
            alt="Church Pledging"
          />
        </div>
        <nav className="mt-5 flex-1 space-y-1 px-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                  isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <item.icon
                  className={`mr-3 h-6 w-6 flex-shrink-0 ${
                    isActive
                      ? 'text-white'
                      : 'text-gray-400 group-hover:text-gray-300'
                  }`}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      {user && (
        <div className="flex flex-shrink-0 bg-gray-700 p-4">
          <div className="group block w-full flex-shrink-0">
            <div className="flex items-center">
              <div>
                <img
                  className="inline-block h-9 w-9 rounded-full"
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                    user.full_name
                  )}&background=random`}
                  alt=""
                />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-white">{user.full_name}</p>
                <p className="text-xs font-medium text-gray-300 group-hover:text-gray-200">
                  {user.role}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 