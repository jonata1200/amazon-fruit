/**
 * Componente Tooltip - Dicas contextuais
 * Componente para exibir informações adicionais ao passar o mouse
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const tooltipVariants = cva(
  'absolute z-50 rounded-md px-3 py-1.5 text-sm shadow-md border pointer-events-none whitespace-nowrap animate-in fade-in-0 zoom-in-95',
  {
    variants: {
      variant: {
        default: 'bg-popover text-popover-foreground border-border',
        dark: 'bg-neutral-900 text-neutral-50 border-neutral-800',
        light: 'bg-white text-neutral-900 border-neutral-200',
      },
      side: {
        top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
        bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
        left: 'right-full top-1/2 -translate-y-1/2 mr-2',
        right: 'left-full top-1/2 -translate-y-1/2 ml-2',
      },
    },
    defaultVariants: {
      variant: 'default',
      side: 'top',
    },
  }
);

const arrowVariants = cva('absolute w-2 h-2 border rotate-45', {
  variants: {
    side: {
      top: 'top-full left-1/2 -translate-x-1/2 -translate-y-1/2 border-t-0 border-r-0',
      bottom: 'bottom-full left-1/2 -translate-x-1/2 translate-y-1/2 border-b-0 border-l-0',
      left: 'left-full top-1/2 -translate-y-1/2 -translate-x-1/2 border-l-0 border-b-0',
      right: 'right-full top-1/2 -translate-y-1/2 translate-x-1/2 border-r-0 border-t-0',
    },
    variant: {
      default: 'bg-popover border-border',
      dark: 'bg-neutral-900 border-neutral-800',
      light: 'bg-white border-neutral-200',
    },
  },
});

export interface TooltipProps extends VariantProps<typeof tooltipVariants> {
  children: React.ReactNode;
  content: React.ReactNode;
  delay?: number;
  className?: string;
  disabled?: boolean;
}

export function Tooltip({
  children,
  content,
  side = 'top',
  variant = 'default',
  delay = 200,
  className,
  disabled = false,
}: TooltipProps) {
  const [isVisible, setIsVisible] = React.useState(false);
  const timeoutRef = React.useRef<NodeJS.Timeout>();
  const tooltipId = React.useId(); // Mover useId para fora da renderização condicional

  const handleMouseEnter = () => {
    if (disabled) return;
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  // Suporte para touch em mobile
  const handleTouchStart = () => {
    if (disabled) return;
    setIsVisible(true);
  };

  const handleTouchEnd = () => {
    // Delay para permitir que o usuário veja o tooltip
    setTimeout(() => {
      setIsVisible(false);
    }, 2000);
  };

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <div
      className="relative inline-block"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleMouseEnter}
      onBlur={handleMouseLeave}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {children}
      {isVisible && !disabled && (
        <div
          role="tooltip"
          className={cn(tooltipVariants({ side, variant }), className)}
          id={`tooltip-${tooltipId}`}
        >
          {content}
          <div className={cn(arrowVariants({ side, variant }))} />
        </div>
      )}
    </div>
  );
}

interface HelpTooltipProps {
  content: React.ReactNode;
  className?: string;
  variant?: VariantProps<typeof tooltipVariants>['variant'];
}

export function HelpTooltip({ content, className, variant }: HelpTooltipProps) {
  return (
    <Tooltip content={content} className={className} variant={variant}>
      <span
        className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-muted text-muted-foreground text-xs cursor-help hover:bg-accent transition-colors"
        aria-label="Informação adicional"
      >
        ?
      </span>
    </Tooltip>
  );
}

export { tooltipVariants };
