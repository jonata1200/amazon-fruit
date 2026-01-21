/**
 * Componente Heading - Títulos hierárquicos (H1-H6)
 * Componente semântico para títulos com hierarquia tipográfica clara
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const headingVariants = cva(
  'font-sans font-bold text-foreground tracking-tight',
  {
    variants: {
      level: {
        h1: 'text-5xl md:text-6xl leading-tight',
        h2: 'text-4xl md:text-5xl leading-snug',
        h3: 'text-3xl md:text-4xl leading-snug',
        h4: 'text-2xl md:text-3xl leading-normal',
        h5: 'text-xl md:text-2xl leading-normal',
        h6: 'text-lg md:text-xl leading-normal',
        display: 'text-6xl md:text-7xl lg:text-8xl leading-tight',
      },
      weight: {
        bold: 'font-bold',
        semibold: 'font-semibold',
        extrabold: 'font-extrabold',
      },
      color: {
        default: 'text-foreground',
        muted: 'text-muted-foreground',
        primary: 'text-primary',
        secondary: 'text-secondary-foreground',
      },
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
      },
    },
    defaultVariants: {
      level: 'h1',
      weight: 'bold',
      color: 'default',
      align: 'left',
    },
  }
);

export interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof headingVariants> {
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
}

const Heading = React.forwardRef<HTMLHeadingElement, HeadingProps>(
  ({ className, as, level, weight, color, align, children, ...props }, ref) => {
    // Determinar tag HTML baseado em 'as' ou 'level'
    const tag = as || (level?.replace('h', '') as 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | undefined) || 'h1';
    const Component = tag;

    // Se level for 'display', usar h1 como tag mas com estilos de display
    const actualLevel = level === 'display' ? 'h1' : level || 'h1';

    return (
      <Component
        ref={ref}
        className={cn(headingVariants({ level: actualLevel, weight, color, align }), className)}
        {...props}
      >
        {children}
      </Component>
    );
  }
);
Heading.displayName = 'Heading';

export { Heading, headingVariants };
