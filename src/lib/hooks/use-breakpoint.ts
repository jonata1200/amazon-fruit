/**
 * Hook useBreakpoint - Hook para detectar breakpoints
 * Hook React para verificar breakpoints responsivos
 */

'use client';

import { useState, useEffect } from 'react';
import { isAboveBreakpoint, isBelowBreakpoint } from '@/lib/utils/breakpoints';
import type { Breakpoint } from '@/lib/design-tokens/types';

/**
 * Hook para verificar se o viewport está acima de um breakpoint
 * @param breakpoint - Breakpoint a verificar
 * @returns true se está acima do breakpoint
 */
export function useBreakpoint(breakpoint: Breakpoint): boolean {
  const [isAbove, setIsAbove] = useState(() => {
    if (typeof window === 'undefined') return false;
    return isAboveBreakpoint(breakpoint);
  });

  useEffect(() => {
    const handleResize = () => {
      setIsAbove(isAboveBreakpoint(breakpoint));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [breakpoint]);

  return isAbove;
}

/**
 * Hook para verificar se o viewport está abaixo de um breakpoint
 * @param breakpoint - Breakpoint a verificar
 * @returns true se está abaixo do breakpoint
 */
export function useBreakpointBelow(breakpoint: Breakpoint): boolean {
  const [isBelow, setIsBelow] = useState(() => {
    if (typeof window === 'undefined') return false;
    return isBelowBreakpoint(breakpoint);
  });

  useEffect(() => {
    const handleResize = () => {
      setIsBelow(isBelowBreakpoint(breakpoint));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [breakpoint]);

  return isBelow;
}

/**
 * Hook para obter o breakpoint atual
 * @returns Breakpoint atual ou null
 */
export function useCurrentBreakpoint(): Breakpoint | null {
  const [current, setCurrent] = useState<Breakpoint | null>(() => {
    if (typeof window === 'undefined') return null;
    
    if (isAboveBreakpoint('2xl')) return '2xl';
    if (isAboveBreakpoint('xl')) return 'xl';
    if (isAboveBreakpoint('lg')) return 'lg';
    if (isAboveBreakpoint('md')) return 'md';
    if (isAboveBreakpoint('sm')) return 'sm';
    return null;
  });

  useEffect(() => {
    const handleResize = () => {
      if (isAboveBreakpoint('2xl')) setCurrent('2xl');
      else if (isAboveBreakpoint('xl')) setCurrent('xl');
      else if (isAboveBreakpoint('lg')) setCurrent('lg');
      else if (isAboveBreakpoint('md')) setCurrent('md');
      else if (isAboveBreakpoint('sm')) setCurrent('sm');
      else setCurrent(null);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return current;
}
