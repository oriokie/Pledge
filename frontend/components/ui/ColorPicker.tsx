'use client';

import { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface ColorPickerProps {
  label?: string;
  value: string;
  onChange: (value: string) => void;
  className?: string;
}

export function ColorPicker({
  label,
  value,
  onChange,
  className,
}: ColorPickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const pickerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (pickerRef.current && !pickerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const presetColors = [
    '#4F46E5', // Indigo
    '#10B981', // Emerald
    '#EF4444', // Red
    '#F59E0B', // Amber
    '#6366F1', // Blue
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#000000', // Black
    '#FFFFFF', // White
  ];

  return (
    <div className={cn('relative', className)} ref={pickerRef}>
      {label && (
        <label className="block text-sm font-medium text-gray-900 dark:text-gray-200 mb-2">
          {label}
        </label>
      )}
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="h-10 w-10 rounded-md border border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          style={{ backgroundColor: value }}
          onClick={() => setIsOpen(!isOpen)}
        />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
          placeholder="#000000"
        />
      </div>
      {isOpen && (
        <div className="absolute z-10 mt-2 rounded-md border border-gray-200 bg-white p-4 shadow-lg dark:border-gray-700 dark:bg-gray-800">
          <div className="grid grid-cols-3 gap-2">
            {presetColors.map((color) => (
              <button
                key={color}
                type="button"
                className="h-8 w-8 rounded-md border border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                style={{ backgroundColor: color }}
                onClick={() => {
                  onChange(color);
                  setIsOpen(false);
                }}
              />
            ))}
          </div>
          <div className="mt-4">
            <input
              type="color"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              className="h-8 w-full cursor-pointer rounded-md border-0"
            />
          </div>
        </div>
      )}
    </div>
  );
} 