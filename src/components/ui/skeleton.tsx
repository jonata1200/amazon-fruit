/**
 * Componente Skeleton - Placeholders de carregamento
 * Componente para exibir placeholders durante o carregamento
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const skeletonVariants = cva('animate-pulse rounded-md bg-muted', {
  variants: {
    variant: {
      default: 'bg-muted',
      light: 'bg-muted/50',
      dark: 'bg-muted-foreground/10',
    },
    size: {
      xs: 'h-4',
      sm: 'h-6',
      md: 'h-8',
      lg: 'h-12',
      xl: 'h-16',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'md',
  },
});

export interface SkeletonProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof skeletonVariants> {
  circle?: boolean;
}

function Skeleton({ className, variant, size, circle, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        skeletonVariants({ variant, size }),
        circle && 'rounded-full',
        className
      )}
      aria-busy="true"
      aria-label="Carregando conteúdo"
      {...props}
    />
  );
}

export { Skeleton, skeletonVariants };
