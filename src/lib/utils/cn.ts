/**
 * Função cn() Otimizada
 * Combina clsx e tailwind-merge para melhor performance e suporte a design tokens
 */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Combina classes CSS de forma otimizada
 * 
 * @param inputs - Classes CSS, objetos condicionais, arrays, etc.
 * @returns String com classes combinadas e conflitos resolvidos
 * 
 * @example
 * cn('px-4', 'py-2', 'bg-primary')
 * cn('px-4', { 'bg-primary': isActive })
 * cn(['px-4', 'py-2'], 'bg-primary')
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Helper para criar classes condicionais com variantes
 * Útil para componentes com múltiplas variantes
 * 
 * @param base - Classes base
 * @param variants - Objeto com variantes e classes correspondentes
 * @param conditionals - Classes condicionais adicionais
 * @returns String com classes combinadas
 * 
 * @example
 * cnVariants('btn', {
 *   size: { sm: 'px-2 py-1', md: 'px-4 py-2' },
 *   variant: { primary: 'bg-primary', secondary: 'bg-secondary' }
 * }, { sm: true, variant: 'primary' })
 */
export function cnVariants<T extends Record<string, Record<string, string>>>(
  base: string | ClassValue,
  variants: T,
  conditionals?: Partial<Record<keyof T, keyof T[keyof T]>>,
  ...additional: ClassValue[]
): string {
  const baseClasses = typeof base === 'string' ? base : cn(base);
  const variantClasses = conditionals
    ? Object.entries(conditionals)
        .map(([key, value]) => {
          if (value && variants[key as keyof T]) {
            return variants[key as keyof T][value as keyof T[keyof T]];
          }
          return '';
        })
        .filter(Boolean)
        .join(' ')
    : '';

  return cn(baseClasses, variantClasses, ...additional);
}

/**
 * Helper para criar classes com design tokens
 * Facilita uso de design tokens em componentes
 * 
 * @param tokenPath - Caminho do token (ex: 'spacing.md', 'colors.primary.600')
 * @param prefix - Prefixo da classe Tailwind (ex: 'p-', 'text-', 'bg-')
 * @returns Classe Tailwind formatada
 * 
 * @example
 * tokenClass('spacing.md', 'p-') // 'p-4'
 * tokenClass('colors.primary.600', 'bg-') // 'bg-primary-600'
 */
export function tokenClass(tokenPath: string, prefix: string): string {
  // Esta função é mais para documentação - na prática, use os tokens diretamente
  // ou crie classes utilitárias específicas
  return `${prefix}${tokenPath.replace(/\./g, '-')}`;
}
