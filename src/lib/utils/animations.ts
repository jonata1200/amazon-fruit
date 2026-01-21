/**
 * Utilitários de Animações
 * Funções para trabalhar com animações e transições
 */

import { getTransition } from './design-tokens';
import type { TransitionDuration } from '@/lib/design-tokens/types';

/**
 * Verifica se o usuário prefere movimento reduzido
 * @returns true se prefers-reduced-motion está ativo
 */
export function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Obtém duração de transição respeitando prefers-reduced-motion
 * @param duration - Duração da transição
 * @returns Duração ajustada
 */
export function getRespectfulTransitionDuration(
  duration: TransitionDuration
): string {
  if (prefersReducedMotion()) {
    return '0ms';
  }
  return getTransition('duration', duration);
}

/**
 * Obtém classes Tailwind para animação
 * @param animation - Nome da animação
 * @param duration - Duração da animação
 * @returns Classes Tailwind
 */
export function getAnimationClasses(
  animation: 'fade' | 'slide' | 'scale' | 'spin',
  duration: TransitionDuration = 'base'
): string {
  const animationMap = {
    fade: 'animate-fade-in',
    slide: 'animate-slide-up',
    scale: 'animate-scale-in',
    spin: 'animate-spin',
  };

  const durationMap: Record<TransitionDuration, string> = {
    instant: 'duration-instant',
    fast: 'duration-fast',
    base: 'duration-base',
    slow: 'duration-slow',
    slower: 'duration-slower',
    slowest: 'duration-slowest',
  };

  return `${animationMap[animation]} ${durationMap[duration]}`;
}

/**
 * Cria delay de animação
 * @param delay - Delay em ms
 * @returns Classe Tailwind para delay
 */
export function getAnimationDelay(delay: number): string {
  return `delay-[${delay}ms]`;
}

/**
 * Obtém classes Tailwind para transição
 * @param properties - Propriedades para transicionar
 * @param duration - Duração
 * @param easing - Easing function
 * @returns Classes Tailwind
 */
export function getTransitionClasses(
  properties: string[] = ['all'],
  duration: TransitionDuration = 'base',
  easing: 'in' | 'out' | 'inOut' | 'linear' | 'spring' = 'inOut'
): string {
  const propClass = properties.length === 1 && properties[0] === 'all' 
    ? 'transition-all' 
    : `transition-[${properties.join(',')}]`;

  const durationClass = `duration-${duration}`;
  const easingClass = `ease-${easing}`;

  return `${propClass} ${durationClass} ${easingClass}`;
}
