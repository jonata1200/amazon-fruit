// tests/unit/components/layouts/footer.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { Footer } from '@/components/layouts/footer';

describe('Footer', () => {
  it('renders footer', () => {
    render(<Footer />);
    expect(screen.getByText(/Amazon Fruit/)).toBeInTheDocument();
  });

  it('displays current year', async () => {
    render(<Footer />);
    const currentYear = new Date().getFullYear();
    await waitFor(() => {
      expect(screen.getByText(new RegExp(currentYear.toString()))).toBeInTheDocument();
    });
  });

  it('displays copyright text', () => {
    render(<Footer />);
    expect(screen.getByText(/Sistema de Análise de Dados/)).toBeInTheDocument();
  });

  it('has correct structure', () => {
    const { container } = render(<Footer />);
    const footer = container.querySelector('footer');
    expect(footer).toBeInTheDocument();
    expect(footer).toHaveClass('border-t', 'py-4', 'px-6');
  });
});
