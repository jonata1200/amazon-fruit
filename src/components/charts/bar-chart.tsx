// src/components/charts/bar-chart.tsx
'use client';

import { memo, useCallback } from 'react';
import { analytics } from '@/lib/analytics/events';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface BarChartDataItem {
  [key: string]: string | number;
}

interface BarChartProps {
  title?: string;
  data: BarChartDataItem[];
  bars: {
    dataKey: string;
    name: string;
    color: string;
  }[];
  xAxisKey: string;
  height?: number;
  layout?: 'horizontal' | 'vertical';
}

export const BarChart = memo(function BarChart({
  title,
  data,
  bars,
  xAxisKey,
  height = 300,
  layout = 'horizontal',
}: BarChartProps) {
  const handleLegendClick = useCallback(() => {
    analytics.chartInteracted('geral', 'bar', 'legend_click');
  }, []);

  const handleBarClick = useCallback(() => {
    analytics.chartInteracted('geral', 'bar', 'data_point_click');
  }, []);

  return (
    <Card>
      {title && (
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <RechartsBarChart data={data} layout={layout}>
            <CartesianGrid strokeDasharray="3 3" />
            {layout === 'horizontal' ? (
              <>
                <XAxis dataKey={xAxisKey} />
                <YAxis />
              </>
            ) : (
              <>
                <XAxis type="number" />
                <YAxis dataKey={xAxisKey} type="category" />
              </>
            )}
            <Tooltip />
            <Legend onClick={handleLegendClick} />
            {bars.map((bar) => (
              <Bar 
                key={bar.dataKey} 
                dataKey={bar.dataKey} 
                name={bar.name} 
                fill={bar.color}
                onClick={handleBarClick}
                style={{ cursor: 'pointer' }}
              />
            ))}
          </RechartsBarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
});
