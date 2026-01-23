// src/components/dashboards/period-selector.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAppStore } from '@/store';
import { analytics } from '@/lib/analytics/events';
import { usePathname } from 'next/navigation';

export function PeriodSelector() {
  const dateRange = useAppStore((state) => state.dateRange);
  const setDateRange = useAppStore((state) => state.setDateRange);
  const pathname = usePathname();

  const [startDate, setStartDate] = useState(dateRange.start);
  const [endDate, setEndDate] = useState(dateRange.end);

  const handleApply = () => {
    setDateRange(startDate, endDate);
    
    // Rastrear mudança de período
    const dashboard = pathname?.split('/').filter(Boolean)[0] || 'unknown';
    analytics.dashboardPeriodChanged(dashboard, 'custom', startDate, endDate);
  };

  const handleReset = () => {
    // Reset para o ano atual
    const currentYear = new Date().getFullYear();
    const newStart = `${currentYear}-01-01`;
    const newEnd = `${currentYear}-12-31`;
    setStartDate(newStart);
    setEndDate(newEnd);
    setDateRange(newStart, newEnd);
  };

  return (
    <div className="flex flex-col sm:flex-row sm:flex-wrap items-stretch sm:items-end gap-3 sm:gap-4 rounded-lg border bg-card p-3 sm:p-4">
      <div className="flex-1 min-w-0 sm:min-w-[200px]">
        <Label htmlFor="start-date" className="text-sm">Data Inicial</Label>
        <Input
          id="start-date"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="w-full mt-1"
        />
      </div>

      <div className="flex-1 min-w-0 sm:min-w-[200px]">
        <Label htmlFor="end-date" className="text-sm">Data Final</Label>
        <Input
          id="end-date"
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="w-full mt-1"
        />
      </div>

      <div className="flex gap-2 sm:flex-shrink-0">
        <Button onClick={handleApply} className="flex-1 sm:flex-initial">
          Aplicar
        </Button>

        <Button variant="outline" onClick={handleReset} className="flex-1 sm:flex-initial">
          Resetar
        </Button>
      </div>
    </div>
  );
}
