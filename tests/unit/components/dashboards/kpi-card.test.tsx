// tests/unit/components/dashboards/kpi-card.test.tsx
import { render, screen } from '@testing-library/react';
import { KPICard } from '@/components/dashboards/kpi-card';
import { DollarSign } from 'lucide-react';

describe('KPICard', () => {
  it('renders title and value', () => {
    render(<KPICard title="Receita" value={100000} format="currency" />);

    expect(screen.getByText('Receita')).toBeInTheDocument();
    expect(screen.getByText(/100\.000,00/)).toBeInTheDocument();
  });

  it('formats number correctly', () => {
    render(<KPICard title="Total" value={5000} format="number" />);

    expect(screen.getByText('5.000')).toBeInTheDocument();
  });

  it('formats percentage correctly', () => {
    render(<KPICard title="Taxa" value={15.5} format="percentage" />);

    expect(screen.getByText('15,5%')).toBeInTheDocument();
  });

  it('displays change with increase indicator', () => {
    render(
      <KPICard title="Vendas" value={10000} format="currency" change={15} changeType="increase" />
    );

    expect(screen.getByText(/15,0%/)).toBeInTheDocument();
  });

  it('displays change with decrease indicator', () => {
    render(
      <KPICard title="Despesas" value={5000} format="currency" change={-10} changeType="decrease" />
    );

    expect(screen.getByText(/10,0%/)).toBeInTheDocument();
  });

  it('renders icon when provided', () => {
    const { container } = render(
      <KPICard title="Receita" value={100000} format="currency" icon={DollarSign} />
    );

    expect(container.querySelector('svg')).toBeInTheDocument();
  });

  it('does not show change when not provided', () => {
    render(<KPICard title="Total" value={1000} format="number" />);

    expect(screen.queryByText(/%/)).not.toBeInTheDocument();
  });
});
