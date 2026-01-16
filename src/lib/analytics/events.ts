// src/lib/analytics/events.ts
/**
 * Eventos de Analytics
 * Mapeamento de todos os eventos rastreados na aplicação
 */

export type AnalyticsEvent =
  | DashboardViewedEvent
  | DashboardPeriodChangedEvent
  | DataExportedEvent
  | SearchPerformedEvent
  | ChartInteractedEvent
  | ErrorOccurredEvent
  | FeatureUsedEvent;

export interface DashboardViewedEvent {
  type: 'dashboard_viewed';
  dashboard: string;
  timestamp: number;
  userId?: string;
}

export interface DashboardPeriodChangedEvent {
  type: 'dashboard_period_changed';
  dashboard: string;
  period: string;
  startDate: string;
  endDate: string;
  timestamp: number;
}

export interface DataExportedEvent {
  type: 'data_exported';
  dashboard: string;
  format: 'pdf' | 'excel' | 'csv';
  timestamp: number;
}

export interface SearchPerformedEvent {
  type: 'search_performed';
  query: string;
  resultsCount: number;
  timestamp: number;
}

export interface ChartInteractedEvent {
  type: 'chart_interacted';
  dashboard: string;
  chartType: 'line' | 'bar' | 'pie';
  interaction: 'zoom' | 'filter' | 'legend_click' | 'data_point_click';
  timestamp: number;
}

export interface ErrorOccurredEvent {
  type: 'error_occurred';
  errorType: string;
  message: string;
  component?: string;
  timestamp: number;
}

export interface FeatureUsedEvent {
  type: 'feature_used';
  feature: string;
  context?: Record<string, unknown>;
  timestamp: number;
}

/**
 * Função para rastrear eventos de analytics
 */
export function trackEvent(event: AnalyticsEvent) {
  // Em produção, enviar para serviço de analytics
  if (process.env.NODE_ENV === 'production') {
    // Exemplo: Google Analytics 4
    // if (typeof window !== 'undefined' && window.gtag) {
    //   window.gtag('event', event.type, {
    //     ...event,
    //   });
    // }

    // Exemplo: PostHog
    // if (typeof window !== 'undefined' && window.posthog) {
    //   window.posthog.capture(event.type, event);
    // }

    // Exemplo: Custom analytics endpoint
    // fetch('/api/analytics', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(event),
    // }).catch(() => {}); // Fail silently
  }

  // Log em desenvolvimento
  if (process.env.NODE_ENV === 'development') {
    console.log('[Analytics Event]', event);
  }
}

/**
 * Helpers para eventos comuns
 */
export const analytics = {
  dashboardViewed: (dashboard: string, userId?: string) => {
    trackEvent({
      type: 'dashboard_viewed',
      dashboard,
      timestamp: Date.now(),
      userId,
    });
  },

  dashboardPeriodChanged: (
    dashboard: string,
    period: string,
    startDate: string,
    endDate: string
  ) => {
    trackEvent({
      type: 'dashboard_period_changed',
      dashboard,
      period,
      startDate,
      endDate,
      timestamp: Date.now(),
    });
  },

  dataExported: (dashboard: string, format: 'pdf' | 'excel' | 'csv') => {
    trackEvent({
      type: 'data_exported',
      dashboard,
      format,
      timestamp: Date.now(),
    });
  },

  searchPerformed: (query: string, resultsCount: number) => {
    trackEvent({
      type: 'search_performed',
      query,
      resultsCount,
      timestamp: Date.now(),
    });
  },

  chartInteracted: (
    dashboard: string,
    chartType: 'line' | 'bar' | 'pie',
    interaction: 'zoom' | 'filter' | 'legend_click' | 'data_point_click'
  ) => {
    trackEvent({
      type: 'chart_interacted',
      dashboard,
      chartType,
      interaction,
      timestamp: Date.now(),
    });
  },

  errorOccurred: (errorType: string, message: string, component?: string) => {
    trackEvent({
      type: 'error_occurred',
      errorType,
      message,
      component,
      timestamp: Date.now(),
    });
  },

  featureUsed: (feature: string, context?: Record<string, unknown>) => {
    trackEvent({
      type: 'feature_used',
      feature,
      context,
      timestamp: Date.now(),
    });
  },
};
