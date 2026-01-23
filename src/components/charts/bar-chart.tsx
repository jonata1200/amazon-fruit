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
      <CardContent className="p-3 sm:p-6">
        <ResponsiveContainer width="100%" height={height}>
          <RechartsBarChart data={data} layout={layout} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            {layout === 'horizontal' ? (
              <>
                <XAxis 
                  dataKey={xAxisKey} 
                  tick={{ fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis tick={{ fontSize: 12 }} />
              </>
            ) : (
              <>
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis 
                  dataKey={xAxisKey} 
                  type="category" 
                  tick={{ fontSize: 12 }}
                  width={80}
                />
              </>
            )}
            <Tooltip 
              contentStyle={{ 
                fontSize: '12px',
                padding: '8px',
                borderRadius: '6px'
              }}
            />
            <Legend 
              onClick={handleLegendClick}
              wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
            />
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
