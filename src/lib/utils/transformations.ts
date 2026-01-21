/**
 * Funções de Transformação de Tokens
 * Transforma design tokens em CSS, Tailwind classes e outros formatos
 */

import { tokens } from '@/lib/design-tokens';
import type { ColorName, ColorScale, SpacingKey, ShadowKey, BorderRadius } from '@/lib/design-tokens/types';

/**
 * Transforma token de cor em CSS custom property
 * @param name - Nome da cor
 * @param scale - Escala da cor
 * @returns CSS custom property
 */
export function colorToCSSVariable(name: ColorName, scale: ColorScale = 600): string {
  return `var(--color-${name}-${scale})`;
}

/**
 * Transforma token de espaçamento em classe Tailwind
 * @param key - Chave do espaçamento
 * @returns Classe Tailwind (ex: 'p-4', 'm-6')
 */
export function spacingToTailwindClass(key: SpacingKey, type: 'p' | 'm' | 'gap' = 'p'): string {
  const spacingMap: Record<SpacingKey, string> = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    12: '12',
    14: '14',
    16: '16',
    20: '20',
    24: '24',
    28: '28',
    32: '32',
    36: '36',
    40: '40',
    44: '44',
    48: '48',
    52: '52',
    56: '56',
    60: '60',
    64: '64',
    72: '72',
    80: '80',
    96: '96',
  };

  const value = spacingMap[key] || '4';
  return `${type}-${value}`;
}

/**
 * Transforma token de sombra em classe Tailwind
 * @param key - Chave da sombra
 * @returns Classe Tailwind (ex: 'shadow-md', 'shadow-lg')
 */
export function shadowToTailwindClass(key: ShadowKey): string {
  const shadowMap: Record<ShadowKey, string> = {
    none: 'shadow-none',
    sm: 'shadow-sm',
    base: 'shadow',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
    '2xl': 'shadow-2xl',
    inner: 'shadow-inner',
  };

  return shadowMap[key] || 'shadow';
}

/**
 * Transforma token de border radius em classe Tailwind
 * @param key - Chave do border radius
 * @returns Classe Tailwind (ex: 'rounded-md', 'rounded-lg')
 */
export function radiusToTailwindClass(key: BorderRadius): string {
  const radiusMap: Record<BorderRadius, string> = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    base: 'rounded',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl',
    full: 'rounded-full',
  };

  return radiusMap[key] || 'rounded';
}

/**
 * Gera CSS custom properties de todos os tokens
 * @returns String com CSS custom properties
 */
export function tokensToCSSVariables(): string {
  const cssVars: string[] = [];

  // Cores
  Object.entries(tokens.colors).forEach(([name, scales]) => {
    Object.entries(scales).forEach(([scale, value]) => {
      cssVars.push(`  --color-${name}-${scale}: ${value};`);
    });
  });

  // Espaçamento
  Object.entries(tokens.spacing.semantic).forEach(([key, value]) => {
    cssVars.push(`  --spacing-${key}: ${value};`);
  });

  // Sombras
  Object.entries(tokens.shadows).forEach(([key, value]) => {
    cssVars.push(`  --shadow-${key}: ${value};`);
  });

  return `:root {\n${cssVars.join('\n')}\n}`;
}

/**
 * Transforma objeto de tokens em classes Tailwind
 * @param config - Configuração de tokens
 * @returns Classes Tailwind combinadas
 */
export function tokensToTailwindClasses(config: {
  padding?: SpacingKey;
  margin?: SpacingKey;
  gap?: SpacingKey;
  shadow?: ShadowKey;
  radius?: BorderRadius;
}): string {
  const classes: string[] = [];

  if (config.padding) {
    classes.push(spacingToTailwindClass(config.padding, 'p'));
  }
  if (config.margin) {
    classes.push(spacingToTailwindClass(config.margin, 'm'));
  }
  if (config.gap) {
    classes.push(spacingToTailwindClass(config.gap, 'gap'));
  }
  if (config.shadow) {
    classes.push(shadowToTailwindClass(config.shadow));
  }
  if (config.radius) {
    classes.push(radiusToTailwindClass(config.radius));
  }

  return classes.join(' ');
}

/**
 * Valida e normaliza valor de token
 * @param value - Valor a ser validado
 * @param type - Tipo do token
 * @returns Valor normalizado ou valor padrão
 */
export function normalizeTokenValue(
  value: unknown,
  type: 'color' | 'spacing' | 'shadow' | 'radius'
): string {
  if (typeof value !== 'string') {
    return getDefaultValue(type);
  }

  // Validação básica
  switch (type) {
    case 'color':
      if (!value.match(/^#[0-9a-fA-F]{6}$/)) {
        return getDefaultValue(type);
      }
      break;
    case 'spacing':
      if (!value.match(/^\d+(\.\d+)?(rem|px)$/)) {
        return getDefaultValue(type);
      }
      break;
    case 'shadow':
      // Validação básica de sombra
      if (value === 'none' || value.includes('rgb') || value.includes('px')) {
        return value;
      }
      return getDefaultValue(type);
    case 'radius':
      if (!value.match(/^\d+(\.\d+)?(rem|px)$/) && value !== '0' && value !== '9999px') {
        return getDefaultValue(type);
      }
      break;
  }

  return value;
}

/**
 * Obtém valor padrão para tipo de token
 */
function getDefaultValue(type: 'color' | 'spacing' | 'shadow' | 'radius'): string {
  // Importar valores diretamente para evitar referência circular
  switch (type) {
    case 'color':
      return '#9333ea'; // primary-600
    case 'spacing':
      return '1rem'; // md spacing
    case 'shadow':
      return '0 1px 2px 0 rgb(0 0 0 / 0.05)'; // base shadow
    case 'radius':
      return '0.375rem'; // md radius
  }
}
