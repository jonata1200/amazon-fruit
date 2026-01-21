/**
 * Tailwind CSS - Variantes Customizadas
 * Variantes para estados, acessibilidade e media queries
 */

import type { Config } from 'tailwindcss';

/**
 * Variantes customizadas para o Tailwind
 */
export const customVariants: Config['theme'] = {
  extend: {},
};

/**
 * Função helper para criar variantes customizadas
 * Pode ser usado em plugins do Tailwind
 */
export function createCustomVariants() {
  return {
    // Variante para reduced-motion (acessibilidade)
    'reduced-motion': '@media (prefers-reduced-motion: reduce)',
    // Variante para print
    'print': '@media print',
    // Variante para hover que funciona em touch devices
    'hover-touch': '@media (hover: hover) and (pointer: fine)',
    // Variante para dark mode melhorado
    'dark-mode': '.dark &',
  };
}
