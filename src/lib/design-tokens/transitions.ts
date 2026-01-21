/**
 * Design Tokens - Transições e Animações
 * Durações, easings e delays para transições
 */

export const transitions = {
  duration: {
    instant: '0ms',
    fast: '150ms',
    base: '200ms',
    slow: '300ms',
    slower: '500ms',
    slowest: '700ms',
  },
  easing: {
    linear: 'linear',
    in: 'cubic-bezier(0.4, 0, 1, 1)',
    out: 'cubic-bezier(0, 0, 0.2, 1)',
    inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    // Easing functions mais suaves
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    // Easing para animações mais naturais
    spring: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
  delay: {
    none: '0ms',
    fast: '50ms',
    base: '100ms',
    slow: '200ms',
    slower: '300ms',
  },
} as const;

// Transições padrão para componentes
export const componentTransitions = {
  // Transições de cor
  color: `${transitions.duration.base} ${transitions.easing.inOut}`,
  // Transições de background
  background: `${transitions.duration.base} ${transitions.easing.inOut}`,
  // Transições de transform
  transform: `${transitions.duration.base} ${transitions.easing.out}`,
  // Transições de opacity
  opacity: `${transitions.duration.fast} ${transitions.easing.inOut}`,
  // Transições de shadow
  shadow: `${transitions.duration.base} ${transitions.easing.inOut}`,
  // Transições de border
  border: `${transitions.duration.fast} ${transitions.easing.inOut}`,
} as const;

// Animações comuns
export const animations = {
  fadeIn: {
    from: { opacity: 0 },
    to: { opacity: 1 },
    duration: transitions.duration.base,
    easing: transitions.easing.out,
  },
  slideUp: {
    from: { transform: 'translateY(10px)', opacity: 0 },
    to: { transform: 'translateY(0)', opacity: 1 },
    duration: transitions.duration.base,
    easing: transitions.easing.out,
  },
  slideDown: {
    from: { transform: 'translateY(-10px)', opacity: 0 },
    to: { transform: 'translateY(0)', opacity: 1 },
    duration: transitions.duration.base,
    easing: transitions.easing.out,
  },
  scaleIn: {
    from: { transform: 'scale(0.95)', opacity: 0 },
    to: { transform: 'scale(1)', opacity: 1 },
    duration: transitions.duration.base,
    easing: transitions.easing.spring,
  },
} as const;
