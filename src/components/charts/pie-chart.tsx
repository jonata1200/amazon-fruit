// src/components/charts/pie-chart.tsx
'use client';

import { memo, useCallback } from 'react';
import { analytics } from '@/lib/analytics/events';
import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface PieChartDataItem {
  [key: string]: string | number;
}

interface PieChartProps {
  title?: string;
  data: PieChartDataItem[];
  dataKey: string;
  nameKey: string;
  colors: string[];
  height?: number;
}

export const PieChart = memo(function PieChart({ title, data, dataKey, nameKey, colors, height = 300 }: PieChartProps) {
  const handleLegendClick = useCallback(() => {
    analytics.chartInteracted('geral', 'pie', 'legend_click');
  }, []);

  const handleCellClick = useCallback(() => {
    analytics.chartInteracted('geral', 'pie', 'data_point_click');
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
          <RechartsPieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(props) => String((props as unknown as PieChartDataItem)[nameKey])}
              outerRadius={80}
              fill="#8884d8"
              dataKey={dataKey}
              onClick={handleCellClick}
            >
              {data.map((_, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={colors[index % colors.length]}
                  style={{ cursor: 'pointer' }}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend onClick={handleLegendClick} />
          </RechartsPieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
});
