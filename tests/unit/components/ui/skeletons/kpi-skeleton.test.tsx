// tests/unit/components/ui/skeletons/kpi-skeleton.test.tsx
import { render } from '@testing-library/react';
import { KPISkeleton } from '@/components/ui/skeletons/kpi-skeleton';

describe('KPISkeleton', () => {
  it('renders KPI skeleton', () => {
    const { container } = render(<KPISkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders title skeleton', () => {
    const { container } = render(<KPISkeleton />);
    const titleSkeleton = container.querySelector('.h-4.w-24');
    expect(titleSkeleton).toBeInTheDocument();
  });

  it('renders icon skeleton', () => {
    const { container } = render(<KPISkeleton />);
    const iconSkeleton = container.querySelector('.h-4.w-4.rounded');
    expect(iconSkeleton).toBeInTheDocument();
  });

  it('renders value skeleton', () => {
    const { container } = render(<KPISkeleton />);
    const valueSkeleton = container.querySelector('.h-8.w-32');
    expect(valueSkeleton).toBeInTheDocument();
  });

  it('renders change skeleton', () => {
    const { container } = render(<KPISkeleton />);
    const changeSkeleton = container.querySelector('.h-3.w-20');
    expect(changeSkeleton).toBeInTheDocument();
  });
});
