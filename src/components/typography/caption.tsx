/**
 * Componente Caption - Texto de legenda
 * Componente para textos pequenos, legendas e informações auxiliares
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const captionVariants = cva(
  'font-sans text-xs leading-normal tracking-wide',
  {
    variants: {
      color: {
        default: 'text-muted-foreground',
        muted: 'text-muted-foreground/70',
        primary: 'text-primary',
        success: 'text-success-600 dark:text-success-500',
        warning: 'text-warning-600 dark:text-warning-500',
        error: 'text-error-600 dark:text-error-500',
        info: 'text-info-600 dark:text-info-500',
      },
      weight: {
        normal: 'font-normal',
        medium: 'font-medium',
      },
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
      },
    },
    defaultVariants: {
      color: 'default',
      weight: 'normal',
      align: 'left',
    },
  }
);

export interface CaptionProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof captionVariants> {
  as?: 'p' | 'span' | 'div' | 'small';
}

const Caption = React.forwardRef<HTMLElement, CaptionProps>(
  ({ className, as = 'p', color, weight, align, ...props }, ref) => {
    const Component = as;
    return (
      <Component
        ref={ref as never}
        className={cn(captionVariants({ color, weight, align }), className)}
        {...props}
      />
    );
  }
);
Caption.displayName = 'Caption';

export { Caption, captionVariants };
