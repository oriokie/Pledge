'use client';

import { forwardRef } from 'react';
import { ExclamationCircleIcon } from '@heroicons/react/24/solid';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  multiline?: boolean;
  rows?: number;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  children: React.ReactNode;
}

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helper?: string;
}

interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helper?: string;
}

interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helper?: string;
}

const baseInputClasses = 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-800 dark:text-white dark:ring-gray-700 dark:placeholder:text-gray-500';
const errorInputClasses = 'ring-red-300 focus:ring-red-500 dark:ring-red-700';
const labelClasses = 'block text-sm font-medium leading-6 text-gray-900 dark:text-gray-200 mb-2';
const errorMessageClasses = 'mt-2 text-sm text-red-600 dark:text-red-500';

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, multiline, rows = 3, ...props }, ref) => {
    const Component = multiline ? 'textarea' : 'input';
    
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={props.id || props.name} className={labelClasses}>
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <Component
          className={cn(
            baseInputClasses,
            error && errorInputClasses,
            className
          )}
          ref={ref as any}
          {...(multiline ? { rows } : {})}
          {...props}
        />
        {error && <p className={errorMessageClasses}>{error}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, children, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={props.id || props.name} className={labelClasses}>
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <select
          className={cn(
            baseInputClasses,
            error && errorInputClasses,
            className
          )}
          ref={ref}
          {...props}
        >
          {children}
        </select>
        {error && <p className={errorMessageClasses}>{error}</p>}
      </div>
    );
  }
);

Select.displayName = 'Select';

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ label, error, helper, className, ...props }, ref) => {
    return (
      <div>
        {label && (
          <label htmlFor={props.id} className={labelClasses}>
            {label}
          </label>
        )}
        <div className="relative">
          <textarea
            ref={ref}
            className={`${error ? errorInputClasses : baseInputClasses} ${
              className || ''
            }`}
            {...props}
          />
          {error && (
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
              <ExclamationCircleIcon
                className="h-5 w-5 text-red-500"
                aria-hidden="true"
              />
            </div>
          )}
        </div>
        {error ? (
          <p className={errorMessageClasses}>{error}</p>
        ) : helper ? (
          <p className={errorMessageClasses}>{helper}</p>
        ) : null}
      </div>
    );
  }
);

TextArea.displayName = 'TextArea';

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, error, helper, className, ...props }, ref) => {
    return (
      <div>
        <div className="flex items-center">
          <input
            ref={ref}
            type="checkbox"
            className={`h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 ${
              error ? 'border-red-300' : ''
            } ${className || ''}`}
            {...props}
          />
          {label && (
            <label
              htmlFor={props.id}
              className="ml-2 block text-sm text-gray-900 dark:text-gray-300"
            >
              {label}
            </label>
          )}
        </div>
        {error ? (
          <p className={errorMessageClasses}>{error}</p>
        ) : helper ? (
          <p className={errorMessageClasses}>{helper}</p>
        ) : null}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export const Radio = forwardRef<HTMLInputElement, RadioProps>(
  ({ label, error, helper, className, ...props }, ref) => {
    return (
      <div>
        <div className="flex items-center">
          <input
            ref={ref}
            type="radio"
            className={`h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 ${
              error ? 'border-red-300' : ''
            } ${className || ''}`}
            {...props}
          />
          {label && (
            <label
              htmlFor={props.id}
              className="ml-2 block text-sm text-gray-900 dark:text-gray-300"
            >
              {label}
            </label>
          )}
        </div>
        {error ? (
          <p className={errorMessageClasses}>{error}</p>
        ) : helper ? (
          <p className={errorMessageClasses}>{helper}</p>
        ) : null}
      </div>
    );
  }
);

Radio.displayName = 'Radio'; 