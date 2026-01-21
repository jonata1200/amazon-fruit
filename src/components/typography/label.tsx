/**
 * Componente Label - Rótulos e etiquetas
 * Componente para rótulos de formulários e etiquetas
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const labelVariants = cva(
  'font-sans font-medium text-foreground leading-none',
  {
    variants: {
      size: {
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
      },
      weight: {
        normal: 'font-normal',
        medium: 'font-medium',
        semibold: 'font-semibold',
      },
      color: {
        default: 'text-foreground',
        muted: 'text-muted-foreground',
        required: 'text-foreground after:content-["*"] after:text-error-500 after:ml-1',
      },
      required: {
        true: 'after:content-["*"] after:text-error-500 after:ml-1',
        false: '',
      },
    },
    defaultVariants: {
      size: 'sm',
      weight: 'medium',
      color: 'default',
      required: false,
    },
  }
);

export interface LabelProps
  extends React.LabelHTMLAttributes<HTMLLabelElement>,
    VariantProps<typeof labelVariants> {}

const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, size, weight, color, required, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(
          labelVariants({ size, weight, color, required }),
          'peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
          className
        )}
        {...props}
      />
    );
  }
);
Label.displayName = 'Label';

export { Label, labelVariants };
