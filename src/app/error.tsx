// src/app/error.tsx
'use client';

import { useEffect } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log do erro (em produção, enviar para serviço de monitoramento)
    console.error('Página de erro capturou:', error);

    // Em produção, integrar com serviço de monitoramento
    if (process.env.NODE_ENV === 'production' && typeof window !== 'undefined') {
      import('@sentry/nextjs').then((Sentry) => {
        Sentry.captureException(error);
      }).catch(() => {
        // Falha silenciosamente se Sentry não estiver configurado
      });
    }
  }, [error]);

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
            <CardTitle className="text-xl">Erro inesperado</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            Ocorreu um erro inesperado. Por favor, tente novamente.
          </p>

          {process.env.NODE_ENV === 'development' && (
            <details className="rounded-md border p-3 text-sm">
              <summary className="cursor-pointer font-medium text-destructive mb-2">
                Detalhes do erro (desenvolvimento)
              </summary>
              <pre className="mt-2 overflow-auto text-xs">
                {error.message}
                {error.digest && `\nDigest: ${error.digest}`}
              </pre>
            </details>
          )}

          <div className="flex gap-2 flex-wrap">
            <Button onClick={reset} variant="default">
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
