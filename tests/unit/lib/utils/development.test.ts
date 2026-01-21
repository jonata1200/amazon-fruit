/**
 * Testes para utilitários de desenvolvimento
 */

import { devLogger, validateProps, debugValue, measurePerformance } from '@/lib/utils/development';

describe('Development Utils', () => {
  const originalEnv = process.env.NODE_ENV;
  const consoleSpy = {
    log: jest.spyOn(console, 'log').mockImplementation(),
    warn: jest.spyOn(console, 'warn').mockImplementation(),
    error: jest.spyOn(console, 'error').mockImplementation(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterAll(() => {
    process.env.NODE_ENV = originalEnv;
    consoleSpy.log.mockRestore();
    consoleSpy.warn.mockRestore();
    consoleSpy.error.mockRestore();
  });

  describe('devLogger', () => {
    it('deve logar apenas em desenvolvimento', () => {
      process.env.NODE_ENV = 'development';
      devLogger.log('test');
      expect(consoleSpy.log).toHaveBeenCalled();

      process.env.NODE_ENV = 'production';
      devLogger.log('test');
      expect(consoleSpy.log).toHaveBeenCalledTimes(1);
    });

    it('deve logar warnings', () => {
      process.env.NODE_ENV = 'development';
      devLogger.warn('warning');
      expect(consoleSpy.warn).toHaveBeenCalled();
    });

    it('deve logar errors', () => {
      process.env.NODE_ENV = 'development';
      devLogger.error('error');
      expect(consoleSpy.error).toHaveBeenCalled();
    });
  });

  describe('validateProps', () => {
    it('deve validar props em desenvolvimento', () => {
      process.env.NODE_ENV = 'development';
      
      validateProps('TestComponent', { value: 'test', count: 5 }, {
        value: (v) => typeof v === 'string',
        count: (c) => typeof c === 'number' && c >= 0,
      });

      // Não deve ter warnings para props válidas
      expect(consoleSpy.warn).not.toHaveBeenCalled();
    });

    it('deve avisar sobre props inválidas', () => {
      process.env.NODE_ENV = 'development';
      
      validateProps('TestComponent', { value: 123 }, {
        value: (v) => typeof v === 'string',
      });

      expect(consoleSpy.warn).toHaveBeenCalled();
    });

    it('não deve validar em produção', () => {
      process.env.NODE_ENV = 'production';
      
      validateProps('TestComponent', { value: 123 }, {
        value: (v) => typeof v === 'string',
      });

      expect(consoleSpy.warn).not.toHaveBeenCalled();
    });
  });

  describe('debugValue', () => {
    it('deve retornar valor original', () => {
      const value = { test: 'value' };
      const result = debugValue('test', value);
      expect(result).toBe(value);
    });
  });

  describe('measurePerformance', () => {
    it('deve executar função e medir tempo', () => {
      process.env.NODE_ENV = 'development';
      const fn = jest.fn(() => 'result');
      
      const result = measurePerformance('test', fn);
      
      expect(fn).toHaveBeenCalled();
      expect(result).toBe('result');
      expect(consoleSpy.log).toHaveBeenCalled();
    });

    it('deve executar função normalmente em produção', () => {
      process.env.NODE_ENV = 'production';
      const fn = jest.fn(() => 'result');
      
      const result = measurePerformance('test', fn);
      
      expect(fn).toHaveBeenCalled();
      expect(result).toBe('result');
      expect(consoleSpy.log).not.toHaveBeenCalled();
    });
  });
});
