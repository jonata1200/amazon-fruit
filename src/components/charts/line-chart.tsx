// src/components/charts/line-chart.tsx
'use client';

import { memo, useCallback } from 'react';
import { motion } from 'framer-motion';
import { analytics } from '@/lib/analytics/events';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface LineChartDataItem {
  [key: string]: string | number;
}

interface LineChartProps {
  title?: string;
  data: LineChartDataItem[];
  lines: {
    dataKey: string;
    name: string;
    color: string;
  }[];
  xAxisKey: string;
  height?: number;
}

export const LineChart = memo(function LineChart({ title, data, lines, xAxisKey, height = 300 }: LineChartProps) {
  const handleLegendClick = useCallback((e: any) => {
    analytics.chartInteracted('geral', 'line', 'legend_click');
  }, []);

  const handleDataPointClick = useCallback((data: any, index: number) => {
    analytics.chartInteracted('geral', 'line', 'data_point_click');
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
    >
      <Card>
      {title && (
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent className="p-3 sm:p-6">
        <ResponsiveContainer width="100%" height={height}>
          <RechartsLineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey={xAxisKey} 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fontSize: 12 }} />
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
            {lines.map((line) => (
              <Line
                key={line.dataKey}
                type="monotone"
                dataKey={line.dataKey}
                name={line.name}
                stroke={line.color}
                strokeWidth={2}
                onClick={handleDataPointClick}
                style={{ cursor: 'pointer' }}
              />
            ))}
          </RechartsLineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
    </motion.div>
  );
});
