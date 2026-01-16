// src/lib/hooks/__tests__/useFavorites.test.ts
import { renderHook, act } from '@testing-library/react';
import { useFavorites } from '../useFavorites';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('useFavorites', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  it('should initialize with empty favorites', () => {
    const { result } = renderHook(() => useFavorites());

    expect(result.current.favorites).toEqual([]);
  });

  it('should load favorites from localStorage', () => {
    localStorageMock.setItem('amazon-fruit-favorites', JSON.stringify(['geral', 'financas']));

    const { result } = renderHook(() => useFavorites());

    expect(result.current.favorites).toEqual(['geral', 'financas']);
  });

  it('should add favorite', () => {
    const { result } = renderHook(() => useFavorites());

    act(() => {
      result.current.addFavorite('geral');
    });

    expect(result.current.favorites).toContain('geral');
    expect(result.current.isFavorite('geral')).toBe(true);
  });

  it('should remove favorite', () => {
    const { result } = renderHook(() => useFavorites());

    act(() => {
      result.current.addFavorite('geral');
      result.current.removeFavorite('geral');
    });

    expect(result.current.favorites).not.toContain('geral');
    expect(result.current.isFavorite('geral')).toBe(false);
  });

  it('should toggle favorite', () => {
    const { result } = renderHook(() => useFavorites());

    act(() => {
      result.current.toggleFavorite('geral');
    });

    expect(result.current.isFavorite('geral')).toBe(true);

    act(() => {
      result.current.toggleFavorite('geral');
    });

    expect(result.current.isFavorite('geral')).toBe(false);
  });
});
