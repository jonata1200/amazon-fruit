// src/components/dashboards/kpi-card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { KPICard } from './kpi-card';
import { DollarSign, TrendingUp, Package } from 'lucide-react';

const meta: Meta<typeof KPICard> = {
  title: 'Dashboards/KPICard',
  component: KPICard,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    format: {
      control: 'select',
      options: ['currency', 'number', 'percentage'],
    },
    changeType: {
      control: 'select',
      options: ['increase', 'decrease', 'neutral'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof KPICard>;

export const Default: Story = {
  args: {
    title: 'Total Revenue',
    value: 12345,
    format: 'number',
  },
};

export const Currency: Story = {
  args: {
    title: 'Revenue',
    value: 123456.78,
    format: 'currency',
    icon: DollarSign,
  },
};

export const WithIncrease: Story = {
  args: {
    title: 'Sales Growth',
    value: 125000,
    change: 12.5,
    changeType: 'increase',
    format: 'currency',
    icon: TrendingUp,
  },
};

export const WithDecrease: Story = {
  args: {
    title: 'Expenses',
    value: 85000,
    change: 8.3,
    changeType: 'decrease',
    format: 'currency',
  },
};

export const Percentage: Story = {
  args: {
    title: 'Conversion Rate',
    value: 24.5,
    format: 'percentage',
  },
};

export const WithIcon: Story = {
  args: {
    title: 'Inventory',
    value: 5420,
    change: 5.2,
    changeType: 'increase',
    format: 'number',
    icon: Package,
  },
};

export const Neutral: Story = {
  args: {
    title: 'Static Metric',
    value: 100,
    change: 0,
    changeType: 'neutral',
    format: 'number',
  },
};
