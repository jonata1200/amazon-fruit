// src/components/charts/pie-chart.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { PieChart } from './pie-chart';

const meta: Meta<typeof PieChart> = {
  title: 'Charts/PieChart',
  component: PieChart,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof PieChart>;

const sampleData = [
  { name: 'Desktop', value: 400 },
  { name: 'Mobile', value: 300 },
  { name: 'Tablet', value: 200 },
  { name: 'Other', value: 100 },
];

const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export const Default: Story = {
  args: {
    title: 'Device Distribution',
    data: sampleData,
    dataKey: 'value',
    nameKey: 'name',
    colors,
    height: 300,
  },
};

export const WithoutTitle: Story = {
  args: {
    data: sampleData,
    dataKey: 'value',
    nameKey: 'name',
    colors,
    height: 300,
  },
};

export const Small: Story = {
  args: {
    title: 'Small Pie Chart',
    data: sampleData.slice(0, 3),
    dataKey: 'value',
    nameKey: 'name',
    colors: colors.slice(0, 3),
    height: 250,
  },
};
