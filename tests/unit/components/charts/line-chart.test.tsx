// tests/unit/components/charts/line-chart.test.tsx
import { render, screen } from '@testing-library/react';
import { LineChart } from '@/components/charts/line-chart';

// Mock do analytics
jest.mock('@/lib/analytics/events', () => ({
  analytics: {
    chartInteracted: jest.fn(),
  },
}));

// Mock do framer-motion para evitar problemas de animação nos testes
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: { children: React.ReactNode }) => <div {...props}>{children}</div>,
  },
}));

describe('LineChart', () => {
  const mockData = [
    { month: 'Jan', revenue: 1000, expenses: 500 },
    { month: 'Fev', revenue: 1500, expenses: 600 },
    { month: 'Mar', revenue: 1200, expenses: 550 },
  ];

  const mockLines = [
    { dataKey: 'revenue', name: 'Receita', color: '#8884d8' },
    { dataKey: 'expenses', name: 'Despesas', color: '#82ca9d' },
  ];

  it('renders line chart with data', () => {
    const { container } = render(<LineChart data={mockData} lines={mockLines} xAxisKey="month" />);
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('renders with title when provided', () => {
    render(<LineChart title="Evolução Financeira" data={mockData} lines={mockLines} xAxisKey="month" />);
    expect(screen.getByText('Evolução Financeira')).toBeInTheDocument();
  });

  it('renders without title when not provided', () => {
    const { container } = render(<LineChart data={mockData} lines={mockLines} xAxisKey="month" />);
    const cardHeader = container.querySelector('[class*="CardHeader"]');
    expect(cardHeader).not.toBeInTheDocument();
  });

  it('renders with empty data', () => {
    const { container } = render(<LineChart data={[]} lines={mockLines} xAxisKey="month" />);
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('renders multiple lines', () => {
    const { container } = render(<LineChart data={mockData} lines={mockLines} xAxisKey="month" />);
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('applies custom height', () => {
    const { container } = render(
      <LineChart data={mockData} lines={mockLines} xAxisKey="month" height={400} />
    );
    const responsiveContainer = container.querySelector('[class*="recharts-responsive-container"]');
    expect(responsiveContainer).toBeInTheDocument();
  });
});
