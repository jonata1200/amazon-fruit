// tests/unit/lib/utils/validators.test.ts
import { isValidDate, isValidDateRange, isValidEmail } from '@/lib/utils/validators';

describe('validators', () => {
  describe('isValidDate', () => {
    it('returns true for valid date string', () => {
      expect(isValidDate('2024-01-15')).toBe(true);
      expect(isValidDate('2024-12-31')).toBe(true);
    });

    it('returns false for invalid format', () => {
      expect(isValidDate('2024/01/15')).toBe(false);
      expect(isValidDate('15-01-2024')).toBe(false);
      expect(isValidDate('2024-1-15')).toBe(false);
    });

    it('returns false for invalid date', () => {
      expect(isValidDate('2024-13-01')).toBe(false);
      expect(isValidDate('2024-02-30')).toBe(false);
    });

    it('returns false for empty string', () => {
      expect(isValidDate('')).toBe(false);
    });
  });

  describe('isValidDateRange', () => {
    it('returns true when start is before end', () => {
      expect(isValidDateRange('2024-01-01', '2024-01-31')).toBe(true);
    });

    it('returns true when start equals end', () => {
      expect(isValidDateRange('2024-01-15', '2024-01-15')).toBe(true);
    });

    it('returns false when start is after end', () => {
      expect(isValidDateRange('2024-01-31', '2024-01-01')).toBe(false);
    });

    it('returns false when start date is invalid', () => {
      expect(isValidDateRange('invalid', '2024-01-31')).toBe(false);
    });

    it('returns false when end date is invalid', () => {
      expect(isValidDateRange('2024-01-01', 'invalid')).toBe(false);
    });
  });

  describe('isValidEmail', () => {
    it('returns true for valid email', () => {
      expect(isValidEmail('test@example.com')).toBe(true);
      expect(isValidEmail('user.name@domain.co.uk')).toBe(true);
    });

    it('returns false for invalid email', () => {
      expect(isValidEmail('invalid')).toBe(false);
      expect(isValidEmail('invalid@')).toBe(false);
      expect(isValidEmail('@example.com')).toBe(false);
      expect(isValidEmail('invalid@.com')).toBe(false);
    });

    it('returns false for empty string', () => {
      expect(isValidEmail('')).toBe(false);
    });
  });
});
