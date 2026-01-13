// src/components/features/alerts/alerts-panel.tsx
'use client';

import { useAlerts } from '@/lib/hooks/useAlerts';
import { useAppStore } from '@/store';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { X, AlertTriangle, XCircle, Info, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Skeleton } from '@/components/ui/skeleton';

const alertIcons = {
  warning: AlertTriangle,
  danger: XCircle,
  info: Info,
  success: CheckCircle,
};

const alertColors = {
  warning: 'border-l-yellow-600 bg-yellow-50 dark:bg-yellow-900/20',
  danger: 'border-l-red-600 bg-red-50 dark:bg-red-900/20',
  info: 'border-l-blue-600 bg-blue-50 dark:bg-blue-900/20',
  success: 'border-l-green-600 bg-green-50 dark:bg-green-900/20',
};

const iconColors = {
  warning: 'text-yellow-600',
  danger: 'text-red-600',
  info: 'text-blue-600',
  success: 'text-green-600',
};

function AlertsPanelSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((i) => (
        <Skeleton key={i} className="h-24" />
      ))}
    </div>
  );
}

export function AlertsPanel() {
  const alertsOpen = useAppStore((state) => state.alertsOpen);
  const toggleAlerts = useAppStore((state) => state.toggleAlerts);
  const { data, isLoading } = useAlerts();

  if (!alertsOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md border-l bg-background shadow-lg">
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex items-center justify-between border-b p-4">
          <h2 className="text-lg font-semibold">Alertas do Sistema</h2>
          <Button variant="ghost" size="icon" onClick={toggleAlerts}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {isLoading ? (
            <AlertsPanelSkeleton />
          ) : data && data.alerts.length > 0 ? (
            <div className="space-y-3">
              {data.alerts.map((alert) => {
                const Icon = alertIcons[alert.type];
                return (
                  <Card key={alert.id} className={cn('border-l-4', alertColors[alert.type])}>
                    <CardContent className="flex gap-3 p-4">
                      <Icon className={cn('h-5 w-5 flex-shrink-0', iconColors[alert.type])} />
                      <div className="flex-1">
                        <p className="font-medium">{alert.category}</p>
                        <p className="text-sm text-muted-foreground">{alert.message}</p>
                        {alert.timestamp && (
                          <p className="mt-1 text-xs text-muted-foreground">
                            {new Date(alert.timestamp).toLocaleString('pt-BR')}
                          </p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          ) : (
            <div className="flex h-full items-center justify-center">
              <div className="text-center text-muted-foreground">
                <CheckCircle className="mx-auto h-12 w-12 mb-2" />
                <p>Nenhum alerta no momento</p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        {data && data.count > 0 && (
          <div className="border-t p-4">
            <p className="text-center text-sm text-muted-foreground">
              Total: {data.count} {data.count === 1 ? 'alerta' : 'alertas'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
