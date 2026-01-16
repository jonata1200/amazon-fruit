// src/components/ui/icon.tsx
import * as React from 'react';
import { LucideIcon, LucideProps } from 'lucide-react';
import { cn } from '@/lib/utils';

export type IconSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

const sizeClasses: Record<IconSize, string> = {
  xs: 'h-3 w-3',
  sm: 'h-4 w-4',
  md: 'h-5 w-5',
  lg: 'h-6 w-6',
  xl: 'h-8 w-8',
};

interface IconProps extends Omit<LucideProps, 'size'> {
  icon: LucideIcon;
  size?: IconSize;
  className?: string;
}

/**
 * Componente de ícone consistente que encapsula Lucide React
 * 
 * @example
 * ```tsx
 * import { Apple } from 'lucide-react';
 * <Icon icon={Apple} size="md" />
 * ```
 */
export function Icon({ icon: IconComponent, size = 'md', className, ...props }: IconProps) {
  return (
    <IconComponent
      className={cn(sizeClasses[size], className)}
      {...props}
    />
  );
}

// Helper para criar ícones com tamanho padrão
export function createIcon(icon: LucideIcon, defaultSize: IconSize = 'md') {
  return function IconWrapper(props: Omit<IconProps, 'icon' | 'size'> & { size?: IconSize }) {
    return <Icon icon={icon} size={props.size || defaultSize} {...props} />;
  };
}
