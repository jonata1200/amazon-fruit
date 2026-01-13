// src/components/charts/pie-chart.tsx
'use client';

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

export function PieChart({ title, data, dataKey, nameKey, colors, height = 300 }: PieChartProps) {
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
            >
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </RechartsPieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
