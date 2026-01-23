/**
 * Componente Data Table - Tabelas de dados
 * Componente padronizado com design tokens, acessibilidade e variantes
 */

'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { EmptyState } from './empty-state';

// Variantes da tabela
const tableVariants = cva('w-full', {
  variants: {
    variant: {
      default: '',
      striped: '[&_tbody_tr:nth-child(even)]:bg-muted/50',
      bordered: 'border-collapse [&_td]:border [&_th]:border',
    },
    size: {
      sm: 'text-sm',
      md: 'text-base',
      lg: 'text-lg',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'md',
  },
});

export interface Column {
  key: string;
  header: string;
  render?: (value: unknown, row: Record<string, unknown>) => React.ReactNode;
  align?: 'left' | 'center' | 'right';
  width?: string;
}

export interface DataTableProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof tableVariants> {
  title?: string;
  columns: Column[];
  data: Record<string, unknown>[];
  loading?: boolean;
  emptyMessage?: string;
  showHeader?: boolean;
}

export function DataTable({ 
  title, 
  columns, 
  data, 
  className,
  variant,
  size,
  loading = false,
  emptyMessage = 'Nenhum dado disponível',
  showHeader = true,
  ...props 
}: DataTableProps) {
  const alignClass = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right',
  };

  if (loading) {
    return (
      <Card className={className} {...props}>
        {title && (
          <CardHeader>
            <CardTitle>{title}</CardTitle>
          </CardHeader>
        )}
        <CardContent>
          <div className="flex items-center justify-center p-8">
            <div className="text-muted-foreground">Carregando...</div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className} {...props}>
      {title && (
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent>
        {data.length === 0 ? (
          <EmptyState
            title={emptyMessage}
            variant="muted"
            size="sm"
          />
        ) : (
          <div className="overflow-x-auto -mx-4 sm:mx-0 px-4 sm:px-0">
            <table className={cn(tableVariants({ variant, size }), 'min-w-full')}>
              {showHeader && (
                <thead>
                  <tr className="border-b">
                    {columns.map((column) => (
                      <th
                        key={column.key}
                        className={cn(
                          'p-3 font-semibold',
                          alignClass[column.align || 'left'],
                          size === 'sm' && 'text-sm',
                          size === 'lg' && 'text-lg'
                        )}
                        style={column.width ? { width: column.width } : undefined}
                      >
                        {column.header}
                      </th>
                    ))}
                  </tr>
                </thead>
              )}
              <tbody>
                {data.map((row, rowIndex) => (
                  <tr
                    key={rowIndex}
                    className={cn(
                      'border-b transition-colors',
                      variant !== 'striped' && 'hover:bg-muted/50'
                    )}
                  >
                    {columns.map((column) => (
                      <td
                        key={column.key}
                        className={cn(
                          'p-3',
                          alignClass[column.align || 'left'],
                          size === 'sm' && 'text-sm',
                          size === 'lg' && 'text-lg'
                        )}
                      >
                        {column.render
                          ? column.render(row[column.key], row)
                          : String(row[column.key] || '-')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
