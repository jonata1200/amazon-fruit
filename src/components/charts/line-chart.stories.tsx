// src/components/charts/line-chart.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { LineChart } from './line-chart';

const meta: Meta<typeof LineChart> = {
  title: 'Charts/LineChart',
  component: LineChart,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof LineChart>;

const sampleData = [
  { mes: 'Jan', receita: 4000, despesa: 2400, lucro: 1600 },
  { mes: 'Fev', receita: 3000, despesa: 1398, lucro: 1602 },
  { mes: 'Mar', receita: 2000, despesa: 9800, lucro: 1200 },
  { mes: 'Abr', receita: 2780, despesa: 3908, lucro: 1872 },
  { mes: 'Mai', receita: 1890, despesa: 4800, lucro: 1090 },
  { mes: 'Jun', receita: 2390, despesa: 3800, lucro: 1590 },
];

export const Default: Story = {
  args: {
    title: 'Sales Trend',
    data: sampleData,
    xAxisKey: 'mes',
    lines: [
      { dataKey: 'receita', name: 'Revenue', color: '#10b981' },
      { dataKey: 'despesa', name: 'Expenses', color: '#ef4444' },
    ],
    height: 300,
  },
};

export const WithProfit: Story = {
  args: {
    title: 'Financial Evolution',
    data: sampleData,
    xAxisKey: 'mes',
    lines: [
      { dataKey: 'receita', name: 'Revenue', color: '#10b981' },
      { dataKey: 'despesa', name: 'Expenses', color: '#ef4444' },
      { dataKey: 'lucro', name: 'Profit', color: '#3b82f6' },
    ],
    height: 400,
  },
};

export const SingleLine: Story = {
  args: {
    title: 'Monthly Revenue',
    data: sampleData,
    xAxisKey: 'mes',
    lines: [{ dataKey: 'receita', name: 'Revenue', color: '#8b5cf6' }],
    height: 300,
  },
};

export const WithoutTitle: Story = {
  args: {
    data: sampleData,
    xAxisKey: 'mes',
    lines: [
      { dataKey: 'receita', name: 'Revenue', color: '#10b981' },
      { dataKey: 'despesa', name: 'Expenses', color: '#ef4444' },
    ],
    height: 300,
  },
};
