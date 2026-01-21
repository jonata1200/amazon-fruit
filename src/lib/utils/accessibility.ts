/**
 * Utilitários de Acessibilidade
 * Funções para melhorar acessibilidade dos componentes
 */

/**
 * Gera um ID único para uso em componentes
 * @param prefix - Prefixo para o ID
 * @returns ID único
 */
export function generateId(prefix: string = 'id'): string {
  return `${prefix}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Cria atributos ARIA para um componente
 * @param options - Opções de ARIA
 * @returns Objeto com atributos ARIA
 */
export function createAriaAttributes(options: {
  label?: string;
  labelledBy?: string;
  describedBy?: string;
  expanded?: boolean;
  hidden?: boolean;
  live?: 'polite' | 'assertive' | 'off';
  busy?: boolean;
  invalid?: boolean;
  required?: boolean;
}): Record<string, string | boolean | undefined> {
  const attrs: Record<string, string | boolean | undefined> = {};

  if (options.label) attrs['aria-label'] = options.label;
  if (options.labelledBy) attrs['aria-labelledby'] = options.labelledBy;
  if (options.describedBy) attrs['aria-describedby'] = options.describedBy;
  if (options.expanded !== undefined) attrs['aria-expanded'] = options.expanded;
  if (options.hidden !== undefined) attrs['aria-hidden'] = options.hidden;
  if (options.live) attrs['aria-live'] = options.live;
  if (options.busy !== undefined) attrs['aria-busy'] = options.busy;
  if (options.invalid !== undefined) attrs['aria-invalid'] = options.invalid;
  if (options.required !== undefined) attrs['aria-required'] = options.required;

  return attrs;
}

/**
 * Cria texto apenas para screen readers
 * @param text - Texto a ser lido
 * @returns Classes Tailwind para screen reader only
 */
export function srOnly(text: string): { className: string; children: string } {
  return {
    className: 'sr-only',
    children: text,
  };
}

/**
 * Verifica se o contraste atende aos requisitos WCAG
 * (Wrapper para função de cores)
 */
export { meetsContrastRatio } from './colors';

/**
 * Cria atributos para navegação por teclado
 * @param onEnter - Callback para Enter
 * @param onEscape - Callback para Escape
 * @param onArrow - Callbacks para setas
 * @returns Handlers de teclado
 */
export function createKeyboardHandlers(options: {
  onEnter?: () => void;
  onEscape?: () => void;
  onArrowUp?: () => void;
  onArrowDown?: () => void;
  onArrowLeft?: () => void;
  onArrowRight?: () => void;
}): {
  onKeyDown: (e: React.KeyboardEvent) => void;
} {
  return {
    onKeyDown: (e: React.KeyboardEvent) => {
      switch (e.key) {
        case 'Enter':
          options.onEnter?.();
          break;
        case 'Escape':
          options.onEscape?.();
          break;
        case 'ArrowUp':
          options.onArrowUp?.();
          break;
        case 'ArrowDown':
          options.onArrowDown?.();
          break;
        case 'ArrowLeft':
          options.onArrowLeft?.();
          break;
        case 'ArrowRight':
          options.onArrowRight?.();
          break;
      }
    },
  };
}

/**
 * Cria atributos para focus management
 * @param autoFocus - Se deve focar automaticamente
 * @param trapFocus - Se deve travar o foco
 * @returns Atributos de foco
 */
export function createFocusAttributes(options: {
  autoFocus?: boolean;
  trapFocus?: boolean;
}): Record<string, boolean | undefined> {
  const attrs: Record<string, boolean | undefined> = {};
  
  if (options.autoFocus) attrs.autoFocus = true;
  if (options.trapFocus) attrs['data-focus-trap'] = true;
  
  return attrs;
}
