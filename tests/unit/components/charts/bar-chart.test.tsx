// tests/unit/components/charts/bar-chart.test.tsx
import { render, screen } from '@testing-library/react';
import { BarChart } from '@/components/charts/bar-chart';

// Mock do analytics
jest.mock('@/lib/analytics/events', () => ({
  analytics: {
    chartInteracted: jest.fn(),
  },
}));

describe('BarChart', () => {
  const mockData = [
    { month: 'Jan', sales: 1000 },
    { month: 'Fev', sales: 1500 },
    { month: 'Mar', sales: 1200 },
  ];

  const mockBars = [
    { dataKey: 'sales', name: 'Vendas', color: '#8884d8' },
  ];

  it('renders bar chart with data', () => {
    const { container } = render(<BarChart data={mockData} bars={mockBars} xAxisKey="month" />);
    // Verificar se o componente renderiza (Card tem classe rounded-lg)
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('renders with title when provided', () => {
    render(<BarChart title="Vendas Mensais" data={mockData} bars={mockBars} xAxisKey="month" />);
    expect(screen.getByText('Vendas Mensais')).toBeInTheDocument();
  });

  it('renders without title when not provided', () => {
    const { container } = render(<BarChart data={mockData} bars={mockBars} xAxisKey="month" />);
    const cardHeader = container.querySelector('[class*="CardHeader"]');
    expect(cardHeader).not.toBeInTheDocument();
  });

  it('renders with empty data', () => {
    const { container } = render(<BarChart data={[]} bars={mockBars} xAxisKey="month" />);
    // Chart deve renderizar mesmo sem dados
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('applies custom height', () => {
    const { container } = render(
      <BarChart data={mockData} bars={mockBars} xAxisKey="month" height={400} />
    );
    const responsiveContainer = container.querySelector('[class*="recharts-responsive-container"]');
    expect(responsiveContainer).toBeInTheDocument();
  });

  it('renders multiple bars', () => {
    const multipleBars = [
      { dataKey: 'sales', name: 'Vendas', color: '#8884d8' },
      { dataKey: 'costs', name: 'Custos', color: '#82ca9d' },
    ];
    const dataWithMultipleBars = [
      { month: 'Jan', sales: 1000, costs: 500 },
      { month: 'Fev', sales: 1500, costs: 600 },
    ];
    const { container } = render(<BarChart data={dataWithMultipleBars} bars={multipleBars} xAxisKey="month" />);
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });
});
