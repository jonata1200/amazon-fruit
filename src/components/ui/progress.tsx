/**
 * Componente Progress - Barra de progresso
 * Componente para exibir progresso de uma operação
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const progressVariants = cva('relative w-full overflow-hidden rounded-full bg-secondary', {
  variants: {
    size: {
      sm: 'h-1',
      md: 'h-2',
      lg: 'h-3',
      xl: 'h-4',
    },
    variant: {
      default: 'bg-secondary',
      success: 'bg-success-100 dark:bg-success-900/20',
      warning: 'bg-warning-100 dark:bg-warning-900/20',
      error: 'bg-error-100 dark:bg-error-900/20',
    },
  },
  defaultVariants: {
    size: 'md',
    variant: 'default',
  },
});

const progressBarVariants = cva(
  'h-full transition-all duration-base ease-in-out',
  {
    variants: {
      variant: {
        default: 'bg-primary',
        success: 'bg-success-600 dark:bg-success-500',
        warning: 'bg-warning-600 dark:bg-warning-500',
        error: 'bg-error-600 dark:bg-error-500',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface ProgressProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof progressVariants> {
  value?: number; // 0-100
  max?: number;
  showLabel?: boolean;
  barVariant?: VariantProps<typeof progressBarVariants>['variant'];
}

export function Progress({
  value = 0,
  max = 100,
  showLabel = false,
  size,
  variant,
  barVariant,
  className,
  ...props
}: ProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div
      className={cn(progressVariants({ size, variant }), className)}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-label={`Progresso: ${Math.round(percentage)}%`}
      {...props}
    >
      <div
        className={cn(progressBarVariants({ variant: barVariant || variant }))}
        style={{ width: `${percentage}%` }}
      />
      {showLabel && (
        <span className="absolute inset-0 flex items-center justify-center text-xs font-medium text-foreground">
          {Math.round(percentage)}%
        </span>
      )}
    </div>
  );
}

export { progressVariants, progressBarVariants };
