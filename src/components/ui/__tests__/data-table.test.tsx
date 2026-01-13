// src/components/ui/__tests__/data-table.test.tsx
import { render, screen } from '@testing-library/react';
import { DataTable } from '../data-table';

describe('DataTable', () => {
  const columns = [
    { key: 'name', header: 'Nome' },
    { key: 'age', header: 'Idade' },
  ];

  const data = [
    { name: 'João', age: 25 },
    { name: 'Maria', age: 30 },
  ];

  it('renders table with data', () => {
    render(<DataTable columns={columns} data={data} />);

    expect(screen.getByText('Nome')).toBeInTheDocument();
    expect(screen.getByText('Idade')).toBeInTheDocument();
    expect(screen.getByText('João')).toBeInTheDocument();
    expect(screen.getByText('Maria')).toBeInTheDocument();
    expect(screen.getByText('25')).toBeInTheDocument();
    expect(screen.getByText('30')).toBeInTheDocument();
  });

  it('renders title when provided', () => {
    render(<DataTable title="Usuários" columns={columns} data={data} />);

    expect(screen.getByText('Usuários')).toBeInTheDocument();
  });

  it('shows empty state when no data', () => {
    render(<DataTable columns={columns} data={[]} />);

    expect(screen.getByText('Nenhum dado disponível')).toBeInTheDocument();
  });

  it('uses custom render function', () => {
    const columnsWithRender = [
      {
        key: 'name',
        header: 'Nome',
        render: (value: unknown) => <strong>{String(value)}</strong>,
      },
    ];

    render(<DataTable columns={columnsWithRender} data={[{ name: 'João' }]} />);

    const strongElement = screen.getByText('João');
    expect(strongElement.tagName).toBe('STRONG');
  });
});
