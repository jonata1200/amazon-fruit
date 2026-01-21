/**
 * Utilitários de Performance
 * Helpers para lazy loading, memoização, debounce/throttle e otimização de renders
 */

import * as React from 'react';
import { useMemo, useCallback, memo, lazy, useRef, useState, useEffect, type ComponentType, type MemoExoticComponent } from 'react';

/**
 * Cria um componente lazy com fallback
 * @param importFn - Função de import
 * @returns Componente lazy
 */
export function createLazyComponent<T extends ComponentType<any>>(
  importFn: () => Promise<{ default: T }>
): MemoExoticComponent<T> {
  const LazyComponent = lazy(importFn);
  return memo(LazyComponent) as MemoExoticComponent<T>;
}

/**
 * Hook para memoização de valores calculados
 * @param factory - Função que calcula o valor
 * @param deps - Dependências
 * @returns Valor memoizado
 */
export function useMemoizedValue<T>(factory: () => T, deps: React.DependencyList): T {
  return useMemo(factory, deps);
}

/**
 * Hook para memoização de callbacks
 * @param callback - Função callback
 * @param deps - Dependências
 * @returns Callback memoizado
 */
export function useMemoizedCallback<T extends (...args: any[]) => any>(
  callback: T,
  deps: React.DependencyList
): T {
  return useCallback(callback, deps) as T;
}

/**
 * Debounce function
 * @param func - Função a ser debounced
 * @param wait - Tempo de espera em ms
 * @returns Função debounced
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function
 * @param func - Função a ser throttled
 * @param limit - Limite de tempo em ms
 * @returns Função throttled
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

/**
 * Hook para debounce
 * @param value - Valor a ser debounced
 * @param delay - Delay em ms
 * @returns Valor debounced
 */
export function useDebounceValue<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook para throttle
 * @param value - Valor a ser throttled
 * @param limit - Limite em ms
 * @returns Valor throttled
 */
export function useThrottleValue<T>(value: T, limit: number = 300): T {
  const [throttledValue, setThrottledValue] = useState<T>(value);
  const lastRan = useRef<number>(Date.now());

  useEffect(() => {
    const handler = setTimeout(() => {
      if (Date.now() - lastRan.current >= limit) {
        setThrottledValue(value);
        lastRan.current = Date.now();
      }
    }, limit - (Date.now() - lastRan.current));

    return () => {
      clearTimeout(handler);
    };
  }, [value, limit]);

  return throttledValue;
}

/**
 * Otimiza componente pesado com memo
 * @param Component - Componente a ser otimizado
 * @param propsAreEqual - Função de comparação customizada
 * @returns Componente memoizado
 */
export function optimizeComponent<P extends object>(
  Component: ComponentType<P>,
  propsAreEqual?: (prevProps: P, nextProps: P) => boolean
): MemoExoticComponent<ComponentType<P>> {
  return memo(Component, propsAreEqual) as MemoExoticComponent<ComponentType<P>>;
}

/**
 * Lazy load de imagens
 * @param src - URL da imagem
 * @param placeholder - Placeholder enquanto carrega
 * @returns Hook que retorna se a imagem está carregada
 */
export function useLazyImage(src: string, placeholder?: string): {
  src: string;
  isLoading: boolean;
  error: Error | null;
} {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const img = new Image();
    img.src = src;

    img.onload = () => {
      setIsLoading(false);
      setError(null);
    };

    img.onerror = () => {
      setIsLoading(false);
      setError(new Error(`Failed to load image: ${src}`));
    };

    return () => {
      img.onload = null;
      img.onerror = null;
    };
  }, [src]);

  return {
    src: isLoading && placeholder ? placeholder : src,
    isLoading,
    error,
  };
}
