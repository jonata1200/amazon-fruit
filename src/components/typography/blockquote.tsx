/**
 * Componente Blockquote - Citações
 * Componente para citações e textos destacados
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const blockquoteVariants = cva(
  'font-sans border-l-4 pl-4 italic text-muted-foreground',
  {
    variants: {
      color: {
        default: 'border-muted-foreground/30',
        primary: 'border-primary',
        success: 'border-success-500',
        warning: 'border-warning-500',
        error: 'border-error-500',
        info: 'border-info-500',
      },
      size: {
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
      },
    },
    defaultVariants: {
      color: 'default',
      size: 'base',
    },
  }
);

export interface BlockquoteProps
  extends React.BlockquoteHTMLAttributes<HTMLQuoteElement>,
    VariantProps<typeof blockquoteVariants> {}

const Blockquote = React.forwardRef<HTMLQuoteElement, BlockquoteProps>(
  ({ className, color, size, ...props }, ref) => {
    return (
      <blockquote
        ref={ref}
        className={cn(blockquoteVariants({ color, size }), className)}
        {...props}
      />
    );
  }
);
Blockquote.displayName = 'Blockquote';

export { Blockquote, blockquoteVariants };
