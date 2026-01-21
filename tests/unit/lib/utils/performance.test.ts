/**
 * Testes para utilitários de performance
 */

import { debounce, throttle } from '@/lib/utils/performance';

describe('Performance Utils', () => {
  describe('debounce', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('deve executar função após delay', () => {
      const fn = jest.fn();
      const debouncedFn = debounce(fn, 300);

      debouncedFn();
      expect(fn).not.toHaveBeenCalled();

      jest.advanceTimersByTime(300);
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('deve cancelar execução anterior se chamado novamente', () => {
      const fn = jest.fn();
      const debouncedFn = debounce(fn, 300);

      debouncedFn();
      debouncedFn();
      debouncedFn();

      jest.advanceTimersByTime(300);
      expect(fn).toHaveBeenCalledTimes(1);
    });
  });

  describe('throttle', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('deve executar função imediatamente', () => {
      const fn = jest.fn();
      const throttledFn = throttle(fn, 300);

      throttledFn();
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('deve limitar execuções dentro do período', () => {
      const fn = jest.fn();
      const throttledFn = throttle(fn, 300);

      throttledFn();
      throttledFn();
      throttledFn();

      expect(fn).toHaveBeenCalledTimes(1);

      jest.advanceTimersByTime(300);
      throttledFn();
      expect(fn).toHaveBeenCalledTimes(2);
    });
  });
});
