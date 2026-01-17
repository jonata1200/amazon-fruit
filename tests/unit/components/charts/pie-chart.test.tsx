// tests/unit/components/charts/pie-chart.test.tsx
import { render, screen } from '@testing-library/react';
import { PieChart } from '@/components/charts/pie-chart';

// Mock do analytics
jest.mock('@/lib/analytics/events', () => ({
  analytics: {
    chartInteracted: jest.fn(),
  },
}));

describe('PieChart', () => {
  const mockData = [
    { name: 'Categoria A', value: 400 },
    { name: 'Categoria B', value: 300 },
    { name: 'Categoria C', value: 200 },
  ];

  const mockColors = ['#8884d8', '#82ca9d', '#ffc658'];

  it('renders pie chart with data', () => {
    const { container } = render(
      <PieChart
        data={mockData}
        dataKey="value"
        nameKey="name"
        colors={mockColors}
      />
    );
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('renders with title when provided', () => {
    render(
      <PieChart
        title="Distribuição por Categoria"
        data={mockData}
        dataKey="value"
        nameKey="name"
        colors={mockColors}
      />
    );
    expect(screen.getByText('Distribuição por Categoria')).toBeInTheDocument();
  });

  it('renders without title when not provided', () => {
    const { container } = render(
      <PieChart data={mockData} dataKey="value" nameKey="name" colors={mockColors} />
    );
    const cardHeader = container.querySelector('[class*="CardHeader"]');
    expect(cardHeader).not.toBeInTheDocument();
  });

  it('renders with empty data', () => {
    const { container } = render(<PieChart data={[]} dataKey="value" nameKey="name" colors={mockColors} />);
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });

  it('applies custom height', () => {
    const { container } = render(
      <PieChart
        data={mockData}
        dataKey="value"
        nameKey="name"
        colors={mockColors}
        height={400}
      />
    );
    const responsiveContainer = container.querySelector('[class*="recharts-responsive-container"]');
    expect(responsiveContainer).toBeInTheDocument();
  });

  it('renders with multiple data points', () => {
    const largeData = Array.from({ length: 10 }, (_, i) => ({
      name: `Categoria ${i + 1}`,
      value: (i + 1) * 100,
    }));
    const { container } = render(
      <PieChart
        data={largeData}
        dataKey="value"
        nameKey="name"
        colors={mockColors}
      />
    );
    const card = container.querySelector('.rounded-lg');
    expect(card).toBeTruthy();
  });
});
