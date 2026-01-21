// src/lib/design-tokens.ts
/**
 * Design Tokens Centralizados
 * Fonte única de verdade para design system
 * 
 * @deprecated Este arquivo está sendo migrado para estrutura modular em design-tokens/
 * Use `import { tokens } from '@/lib/design-tokens'` para nova estrutura
 * Este arquivo mantém compatibilidade com código existente
 */

// Re-exportar da nova estrutura para compatibilidade
export { tokens } from './design-tokens/index';

// Re-exportar tipos da nova estrutura
export type {
  ColorScale,
  SpacingKey,
  SemanticSpacing,
  FontSize,
  FontWeight,
} from './design-tokens/types';
