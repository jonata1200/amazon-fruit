/**
 * Componente Dropdown Menu - Menus suspensos
 * Componente padronizado com design tokens, acessibilidade e variantes
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { componentZIndex } from '@/lib/design-tokens';

// Variantes do Dropdown Menu Content
const dropdownContentVariants = cva(
  'absolute mt-2 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md transition-all duration-base',
  {
    variants: {
      align: {
        start: 'left-0',
        center: 'left-1/2 -translate-x-1/2',
        end: 'right-0',
      },
      size: {
        sm: 'min-w-[6rem]',
        md: 'min-w-[8rem]',
        lg: 'min-w-[12rem]',
      },
    },
    defaultVariants: {
      align: 'start',
      size: 'md',
    },
  }
);

// Variantes do Dropdown Menu Item
const dropdownItemVariants = cva(
  'relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
  {
    variants: {
      variant: {
        default: 'hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground',
        destructive: 'text-destructive hover:bg-destructive hover:text-destructive-foreground focus:bg-destructive focus:text-destructive-foreground',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface DropdownMenuProps {
  children: React.ReactNode;
}

interface DropdownMenuTriggerProps {
  children: React.ReactNode;
  asChild?: boolean;
  className?: string;
}

export interface DropdownMenuContentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof dropdownContentVariants> {
  children: React.ReactNode;
}

export interface DropdownMenuItemProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof dropdownItemVariants> {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

const DropdownMenuContext = React.createContext<{
  open: boolean;
  setOpen: (open: boolean) => void;
}>({
  open: false,
  setOpen: () => {},
});

export function DropdownMenu({ children }: DropdownMenuProps) {
  const [open, setOpen] = React.useState(false);

  return (
    <DropdownMenuContext.Provider value={{ open, setOpen }}>
      <div className="relative inline-block">{children}</div>
    </DropdownMenuContext.Provider>
  );
}

export function DropdownMenuTrigger({ 
  children, 
  asChild,
  className 
}: DropdownMenuTriggerProps) {
  const { open, setOpen } = React.useContext(DropdownMenuContext);

  const handleClick = () => {
    setOpen(!open);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setOpen(!open);
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  };

  if (asChild) {
    return (
      <div 
        onClick={handleClick} 
        onKeyDown={handleKeyDown}
        className={className}
        role="button"
        tabIndex={0}
        aria-expanded={open}
        aria-haspopup="true"
      >
        {children}
      </div>
    );
  }

  return (
    <button
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-expanded={open}
      aria-haspopup="true"
      aria-label="Abrir menu"
      className={className}
    >
      {children}
    </button>
  );
}

export function DropdownMenuContent({ 
  children, 
  align,
  size,
  className,
  ...props 
}: DropdownMenuContentProps) {
  const { open, setOpen } = React.useContext(DropdownMenuContext);
  const ref = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [open, setOpen]);

  if (!open) return null;

  return (
    <div
      ref={ref}
      role="menu"
      aria-orientation="vertical"
      style={{ zIndex: componentZIndex.dropdown }}
      className={cn(dropdownContentVariants({ align, size }), className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function DropdownMenuItem({ 
  children, 
  onClick, 
  disabled,
  variant,
  className,
  ...props 
}: DropdownMenuItemProps) {
  const { setOpen } = React.useContext(DropdownMenuContext);

  const handleClick = () => {
    if (!disabled && onClick) {
      onClick();
      setOpen(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  };

  return (
    <div
      role="menuitem"
      tabIndex={disabled ? -1 : 0}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-disabled={disabled}
      className={cn(
        dropdownItemVariants({ variant }),
        disabled && 'pointer-events-none opacity-50 cursor-not-allowed',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
