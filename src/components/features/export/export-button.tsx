// src/components/features/export/export-button.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { FileDown, Loader2 } from 'lucide-react';
import { useNotifications } from '@/lib/hooks/useNotifications';
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
  const { showSuccess, showError } = useNotifications();

  const handleExport = async (format: 'pdf' | 'excel' | 'csv') => {
    setIsExporting(true);
    try {
      // Simular exportação por enquanto
      await new Promise((resolve) => setTimeout(resolve, 1500));

      // Em produção, fazer chamada real para API:
      // const blob = await exportService.exportDashboard(dashboard, format);
      // const url = window.URL.createObjectURL(blob);
      // const a = document.createElement('a');
      // a.href = url;
      // a.download = `${dashboard}_${new Date().toISOString()}.${format}`;
      // a.click();

      showSuccess(`Relatório de ${dashboard} exportado em ${format.toUpperCase()} com sucesso!`);
    } catch (error) {
      console.error('Export error:', error);
      showError('Erro ao exportar relatório');
    } finally {
      setIsExporting(false);
    }
  };

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
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => handleExport('pdf')}>Exportar como PDF</DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport('excel')}>
          Exportar como Excel
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport('csv')}>Exportar como CSV</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
