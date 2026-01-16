// src/components/features/export/export-button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ExportButton } from './export-button';

const meta: Meta<typeof ExportButton> = {
  title: 'Features/ExportButton',
  component: ExportButton,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ExportButton>;

export const Default: Story = {
  args: {
    dashboard: 'geral',
  },
};

export const FinanceDashboard: Story = {
  args: {
    dashboard: 'financas',
  },
};

export const EstoqueDashboard: Story = {
  args: {
    dashboard: 'estoque',
  },
};
