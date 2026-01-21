/**
 * Testes para funções de transformação de tokens
 */

import {
  spacingToTailwindClass,
  shadowToTailwindClass,
  radiusToTailwindClass,
  tokensToTailwindClasses,
  normalizeTokenValue,
} from '@/lib/utils/transformations';

describe('Transformations', () => {
  describe('spacingToTailwindClass', () => {
    it('deve converter espaçamento para classe Tailwind', () => {
      expect(spacingToTailwindClass(4, 'p')).toBe('p-4');
      expect(spacingToTailwindClass(6, 'm')).toBe('m-6');
      expect(spacingToTailwindClass(2, 'gap')).toBe('gap-2');
    });

    it('deve usar valor padrão se não encontrado', () => {
      // @ts-expect-error - Testando comportamento com valor inválido
      expect(spacingToTailwindClass('invalid' as any, 'p')).toBe('p-4');
    });
  });

  describe('shadowToTailwindClass', () => {
    it('deve converter sombra para classe Tailwind', () => {
      expect(shadowToTailwindClass('sm')).toBe('shadow-sm');
      expect(shadowToTailwindClass('md')).toBe('shadow-md');
      expect(shadowToTailwindClass('lg')).toBe('shadow-lg');
      expect(shadowToTailwindClass('none')).toBe('shadow-none');
    });
  });

  describe('radiusToTailwindClass', () => {
    it('deve converter border radius para classe Tailwind', () => {
      expect(radiusToTailwindClass('sm')).toBe('rounded-sm');
      expect(radiusToTailwindClass('md')).toBe('rounded-md');
      expect(radiusToTailwindClass('lg')).toBe('rounded-lg');
      expect(radiusToTailwindClass('full')).toBe('rounded-full');
    });
  });

  describe('tokensToTailwindClasses', () => {
    it('deve combinar múltiplos tokens em classes', () => {
      const classes = tokensToTailwindClasses({
        padding: 4,
        gap: 2,
        shadow: 'base',
        radius: 'md',
      });

      expect(classes).toContain('p-4');
      expect(classes).toContain('gap-2');
      expect(classes).toContain('shadow');
      expect(classes).toContain('rounded-md');
    });

    it('deve retornar string vazia se nenhum token fornecido', () => {
      expect(tokensToTailwindClasses({})).toBe('');
    });
  });

  describe('normalizeTokenValue', () => {
    it('deve normalizar valor de cor válido', () => {
      expect(normalizeTokenValue('#9333ea', 'color')).toBe('#9333ea');
    });

    it('deve retornar valor padrão para cor inválida', () => {
      expect(normalizeTokenValue('invalid', 'color')).toBeTruthy();
    });

    it('deve normalizar valor de espaçamento válido', () => {
      expect(normalizeTokenValue('1rem', 'spacing')).toBe('1rem');
      expect(normalizeTokenValue('16px', 'spacing')).toBe('16px');
    });

    it('deve normalizar valor de sombra', () => {
      expect(normalizeTokenValue('none', 'shadow')).toBe('none');
      expect(normalizeTokenValue('0 1px 2px rgb(0 0 0 / 0.05)', 'shadow')).toBeTruthy();
    });

    it('deve normalizar valor de border radius', () => {
      expect(normalizeTokenValue('0.5rem', 'radius')).toBe('0.5rem');
      expect(normalizeTokenValue('9999px', 'radius')).toBe('9999px');
    });
  });
});
