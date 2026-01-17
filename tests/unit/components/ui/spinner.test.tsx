// tests/unit/components/ui/spinner.test.tsx
import { render, screen } from '@testing-library/react';
import { Spinner } from '@/components/ui/spinner';

describe('Spinner', () => {
  it('renders spinner with default size', () => {
    render(<Spinner />);
    const spinner = screen.getByRole('status');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass('h-8');
  });

  it('renders spinner with small size', () => {
    render(<Spinner size="sm" />);
    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('h-4');
  });

  it('renders spinner with large size', () => {
    render(<Spinner size="lg" />);
    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('h-12');
  });

  it('has accessible label', () => {
    render(<Spinner />);
    expect(screen.getByLabelText('Carregando')).toBeInTheDocument();
  });
});
