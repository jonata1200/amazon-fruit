// tests/unit/components/ui/skeleton.test.tsx
import { render } from '@testing-library/react';
import { Skeleton } from '@/components/ui/skeleton';

describe('Skeleton', () => {
  it('renders skeleton element', () => {
    const { container } = render(<Skeleton />);
    const skeleton = container.firstChild;
    expect(skeleton).toBeInTheDocument();
    expect(skeleton).toHaveClass('animate-pulse', 'rounded-md', 'bg-muted');
  });

  it('applies custom className', () => {
    const { container } = render(<Skeleton className="custom-class" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('custom-class');
  });

  it('renders with text variant style', () => {
    const { container } = render(<Skeleton className="h-4 w-32" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('h-4', 'w-32');
  });

  it('renders with circle variant style', () => {
    const { container } = render(<Skeleton className="h-12 w-12 rounded-full" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('rounded-full', 'h-12', 'w-12');
  });

  it('renders with rectangular variant style', () => {
    const { container } = render(<Skeleton className="h-20 w-full" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('h-20', 'w-full');
  });

  it('forwards other props', () => {
    const { container } = render(<Skeleton data-testid="skeleton" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveAttribute('data-testid', 'skeleton');
  });
});
