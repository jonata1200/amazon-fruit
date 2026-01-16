// src/components/error-boundary.tsx
'use client';

import React from 'react';
import { ErrorBoundary as ReactErrorBoundary, FallbackProps } from 'react-error-boundary';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ErrorFallbackProps extends FallbackProps {
  title?: string;
  message?: string;
}

function ErrorFallback({ error, resetErrorBoundary, title, message }: ErrorFallbackProps) {
  const handleReload = () => {
    window.location.reload();
  };

  const handleGoHome = () => {
    window.location.href = '/';
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <div className="flex items-center gap-3">
            <AlertTriangle className="h-6 w-6 text-destructive" />
            <CardTitle className="text-xl">
              {title || 'Algo deu errado'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            {message || 'Ocorreu um erro inesperado. Por favor, tente novamente.'}
          </p>

          {process.env.NODE_ENV === 'development' && error && (
            <details className="rounded-md border p-3 text-sm">
              <summary className="cursor-pointer font-medium text-destructive mb-2">
                Detalhes do erro (desenvolvimento)
              </summary>
              <pre className="mt-2 overflow-auto text-xs">
                {error.message}
                {'\n'}
                {error.stack}
              </pre>
            </details>
          )}

          <div className="flex gap-2">
            <Button onClick={resetErrorBoundary} variant="default">
              <RefreshCw className="mr-2 h-4 w-4" />
              Tentar novamente
            </Button>
            <Button onClick={handleReload} variant="outline">
              <RefreshCw className="mr-2 h-4 w-4" />
              Recarregar página
            </Button>
            <Button onClick={handleGoHome} variant="ghost">
              <Home className="mr-2 h-4 w-4" />
              Ir para início
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<FallbackProps>;
  onError?: (error: Error, info: React.ErrorInfo) => void;
  resetKeys?: Array<string | number>;
  resetOnPropsChange?: boolean;
  title?: string;
  message?: string;
}

export function ErrorBoundary({
  children,
  fallback,
  onError,
  resetKeys,
  resetOnPropsChange,
  title,
  message,
}: ErrorBoundaryProps) {
  const handleError = (error: Error, info: React.ErrorInfo) => {
    // Log do erro (em produção, enviar para serviço de monitoramento)
    console.error('ErrorBoundary capturou um erro:', error, info);

    // Chamar callback customizado se fornecido
    if (onError) {
      onError(error, info);
    }

    // Em produção, integrar com serviço de monitoramento (Sentry, etc.)
    if (process.env.NODE_ENV === 'production' && typeof window !== 'undefined') {
      // Importação dinâmica para evitar erros em desenvolvimento
      import('@sentry/nextjs').then((Sentry) => {
        Sentry.captureException(error, { contexts: { react: info } });
      }).catch(() => {
        // Falha silenciosamente se Sentry não estiver configurado
      });
    }
  };

  const FallbackComponent = fallback || ((props: FallbackProps) => (
    <ErrorFallback {...props} title={title} message={message} />
  ));

  return (
    <ReactErrorBoundary
      FallbackComponent={FallbackComponent}
      onError={handleError}
      resetKeys={resetKeys}
      resetOnPropsChange={resetOnPropsChange}
    >
      {children}
    </ReactErrorBoundary>
  );
}
