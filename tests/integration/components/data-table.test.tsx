// tests/integration/components/data-table.test.tsx
import { renderWithProviders, screen } from '../helpers/render-with-providers';
import { DataTable } from '@/components/ui/data-table';

const mockColumns = [
  { key: 'name', header: 'Nome' },
  { key: 'value', header: 'Valor' },
  { key: 'status', header: 'Status' },
];

const mockData = [
  { name: 'Item 1', value: 100, status: 'Ativo' },
  { name: 'Item 2', value: 200, status: 'Inativo' },
  { name: 'Item 3', value: 300, status: 'Ativo' },
];

describe('DataTable - Integração', () => {
  it('renderiza tabela com dados', () => {
    renderWithProviders(<DataTable columns={mockColumns} data={mockData} />);

    expect(screen.getByText('Nome')).toBeInTheDocument();
    expect(screen.getByText('Valor')).toBeInTheDocument();
    expect(screen.getByText('Status')).toBeInTheDocument();
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
    expect(screen.getByText('Item 3')).toBeInTheDocument();
  });

  it('renderiza título quando fornecido', () => {
    renderWithProviders(<DataTable title="Tabela de Teste" columns={mockColumns} data={mockData} />);

    expect(screen.getByText('Tabela de Teste')).toBeInTheDocument();
  });

  it('exibe mensagem quando não há dados', () => {
    renderWithProviders(<DataTable columns={mockColumns} data={[]} />);

    expect(screen.getByText('Nenhum dado disponível')).toBeInTheDocument();
  });

  it('renderiza células customizadas com render function', () => {
    const columnsWithRender = [
      { key: 'name', header: 'Nome' },
      {
        key: 'value',
        header: 'Valor',
        render: (value: unknown) => `R$ ${value}`,
      },
    ];

    renderWithProviders(<DataTable columns={columnsWithRender} data={mockData} />);

    expect(screen.getByText('R$ 100')).toBeInTheDocument();
    expect(screen.getByText('R$ 200')).toBeInTheDocument();
  });

  it('renderiza todas as linhas de dados', () => {
    renderWithProviders(<DataTable columns={mockColumns} data={mockData} />);

    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
    expect(screen.getByText('Item 3')).toBeInTheDocument();
  });
});
