/**
 * Design Tokens - Export Principal
 * Fonte única de verdade para design system
 * 
 * Este arquivo exporta todos os tokens organizados em uma estrutura hierárquica
 */

// Exportar todos os tokens
export * from './colors';
export * from './spacing';
export * from './typography';
export * from './shadows';
export * from './borders';
export * from './transitions';
export * from './z-index';
export * from './breakpoints';
export * from './types';

// Importar para criar objeto consolidado
import { colors, stateColors, opacity, textColors } from './colors';
import { spacing, semanticSpacing, componentSpacing, gridSpacing } from './spacing';
import { typography, typeScale } from './typography';
import { shadows, shadowsDark, elevation, componentShadows } from './shadows';
import { borderRadius, componentRadius, borderWidth, borderStyle } from './borders';
import { transitions, componentTransitions, animations } from './transitions';
import { zIndex, componentZIndex } from './z-index';
import { breakpoints, containerWidths, mediaQueries } from './breakpoints';

/**
 * Objeto consolidado com todos os tokens
 * Mantém compatibilidade com código existente
 */
export const tokens = {
  colors: {
    ...colors,
    state: stateColors,
    opacity,
    text: textColors,
  },
  spacing: {
    ...spacing,
    semantic: semanticSpacing,
    component: componentSpacing,
    grid: gridSpacing,
  },
  typography: {
    ...typography,
    scale: typeScale,
  },
  shadows: {
    light: shadows,
    dark: shadowsDark,
    elevation,
    component: componentShadows,
  },
  borderRadius: {
    ...borderRadius,
    component: componentRadius,
  },
  borders: {
    width: borderWidth,
    style: borderStyle,
  },
  transitions: {
    ...transitions,
    component: componentTransitions,
    animations,
  },
  zIndex: {
    ...zIndex,
    component: componentZIndex,
  },
  breakpoints: {
    ...breakpoints,
    container: containerWidths,
    media: mediaQueries,
  },
} as const;

// Re-exportar tipos para facilitar uso
export type {
  ColorScale,
  ColorName,
  ColorValue,
  SpacingKey,
  SemanticSpacing,
  FontFamily,
  FontSize,
  FontWeight,
  LineHeight,
  LetterSpacing,
  TypeScaleKey,
  ShadowKey,
  BorderRadius,
  TransitionDuration,
  TransitionEasing,
  TransitionDelay,
  ZIndexKey,
  Breakpoint,
  TokenPath,
} from './types';
