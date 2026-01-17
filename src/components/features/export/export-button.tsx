// src/components/features/export/export-button.tsx
'use client';

import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { FileDown, Loader2 } from 'lucide-react';
import { useNotifications } from '@/lib/hooks/useNotifications';
import { analytics } from '@/lib/analytics/events';
import { Progress } from '@/components/ui/progress';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface ExportButtonProps {
  dashboard: string;
}

export function ExportButton({ dashboard }: ExportButtonProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [progress, setProgress] = useState(0);
  const { showSuccess, showError } = useNotifications();

  const handleExport = useCallback(async (format: 'pdf' | 'excel' | 'csv') => {
    setIsExporting(true);
    setProgress(0);
    
    try {
      // Simular exportação com progresso
      const steps = 10;
      for (let i = 0; i <= steps; i++) {
        await new Promise((resolve) => setTimeout(resolve, 150));
        setProgress((i / steps) * 100);
      }

      // Em produção, fazer chamada real para API:
      // const blob = await exportService.exportDashboard(dashboard, format);
      // const url = window.URL.createObjectURL(blob);
      // const a = document.createElement('a');
      // a.href = url;
      // a.download = `${dashboard}_${new Date().toISOString()}.${format}`;
      // a.click();

      showSuccess(`Relatório de ${dashboard} exportado em ${format.toUpperCase()} com sucesso!`);
      analytics.dataExported(dashboard, format);
    } catch (error) {
      console.error('Export error:', error);
      showError('Erro ao exportar relatório');
    } finally {
      setIsExporting(false);
      setProgress(0);
    }
  }, [dashboard, showSuccess, showError]);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" disabled={isExporting} aria-label="Exportar relatório">
          {isExporting ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Exportando...
            </>
          ) : (
            <>
              <FileDown className="mr-2 h-4 w-4" />
              Exportar
            </>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        {isExporting && (
          <div className="px-2 py-2">
            <Progress value={progress} showLabel className="mb-2" />
            <p className="text-xs text-muted-foreground">Exportando... {Math.round(progress)}%</p>
          </div>
        )}
        <DropdownMenuItem onClick={() => handleExport('pdf')} disabled={isExporting}>
          Exportar como PDF
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport('excel')} disabled={isExporting}>
          Exportar como Excel
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport('csv')} disabled={isExporting}>
          Exportar como CSV
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
