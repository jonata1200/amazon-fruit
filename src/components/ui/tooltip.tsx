// src/components/ui/tooltip.tsx
'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface TooltipProps {
  children: React.ReactNode;
  content: React.ReactNode;
  side?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
  className?: string;
}

export function Tooltip({ children, content, side = 'top', delay = 200, className }: TooltipProps) {
  const [isVisible, setIsVisible] = React.useState(false);
  const timeoutRef = React.useRef<NodeJS.Timeout>();

  const handleMouseEnter = () => {
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

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const sideClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      {isVisible && (
        <div
          role="tooltip"
          className={cn(
            'absolute z-50 rounded-md bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md border pointer-events-none whitespace-nowrap animate-in fade-in-0 zoom-in-95',
            sideClasses[side],
            className
          )}
        >
          {content}
          {/* Arrow */}
          <div
            className={cn(
              'absolute w-2 h-2 bg-popover border rotate-45',
              side === 'top' && 'top-full left-1/2 -translate-x-1/2 -translate-y-1/2 border-t-0 border-r-0',
              side === 'bottom' && 'bottom-full left-1/2 -translate-x-1/2 translate-y-1/2 border-b-0 border-l-0',
              side === 'left' && 'left-full top-1/2 -translate-y-1/2 -translate-x-1/2 border-l-0 border-b-0',
              side === 'right' && 'right-full top-1/2 -translate-y-1/2 translate-x-1/2 border-r-0 border-t-0'
            )}
          />
        </div>
      )}
    </div>
  );
}

interface HelpTooltipProps {
  content: React.ReactNode;
  className?: string;
}

export function HelpTooltip({ content, className }: HelpTooltipProps) {
  return (
    <Tooltip content={content} className={className}>
      <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-muted text-muted-foreground text-xs cursor-help hover:bg-accent">
        ?
      </span>
    </Tooltip>
  );
}
