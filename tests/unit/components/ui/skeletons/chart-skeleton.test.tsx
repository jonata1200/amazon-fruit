// tests/unit/components/ui/skeletons/chart-skeleton.test.tsx
import { render } from '@testing-library/react';
import { ChartSkeleton } from '@/components/ui/skeletons/chart-skeleton';

describe('ChartSkeleton', () => {
  it('renders chart skeleton', () => {
    const { container } = render(<ChartSkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders with title by default', () => {
    const { container } = render(<ChartSkeleton />);
    const skeleton = container.querySelector('.h-6.w-48');
    expect(skeleton).toBeInTheDocument();
  });

  it('does not render title when title is false', () => {
    const { container } = render(<ChartSkeleton title={false} />);
    const skeleton = container.querySelector('.h-6.w-48');
    expect(skeleton).not.toBeInTheDocument();
  });

  it('applies custom height', () => {
    const { container } = render(<ChartSkeleton height={400} />);
    const skeleton = container.querySelector('[style*="height: 400px"]');
    expect(skeleton).toBeInTheDocument();
  });

  it('uses default height when not provided', () => {
    const { container } = render(<ChartSkeleton />);
    const skeleton = container.querySelector('[style*="height: 300px"]');
    expect(skeleton).toBeInTheDocument();
  });
});
