/**
 * Hook useDesignToken - Hook para acessar design tokens com reatividade
 * Hook React para acessar design tokens de forma reativa
 */

'use client';

import { useMemo } from 'react';
import { tokens } from '@/lib/design-tokens';
import { getColor, getSpacing, getTypography, getShadow, getRadius, getTransition } from '@/lib/utils/design-tokens';
import type { ColorName, ColorScale, SpacingKey, FontSize, FontWeight, ShadowKey, BorderRadius, TransitionDuration } from '@/lib/design-tokens/types';

/**
 * Hook para acessar design tokens de forma reativa
 * @param tokenPath - Caminho do token (ex: 'colors.primary.600', 'spacing.md')
 * @returns Valor do token
 */
export function useDesignToken<T extends string>(tokenPath: T): string {
  return useMemo(() => {
    const parts = tokenPath.split('.');
    const category = parts[0];
    const key = parts[1];
    const subKey = parts[2];

    switch (category) {
      case 'colors':
        if (key && subKey) {
          return getColor(key as ColorName, parseInt(subKey) as ColorScale);
        }
        break;
      case 'spacing':
        if (key) {
          return getSpacing(key as SpacingKey);
        }
        break;
      case 'typography':
        if (key === 'fontSize' && subKey) {
          return getTypography('fontSize', subKey as FontSize);
        }
        if (key === 'fontWeight' && subKey) {
          return getTypography('fontWeight', subKey as FontWeight);
        }
        break;
      case 'shadows':
        if (key) {
          return getShadow(key as ShadowKey);
        }
        break;
      case 'borderRadius':
        if (key) {
          return getRadius(key as BorderRadius);
        }
        break;
      case 'transitions':
        if (key === 'duration' && subKey) {
          return getTransition('duration', subKey as TransitionDuration);
        }
        break;
    }

    // Fallback: tentar acessar diretamente do objeto tokens
    let value: any = tokens;
    for (const part of parts) {
      value = value?.[part];
      if (value === undefined) break;
    }

    return value || '';
  }, [tokenPath]);
}

/**
 * Hook para acessar cor específica
 * @param name - Nome da cor
 * @param scale - Escala da cor (padrão: 600)
 * @returns Valor da cor
 */
export function useColor(name: ColorName, scale: ColorScale = 600): string {
  return useMemo(() => getColor(name, scale), [name, scale]);
}

/**
 * Hook para acessar espaçamento específico
 * @param key - Chave do espaçamento
 * @returns Valor do espaçamento
 */
export function useSpacing(key: SpacingKey): string {
  return useMemo(() => getSpacing(key), [key]);
}

/**
 * Hook para acessar tipografia específica
 * @param type - Tipo (fontSize, fontWeight, etc)
 * @param key - Chave do valor
 * @returns Valor tipográfico
 */
export function useTypography(type: 'fontSize' | 'fontWeight', key: FontSize | FontWeight): string {
  return useMemo(() => getTypography(type, key as any), [type, key]);
}

/**
 * Hook para acessar múltiplos tokens de uma vez
 * @param tokens - Objeto com caminhos de tokens
 * @returns Objeto com valores dos tokens
 */
/**
 * Hook para acessar múltiplos tokens de uma vez
 * @param tokenPaths - Objeto com caminhos de tokens
 * @returns Objeto com valores dos tokens
 */
export function useDesignTokens<T extends Record<string, string>>(
  tokenPaths: T
): Record<keyof T, string> {
  return useMemo(() => {
    const result: Record<string, string> = {};
    for (const [key, path] of Object.entries(tokenPaths)) {
      result[key] = useDesignToken(path);
    }
    return result as Record<keyof T, string>;
  }, [tokenPaths]);
}
