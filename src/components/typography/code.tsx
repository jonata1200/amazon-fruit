/**
 * Componente Code - Código inline e block
 * Componente para exibir código com estilos apropriados
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const codeVariants = cva(
  'font-mono',
  {
    variants: {
      variant: {
        inline: 'relative rounded bg-muted px-[0.3rem] py-[0.2rem] text-sm font-mono text-foreground',
        block: 'relative w-full rounded-lg bg-muted p-4 text-sm font-mono text-foreground overflow-x-auto',
      },
      size: {
        sm: 'text-xs',
        base: 'text-sm',
        lg: 'text-base',
      },
    },
    defaultVariants: {
      variant: 'inline',
      size: 'base',
    },
  }
);

export interface CodeProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof codeVariants> {
  as?: 'code' | 'pre';
}

const Code = React.forwardRef<HTMLElement, CodeProps>(
  ({ className, as, variant = 'inline', size, children, ...props }, ref) => {
    // Se for block, usar <pre><code>, senão usar <code>
    if (variant === 'block') {
      return (
        <pre
          ref={ref as React.RefObject<HTMLPreElement>}
          className={cn(codeVariants({ variant, size }), className)}
          {...props}
        >
          <code>{children}</code>
        </pre>
      );
    }

    const Component = as || 'code';
    return (
      <Component
        ref={ref as never}
        className={cn(codeVariants({ variant, size }), className)}
        {...props}
      >
        {children}
      </Component>
    );
  }
);
Code.displayName = 'Code';

export { Code, codeVariants };
