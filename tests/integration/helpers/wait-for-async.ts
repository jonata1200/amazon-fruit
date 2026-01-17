// tests/integration/helpers/wait-for-async.ts
import { waitFor } from '@testing-library/react';

/**
 * Aguarda até que uma condição assíncrona seja satisfeita
 * Útil para testes de integração que envolvem múltiplas atualizações de estado
 */
export async function waitForAsync(
  condition: () => boolean | Promise<boolean>,
  options?: { timeout?: number; interval?: number }
) {
  const { timeout = 5000, interval = 100 } = options || {};
  
  return waitFor(
    async () => {
      const result = await condition();
      if (!result) {
        throw new Error('Condition not met');
      }
      return result;
    },
    { timeout, interval }
  );
}

/**
 * Aguarda até que um elemento apareça no DOM
 */
export async function waitForElement(
  queryFn: () => HTMLElement | null,
  options?: { timeout?: number }
) {
  return waitFor(
    () => {
      const element = queryFn();
      if (!element) {
        throw new Error('Element not found');
      }
      return element;
    },
    { timeout: options?.timeout || 5000 }
  );
}

/**
 * Aguarda até que um texto apareça no DOM
 */
export async function waitForText(
  text: string | RegExp,
  container?: HTMLElement,
  options?: { timeout?: number }
) {
  return waitFor(
    () => {
      const query = container
        ? container.textContent || ''
        : document.body.textContent || '';
      
      const found = typeof text === 'string'
        ? query.includes(text)
        : text.test(query);
      
      if (!found) {
        throw new Error(`Text "${text}" not found`);
      }
      return true;
    },
    { timeout: options?.timeout || 5000 }
  );
}
