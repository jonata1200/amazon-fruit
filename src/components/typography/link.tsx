/**
 * Componente Link - Links tipográficos
 * Componente para links com estilos consistentes e acessibilidade
 */

import * as React from 'react';
import Link from 'next/link';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const linkVariants = cva(
  'font-sans text-primary underline-offset-4 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'text-primary hover:text-primary/80 hover:underline',
        muted: 'text-muted-foreground hover:text-foreground hover:underline',
        underline: 'text-primary underline hover:text-primary/80',
        none: 'text-primary hover:text-primary/80 no-underline',
      },
      size: {
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
      },
      external: {
        true: 'after:content-["_↗"] after:text-xs after:opacity-70',
        false: '',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'base',
      external: false,
    },
  }
);

export interface TypographyLinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement>,
    VariantProps<typeof linkVariants> {
  href: string;
  external?: boolean;
  asChild?: boolean;
}

const TypographyLink = React.forwardRef<HTMLAnchorElement, TypographyLinkProps>(
  ({ className, href, variant, size, external, asChild, children, ...props }, ref) => {
    // Se for link externo, usar <a>, senão usar Next.js Link
    const isExternal = external || href.startsWith('http') || href.startsWith('//');

    if (isExternal || asChild) {
      return (
        <a
          ref={ref}
          href={href}
          target={isExternal ? '_blank' : undefined}
          rel={isExternal ? 'noopener noreferrer' : undefined}
          className={cn(linkVariants({ variant, size, external: isExternal }), className)}
          {...props}
        >
          {children}
        </a>
      );
    }

    return (
      <Link
        ref={ref}
        href={href}
        className={cn(linkVariants({ variant, size, external: false }), className)}
        {...props}
      >
        {children}
      </Link>
    );
  }
);
TypographyLink.displayName = 'TypographyLink';

export { TypographyLink, linkVariants };
