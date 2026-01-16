// src/components/charts/bar-chart.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { BarChart } from './bar-chart';

const meta: Meta<typeof BarChart> = {
  title: 'Charts/BarChart',
  component: BarChart,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof BarChart>;

const sampleData = [
  { category: 'Q1', value: 4000, target: 3500 },
  { category: 'Q2', value: 3000, target: 4000 },
  { category: 'Q3', value: 5000, target: 4500 },
  { category: 'Q4', value: 4500, target: 5000 },
];

export const Default: Story = {
  args: {
    title: 'Quarterly Performance',
    data: sampleData,
    xAxisKey: 'category',
    bars: [
      { dataKey: 'value', name: 'Actual', color: '#3b82f6' },
      { dataKey: 'target', name: 'Target', color: '#10b981' },
    ],
    height: 300,
  },
};

export const SingleBar: Story = {
  args: {
    title: 'Sales by Quarter',
    data: sampleData,
    xAxisKey: 'category',
    bars: [{ dataKey: 'value', name: 'Sales', color: '#8b5cf6' }],
    height: 300,
  },
};

export const Vertical: Story = {
  args: {
    title: 'Vertical Bar Chart',
    data: sampleData,
    xAxisKey: 'category',
    bars: [
      { dataKey: 'value', name: 'Value', color: '#ef4444' },
      { dataKey: 'target', name: 'Target', color: '#f59e0b' },
    ],
    layout: 'vertical',
    height: 400,
  },
};
