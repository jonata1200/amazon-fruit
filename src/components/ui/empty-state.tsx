/**
 * Componente Empty State - Estado vazio
 * Componente para exibir quando não há conteúdo
 */

import * as React from 'react';
import { LucideIcon } from 'lucide-react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { Button } from './button';

const emptyStateVariants = cva('flex flex-col items-center justify-center text-center', {
  variants: {
    size: {
      sm: 'py-6 sm:py-8',
      md: 'py-8 sm:py-12',
      lg: 'py-12 sm:py-16',
    },
    variant: {
      default: '',
      muted: 'text-muted-foreground',
    },
  },
  defaultVariants: {
    size: 'md',
    variant: 'default',
  },
});

export interface EmptyStateProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof emptyStateVariants> {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  actionLabel,
  onAction,
  size,
  variant,
  className,
  ...props
}: EmptyStateProps) {
  return (
    <div className={cn(emptyStateVariants({ size, variant }), className)} {...props}>
      {Icon && (
        <Icon
          className={cn(
            'mb-4',
            size === 'sm' && 'h-8 w-8',
            size === 'md' && 'h-12 w-12',
            size === 'lg' && 'h-16 w-16',
            variant === 'muted' ? 'text-muted-foreground' : 'text-foreground/60'
          )}
          aria-hidden="true"
        />
      )}
      <h3 className={cn('font-semibold', size === 'sm' && 'text-base', size === 'md' && 'text-lg', size === 'lg' && 'text-xl')}>
        {title}
      </h3>
      {description && (
        <p
          className={cn(
            'mt-2 max-w-md',
            size === 'sm' && 'text-xs',
            size === 'md' && 'text-sm',
            size === 'lg' && 'text-base',
            variant === 'muted' ? 'text-muted-foreground' : 'text-muted-foreground'
          )}
        >
          {description}
        </p>
      )}
      {(action || (actionLabel && onAction)) && (
        <div className="mt-6">
          {action || (
            <Button onClick={onAction} variant="default" size="md">
              {actionLabel}
            </Button>
          )}
        </div>
      )}
    </div>
  );
}

export { emptyStateVariants };
