/**
 * Testes para validação de design tokens
 */

import { validateTokens } from '@/scripts/validate-tokens';
import { getColor, getSpacing, getTypography } from '@/lib/utils/design-tokens';
import { tokens } from '@/lib/design-tokens';

describe('Design Tokens Validation', () => {
  describe('validateTokens', () => {
    it('deve validar tokens corretamente', () => {
      const result = validateTokens();
      
      expect(result).toHaveProperty('passed');
      expect(result).toHaveProperty('errors');
      expect(result).toHaveProperty('warnings');
      expect(typeof result.passed).toBe('boolean');
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });

    it('deve passar validação básica de tokens', () => {
      const result = validateTokens();
      
      // Não deve ter erros críticos
      expect(result.errors.length).toBe(0);
    });
  });

  describe('getColor', () => {
    it('deve retornar cor válida', () => {
      const color = getColor('primary', 600);
      expect(color).toMatch(/^#[0-9a-fA-F]{6}$/);
    });

    it('deve retornar cor padrão se não encontrada', () => {
      // @ts-expect-error - Testando comportamento com cor inválida
      const color = getColor('invalid' as any, 600);
      expect(color).toBeTruthy();
    });
  });

  describe('getSpacing', () => {
    it('deve retornar espaçamento válido', () => {
      const spacing = getSpacing('md');
      expect(spacing).toContain('rem');
    });

    it('deve retornar espaçamento padrão se não encontrado', () => {
      // @ts-expect-error - Testando comportamento com espaçamento inválido
      const spacing = getSpacing('invalid' as any);
      expect(spacing).toBeTruthy();
    });
  });

  describe('getTypography', () => {
    it('deve retornar fontSize válido', () => {
      const fontSize = getTypography('fontSize', 'base');
      expect(fontSize).toBeTruthy();
    });

    it('deve retornar fontWeight válido', () => {
      const fontWeight = getTypography('fontWeight', 'normal');
      expect(fontWeight).toBeTruthy();
    });
  });

  describe('Tokens Structure', () => {
    it('deve ter estrutura de cores válida', () => {
      expect(tokens.colors).toBeDefined();
      expect(tokens.colors.primary).toBeDefined();
      expect(tokens.colors.primary[600]).toBeDefined();
    });

    it('deve ter estrutura de espaçamento válida', () => {
      expect(tokens.spacing).toBeDefined();
      expect(tokens.spacing.semantic).toBeDefined();
      expect(tokens.spacing.semantic.md).toBeDefined();
    });

    it('deve ter estrutura de tipografia válida', () => {
      expect(tokens.typography).toBeDefined();
      expect(tokens.typography.fontSizes).toBeDefined();
      expect(tokens.typography.fontSizes.base).toBeDefined();
    });
  });
});
