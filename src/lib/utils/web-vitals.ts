// src/lib/utils/web-vitals.ts
import type { NextWebVitalsMetric } from 'next/app';

export function reportWebVitals(metric: NextWebVitalsMetric) {
  // Em produção, enviar para analytics/monitoramento
  if (process.env.NODE_ENV === 'production') {
    // Exemplo: Enviar para Google Analytics, Sentry, ou outro serviço
    // gtag('event', metric.name, {
    //   value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    //   event_label: metric.id,
    //   non_interaction: true,
    // });

    // Exemplo: Enviar para Sentry
    // Sentry.metrics.distribution(metric.name, metric.value);
  }

  // Log em desenvolvimento
  if (process.env.NODE_ENV === 'development') {
    console.log('[Web Vitals]', metric.name, metric.value, metric.id);
  }

  // Thresholds para métricas importantes
  const thresholds: Record<string, { good: number; needsImprovement: number }> = {
    FCP: { good: 1800, needsImprovement: 3000 }, // First Contentful Paint
    LCP: { good: 2500, needsImprovement: 4000 }, // Largest Contentful Paint
    CLS: { good: 0.1, needsImprovement: 0.25 }, // Cumulative Layout Shift
    FID: { good: 100, needsImprovement: 300 }, // First Input Delay
    TTFB: { good: 800, needsImprovement: 1800 }, // Time to First Byte
  };

  const threshold = thresholds[metric.name];
  if (threshold) {
    if (metric.value > threshold.needsImprovement) {
      console.warn(
        `[Web Vitals Warning] ${metric.name} is ${metric.value.toFixed(2)}ms, needs improvement (threshold: ${threshold.needsImprovement}ms)`
      );
    } else if (metric.value > threshold.good) {
      console.info(
        `[Web Vitals Info] ${metric.name} is ${metric.value.toFixed(2)}ms, could be improved (good: ${threshold.good}ms)`
      );
    }
  }
}
