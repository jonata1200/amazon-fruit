/**
 * Utilitários de Desenvolvimento
 * Helpers para logging, debugging e validação (apenas em modo desenvolvimento)
 */

/**
 * Logger para desenvolvimento
 * Só funciona em modo desenvolvimento
 */
export const devLogger = {
  log: (...args: any[]) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('[DEV]', ...args);
    }
  },
  warn: (...args: any[]) => {
    if (process.env.NODE_ENV === 'development') {
      console.warn('[DEV WARN]', ...args);
    }
  },
  error: (...args: any[]) => {
    if (process.env.NODE_ENV === 'development') {
      console.error('[DEV ERROR]', ...args);
    }
  },
  group: (label: string, fn: () => void) => {
    if (process.env.NODE_ENV === 'development') {
      console.group(`[DEV] ${label}`);
      fn();
      console.groupEnd();
    }
  },
  table: (data: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.table(data);
    }
  },
};

/**
 * Valida props de componente em desenvolvimento
 * @param componentName - Nome do componente
 * @param props - Props a serem validadas
 * @param schema - Schema de validação
 */
export function validateProps<T extends Record<string, any>>(
  componentName: string,
  props: T,
  schema: Record<keyof T, (value: any) => boolean>
): void {
  if (process.env.NODE_ENV !== 'development') {
    return;
  }

  Object.entries(schema).forEach(([key, validator]) => {
    const value = props[key];
    if (value !== undefined && !validator(value)) {
      devLogger.warn(
        `[${componentName}] Prop "${key}" has invalid value:`,
        value
      );
    }
  });
}

/**
 * Debug helper para inspecionar valores
 * @param label - Label para identificação
 * @param value - Valor a ser inspecionado
 * @returns Valor original (não modifica)
 */
export function debugValue<T>(label: string, value: T): T {
  if (process.env.NODE_ENV === 'development') {
    devLogger.group(`Debug: ${label}`, () => {
      console.log('Value:', value);
      console.log('Type:', typeof value);
      if (typeof value === 'object' && value !== null) {
        console.log('Keys:', Object.keys(value));
      }
    });
  }
  return value;
}

/**
 * Mede performance de função
 * @param label - Label para identificação
 * @param fn - Função a ser medida
 * @returns Resultado da função
 */
export function measurePerformance<T>(
  label: string,
  fn: () => T
): T {
  if (process.env.NODE_ENV !== 'development') {
    return fn();
  }

  const start = performance.now();
  const result = fn();
  const end = performance.now();
  const duration = end - start;

  devLogger.log(`[Performance] ${label}: ${duration.toFixed(2)}ms`);

  if (duration > 16) {
    devLogger.warn(`[Performance] ${label} took longer than 16ms (frame budget)`);
  }

  return result;
}

/**
 * Warning para props deprecadas
 * @param componentName - Nome do componente
 * @param deprecatedProps - Props deprecadas
 * @param replacement - Props de substituição
 */
export function warnDeprecatedProps(
  componentName: string,
  deprecatedProps: string[],
  replacement?: Record<string, string>
): void {
  if (process.env.NODE_ENV !== 'development') {
    return;
  }

  deprecatedProps.forEach((prop) => {
    devLogger.warn(
      `[${componentName}] Prop "${prop}" is deprecated.`,
      replacement?.[prop] ? `Use "${replacement[prop]}" instead.` : ''
    );
  });
}

/**
 * Validação de design tokens em desenvolvimento
 * @param tokenPath - Caminho do token
 * @param value - Valor do token
 */
export function validateToken(
  tokenPath: string,
  value: unknown
): boolean {
  if (process.env.NODE_ENV !== 'development') {
    return true;
  }

  if (value === undefined || value === null) {
    devLogger.warn(`[Token Validation] Token "${tokenPath}" is undefined or null`);
    return false;
  }

  return true;
}

/**
 * Helper para debug de re-renders
 * @param componentName - Nome do componente
 * @param props - Props do componente
 */
export function debugRenders(
  componentName: string,
  props?: Record<string, any>
): void {
  if (process.env.NODE_ENV !== 'development') {
    return;
  }

  devLogger.log(`[Render] ${componentName}`, props ? { props } : '');
}
