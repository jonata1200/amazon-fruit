/**
 * Componente Text - Texto base reutilizável
 * Componente flexível para renderizar texto com variantes tipográficas
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const textVariants = cva(
  'font-sans text-foreground',
  {
    variants: {
      size: {
        xs: 'text-xs',
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl',
        '2xl': 'text-2xl',
        '3xl': 'text-3xl',
      },
      weight: {
        light: 'font-light',
        normal: 'font-normal',
        medium: 'font-medium',
        semibold: 'font-semibold',
        bold: 'font-bold',
      },
      color: {
        default: 'text-foreground',
        muted: 'text-muted-foreground',
        primary: 'text-primary',
        secondary: 'text-secondary-foreground',
        success: 'text-success-600 dark:text-success-500',
        warning: 'text-warning-600 dark:text-warning-500',
        error: 'text-error-600 dark:text-error-500',
        info: 'text-info-600 dark:text-info-500',
      },
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
        justify: 'text-justify',
      },
      transform: {
        none: 'normal-case',
        uppercase: 'uppercase',
        lowercase: 'lowercase',
        capitalize: 'capitalize',
      },
      truncate: {
        none: '',
        true: 'truncate',
        '2': 'truncate-2',
        '3': 'truncate-3',
      },
    },
    defaultVariants: {
      size: 'base',
      weight: 'normal',
      color: 'default',
      align: 'left',
      transform: 'none',
      truncate: 'none',
    },
  }
);

export interface TextProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div' | 'strong' | 'em' | 'small';
}

const Text = React.forwardRef<HTMLElement, TextProps>(
  ({ className, as = 'p', size, weight, color, align, transform, truncate, ...props }, ref) => {
    const Component = as;
    return (
      <Component
        ref={ref as never}
        className={cn(textVariants({ size, weight, color, align, transform, truncate }), className)}
        {...props}
      />
    );
  }
);
Text.displayName = 'Text';

export { Text, textVariants };
