/**
 * Helpers para Variantes de Componentes
 * Utilitários comuns para criar variantes consistentes
 */

import { cva } from 'class-variance-authority';

/**
 * Variantes de tamanho padrão
 */
export const sizeVariants = {
  xs: 'h-7 px-2 text-xs',
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-base',
  lg: 'h-11 px-6 text-lg',
  xl: 'h-12 px-8 text-xl',
} as const;

/**
 * Variantes de espaçamento padrão
 */
export const spacingVariants = {
  none: 'p-0',
  xs: 'p-1',
  sm: 'p-2',
  md: 'p-4',
  lg: 'p-6',
  xl: 'p-8',
} as const;

/**
 * Variantes de elevação/sombra
 */
export const elevationVariants = {
  none: 'shadow-none',
  sm: 'shadow-sm',
  md: 'shadow-md',
  lg: 'shadow-lg',
  xl: 'shadow-xl',
} as const;

/**
 * Variantes de border radius
 */
export const radiusVariants = {
  none: 'rounded-none',
  sm: 'rounded-sm',
  md: 'rounded-md',
  lg: 'rounded-lg',
  xl: 'rounded-xl',
  full: 'rounded-full',
} as const;

/**
 * Variantes de estado (para inputs, etc)
 */
export const stateVariants = {
  default: 'border-input',
  error: 'border-error-500 focus-visible:ring-error-500',
  success: 'border-success-500 focus-visible:ring-success-500',
  warning: 'border-warning-500 focus-visible:ring-warning-500',
} as const;

/**
 * Helper para criar variantes de tamanho
 */
export const createSizeVariants = (baseClasses: string) =>
  cva(baseClasses, {
    variants: {
      size: {
        xs: sizeVariants.xs,
        sm: sizeVariants.sm,
        md: sizeVariants.md,
        lg: sizeVariants.lg,
        xl: sizeVariants.xl,
      },
    },
    defaultVariants: {
      size: 'md',
    },
  });

/**
 * Helper para criar variantes de estado
 */
export const createStateVariants = (baseClasses: string) =>
  cva(baseClasses, {
    variants: {
      state: {
        default: stateVariants.default,
        error: stateVariants.error,
        success: stateVariants.success,
        warning: stateVariants.warning,
      },
    },
    defaultVariants: {
      state: 'default',
    },
  });
