/**
 * Componente Input - Campos de entrada padronizados
 * Componente de input com variantes, estados e acessibilidade
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

const inputVariants = cva(
  'flex w-full rounded-md border bg-background px-3 py-2 text-sm ring-offset-background transition-all duration-base file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      size: {
        sm: 'h-8 px-2 text-sm',
        md: 'h-10 px-3 text-sm min-h-[44px]',
        lg: 'h-12 px-4 text-base min-h-[44px]',
      },
      state: {
        default: 'border-input focus-visible:ring-ring',
        error: 'border-error-500 focus-visible:ring-error-500',
        success: 'border-success-500 focus-visible:ring-success-500',
        warning: 'border-warning-500 focus-visible:ring-warning-500',
      },
    },
    defaultVariants: {
      size: 'md',
      state: 'default',
    },
  }
);

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement>,
    VariantProps<typeof inputVariants> {
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  showStateIcon?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, size, state, leftIcon, rightIcon, showStateIcon, ...props }, ref) => {
    const hasLeftIcon = leftIcon || (showStateIcon && state === 'error');
    const hasRightIcon = rightIcon || (showStateIcon && (state === 'success' || state === 'error'));

    return (
      <div className="relative w-full">
        {hasLeftIcon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
            {showStateIcon && state === 'error' ? (
              <AlertCircle className="h-4 w-4 text-error-500" aria-hidden="true" />
            ) : (
              leftIcon
            )}
          </div>
        )}
        <input
          type={type}
          className={cn(
            inputVariants({ size, state }),
            hasLeftIcon && 'pl-9',
            hasRightIcon && 'pr-9',
            'text-base sm:text-sm', // Prevenir zoom iOS (mínimo 16px)
            className
          )}
          ref={ref}
          aria-invalid={state === 'error' ? 'true' : undefined}
          {...props}
        />
        {hasRightIcon && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground">
            {showStateIcon && state === 'success' ? (
              <CheckCircle2 className="h-4 w-4 text-success-500" aria-hidden="true" />
            ) : showStateIcon && state === 'error' ? (
              <AlertCircle className="h-4 w-4 text-error-500" aria-hidden="true" />
            ) : (
              rightIcon
            )}
          </div>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input, inputVariants };
