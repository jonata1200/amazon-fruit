// src/types/common.ts

/**
 * Branded Types
 * Types marcados para evitar confusão entre tipos semelhantes
 */

export type DashboardId = string & { readonly __brand: 'DashboardId' };

export type ISODate = string & { readonly __brand: 'ISODate' };

export type DateRange = {
  start: ISODate;
  end: ISODate;
};

/**
 * Type helpers para criar branded types
 */
export function createDashboardId(id: string): DashboardId {
  return id as DashboardId;
}

export function createISODate(date: string): ISODate {
  // Validar formato ISO 8601 básico
  if (!/^\d{4}-\d{2}-\d{2}/.test(date)) {
    throw new Error(`Invalid ISO date format: ${date}`);
  }
  return date as ISODate;
}

/**
 * Discriminated Unions para estados de API
 */
export type ApiState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

/**
 * Type guard para verificar se ApiState é success
 */
export function isApiSuccess<T>(state: ApiState<T>): state is { status: 'success'; data: T } {
  return state.status === 'success';
}

/**
 * Type guard para verificar se ApiState é error
 */
export function isApiError<T>(state: ApiState<T>): state is { status: 'error'; error: Error } {
  return state.status === 'error';
}

/**
 * Type guard para verificar se ApiState está loading
 */
export function isApiLoading<T>(state: ApiState<T>): state is { status: 'loading' } {
  return state.status === 'loading';
}
