// src/components/dashboards/kpi-card.tsx
'use client';

import { memo } from 'react';
import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { formatCurrency, formatNumber, formatPercentage } from '@/lib/utils';

interface KPICardProps {
  title: string;
  value: number;
  change?: number;
  changeType?: 'increase' | 'decrease' | 'neutral';
  format?: 'currency' | 'number' | 'percentage';
  icon?: LucideIcon;
  className?: string;
}

export const KPICard = memo(function KPICard({
  title,
  value,
  change,
  changeType = 'neutral',
  format = 'number',
  icon: Icon,
  className,
}: KPICardProps) {
  const formattedValue =
    format === 'currency'
      ? formatCurrency(value)
      : format === 'percentage'
        ? formatPercentage(value)
        : formatNumber(value);

  const TrendIcon =
    changeType === 'increase' ? TrendingUp : changeType === 'decrease' ? TrendingDown : Minus;

  const trendColor =
    changeType === 'increase'
      ? 'text-green-600'
      : changeType === 'decrease'
        ? 'text-red-600'
        : 'text-muted-foreground';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={className}
    >
      <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-2">
        <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 sm:h-5 sm:w-5 text-muted-foreground flex-shrink-0" />}
      </CardHeader>
      <CardContent className="pt-2">
        <div className="text-xl sm:text-2xl font-bold break-words">{formattedValue}</div>
        {change !== undefined && (
          <div className={cn('flex items-center text-xs mt-2', trendColor)}>
            <TrendIcon className="mr-1 h-3 w-3 sm:h-4 sm:w-4 flex-shrink-0" />
            <span className="truncate">{formatPercentage(Math.abs(change))} vs período anterior</span>
          </div>
        )}
      </CardContent>
    </Card>
    </motion.div>
  );
});
