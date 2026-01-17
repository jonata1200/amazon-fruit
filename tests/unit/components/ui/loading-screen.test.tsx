// tests/unit/components/ui/loading-screen.test.tsx
import { render, screen } from '@testing-library/react';
import { LoadingScreen } from '@/components/ui/loading-screen';

describe('LoadingScreen', () => {
  it('renders with default message', () => {
    render(<LoadingScreen />);
    const message = screen.getByText('Carregando...', { exact: false });
    expect(message).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument(); // Spinner
  });

  it('renders with custom message', () => {
    render(<LoadingScreen message="Loading data..." />);
    expect(screen.getByText('Loading data...')).toBeInTheDocument();
  });

  it('renders spinner', () => {
    render(<LoadingScreen />);
    const spinner = screen.getByRole('status');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass('h-12'); // lg size
  });

  it('has correct layout structure', () => {
    const { container } = render(<LoadingScreen />);
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('flex', 'flex-col', 'items-center', 'justify-center', 'h-screen');
  });
});
