/**
 * Utilitários de Breakpoints
 * Funções e hooks para trabalhar com breakpoints responsivos
 */

import { getBreakpoint } from './design-tokens';
import type { Breakpoint } from '@/lib/design-tokens/types';

/**
 * Converte breakpoint para valor numérico em pixels
 * @param breakpoint - Breakpoint do design system
 * @returns Valor numérico em pixels
 */
export function breakpointToPx(breakpoint: Breakpoint): number {
  const value = getBreakpoint(breakpoint);
  return parseInt(value.replace('px', ''), 10);
}

/**
 * Verifica se o viewport está acima de um breakpoint
 * @param breakpoint - Breakpoint a verificar
 * @returns true se o viewport está acima do breakpoint
 */
export function isAboveBreakpoint(breakpoint: Breakpoint): boolean {
  if (typeof window === 'undefined') return false;
  const px = breakpointToPx(breakpoint);
  return window.innerWidth >= px;
}

/**
 * Verifica se o viewport está abaixo de um breakpoint
 * @param breakpoint - Breakpoint a verificar
 * @returns true se o viewport está abaixo do breakpoint
 */
export function isBelowBreakpoint(breakpoint: Breakpoint): boolean {
  if (typeof window === 'undefined') return false;
  const px = breakpointToPx(breakpoint);
  return window.innerWidth < px;
}

/**
 * Obtém classes Tailwind responsivas
 * @param mobile - Classes para mobile
 * @param tablet - Classes para tablet
 * @param desktop - Classes para desktop
 * @returns Classes Tailwind responsivas
 */
export function getResponsiveClasses(options: {
  mobile?: string;
  tablet?: string;
  desktop?: string;
}): string {
  const classes: string[] = [];
  
  if (options.mobile) classes.push(options.mobile);
  if (options.tablet) classes.push(`md:${options.tablet}`);
  if (options.desktop) classes.push(`lg:${options.desktop}`);
  
  return classes.join(' ');
}
