/**
 * Design Tokens - Types TypeScript
 * Tipos para garantir type-safety ao usar tokens
 */

import type { colors } from './colors';
import type { spacing, semanticSpacing } from './spacing';
import type { typography, typeScale } from './typography';
import type { shadows } from './shadows';
import type { borderRadius } from './borders';
import type { transitions } from './transitions';
import type { zIndex } from './z-index';
import type { breakpoints } from './breakpoints';

// Types para cores
export type ColorScale = keyof typeof colors.primary;
export type ColorName = keyof typeof colors;
export type ColorValue = typeof colors[ColorName][ColorScale];

// Types para espaçamento
export type SpacingKey = keyof typeof spacing;
export type SemanticSpacing = keyof typeof semanticSpacing;

// Types para tipografia
export type FontFamily = keyof typeof typography.fontFamilies;
export type FontSize = keyof typeof typography.fontSizes;
export type FontWeight = keyof typeof typography.fontWeights;
export type LineHeight = keyof typeof typography.lineHeights;
export type LetterSpacing = keyof typeof typography.letterSpacing;
export type TypeScaleKey = keyof typeof typeScale;

// Types para sombras
export type ShadowKey = keyof typeof shadows;

// Types para border radius
export type BorderRadius = keyof typeof borderRadius;

// Types para transições
export type TransitionDuration = keyof typeof transitions.duration;
export type TransitionEasing = keyof typeof transitions.easing;
export type TransitionDelay = keyof typeof transitions.delay;

// Types para z-index
export type ZIndexKey = keyof typeof zIndex;

// Types para breakpoints
export type Breakpoint = keyof typeof breakpoints;

// Helper type para acessar tokens com autocomplete
export type TokenPath =
  | `colors.${ColorName}.${ColorScale}`
  | `spacing.${SpacingKey}`
  | `typography.fontSizes.${FontSize}`
  | `typography.fontWeights.${FontWeight}`
  | `shadows.${ShadowKey}`
  | `borderRadius.${BorderRadius}`;
