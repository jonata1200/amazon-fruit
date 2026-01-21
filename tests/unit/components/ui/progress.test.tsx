// tests/unit/components/ui/progress.test.tsx
import { render, screen } from '@testing-library/react';
import { Progress } from '@/components/ui/progress';

describe('Progress', () => {
  it('renders progress bar', () => {
    render(<Progress value={50} />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toBeInTheDocument();
  });

  it('displays correct value at 0%', () => {
    const { container } = render(<Progress value={0} />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuenow', '0');
    const progressBar = container.querySelector('[style*="width"]');
    expect(progressBar).toHaveStyle({ width: '0%' });
  });

  it('displays correct value at 50%', () => {
    const { container } = render(<Progress value={50} />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuenow', '50');
    const progressBar = container.querySelector('[style*="width"]');
    expect(progressBar).toHaveStyle({ width: '50%' });
  });

  it('displays correct value at 100%', () => {
    const { container } = render(<Progress value={100} />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuenow', '100');
    const progressBar = container.querySelector('[style*="width"]');
    expect(progressBar).toHaveStyle({ width: '100%' });
  });

  it('clamps value above 100%', () => {
    const { container } = render(<Progress value={150} />);
    const progressbar = screen.getByRole('progressbar');
    const progressBar = container.querySelector('[style*="width"]');
    expect(progressBar).toHaveStyle({ width: '100%' });
  });

  it('clamps value below 0%', () => {
    const { container } = render(<Progress value={-10} />);
    const progressbar = screen.getByRole('progressbar');
    const progressBar = container.querySelector('[style*="width"]');
    expect(progressBar).toHaveStyle({ width: '0%' });
  });

  it('shows label when showLabel is true', () => {
    render(<Progress value={75} showLabel />);
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('does not show label by default', () => {
    render(<Progress value={50} />);
    expect(screen.queryByText('50%')).not.toBeInTheDocument();
  });

  it('uses custom max value', () => {
    render(<Progress value={50} max={200} />);
    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuemax', '200');
    expect(progressbar).toHaveAttribute('aria-valuenow', '50');
  });

  it('applies size classes', () => {
    const { rerender } = render(<Progress value={50} size="sm" />);
    let progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveClass('h-1');

    rerender(<Progress value={50} size="md" />);
    progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveClass('h-2');

    rerender(<Progress value={50} size="lg" />);
    progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveClass('h-3');
  });

  it('applies custom className', () => {
    const { container } = render(<Progress value={50} className="custom-class" />);
    expect(container.firstChild).toHaveClass('custom-class');
  });
});
