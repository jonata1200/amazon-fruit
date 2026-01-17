// tests/unit/lib/utils/formatters.test.ts
import {
  formatCurrency,
  formatNumber,
  formatPercentage,
  formatDate,
  formatDateLong,
  formatDateShort,
} from '@/lib/utils/formatters';

describe('formatters', () => {
  describe('formatCurrency', () => {
    it('formats number as currency', () => {
      expect(formatCurrency(1000)).toContain('1.000');
      expect(formatCurrency(1000)).toContain('R$');
    });

    it('formats decimal values', () => {
      expect(formatCurrency(1234.56)).toContain('1.234,56');
    });

    it('formats zero', () => {
      expect(formatCurrency(0)).toContain('0,00');
    });

    it('formats negative values', () => {
      const result = formatCurrency(-1000);
      // Formato esperado: -R$ 1.000,00
      expect(result).toContain('-');
      expect(result).toContain('1.000');
      expect(result).toContain('R$');
    });
  });

  describe('formatNumber', () => {
    it('formats number with default decimals', () => {
      expect(formatNumber(1000)).toBe('1.000');
    });

    it('formats number with custom decimals', () => {
      expect(formatNumber(1234.567, 2)).toBe('1.234,57');
      expect(formatNumber(1234.567, 0)).toBe('1.235');
    });

    it('formats zero', () => {
      expect(formatNumber(0)).toBe('0');
    });
  });

  describe('formatPercentage', () => {
    it('formats percentage with default decimals', () => {
      expect(formatPercentage(15.5)).toBe('15,5%');
    });

    it('formats percentage with custom decimals', () => {
      expect(formatPercentage(15.567, 2)).toBe('15,57%');
    });

    it('formats zero percentage', () => {
      expect(formatPercentage(0)).toBe('0,0%');
    });
  });

  describe('formatDate', () => {
    it('formats date string', () => {
      const result = formatDate('2024-01-15');
      // Pode variar devido a timezone, então verificamos apenas estrutura básica
      expect(result).toMatch(/\d{2}\/\d{2}\/\d{4}/);
      expect(result).toContain('2024');
    });

    it('formats Date object', () => {
      const date = new Date('2024-01-15T12:00:00');
      const result = formatDate(date);
      // Pode variar devido a timezone
      expect(result).toMatch(/\d{2}\/\d{2}\/\d{4}/);
      expect(result).toContain('2024');
    });
  });

  describe('formatDateLong', () => {
    it('formats date in long format', () => {
      const result = formatDateLong('2024-01-15');
      // Pode variar devido a timezone, mas deve conter mês e ano
      expect(result).toContain('janeiro');
      expect(result).toContain('2024');
      // Deve ter um número de dia (pode ser 14 ou 15 dependendo do timezone)
      expect(result).toMatch(/\d{1,2}/);
    });
  });

  describe('formatDateShort', () => {
    it('formats date in short format', () => {
      const result = formatDateShort('2024-01-15');
      // Pode variar devido a timezone (pode ser 14 ou 15)
      expect(result).toMatch(/\d{2}\/\d{2}\/\d{2}/);
      expect(result).toContain('01');
      expect(result).toContain('24');
    });
  });
});
