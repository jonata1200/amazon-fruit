// tests/unit/components/dashboards/dashboard-skeleton.test.tsx
import { render } from '@testing-library/react';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';

describe('DashboardSkeleton', () => {
  it('renders dashboard skeleton', () => {
    const { container } = render(<DashboardSkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders header skeleton', () => {
    const { container } = render(<DashboardSkeleton />);
    const headerSkeletons = container.querySelectorAll('.h-10');
    expect(headerSkeletons.length).toBeGreaterThan(0);
  });

  it('renders KPI cards skeleton', () => {
    const { container } = render(<DashboardSkeleton />);
    const kpiCards = container.querySelectorAll('.grid.gap-4')[0];
    expect(kpiCards).toBeInTheDocument();
  });

  it('renders charts skeleton', () => {
    const { container } = render(<DashboardSkeleton />);
    const chartsGrid = container.querySelectorAll('.grid.gap-4')[1];
    expect(chartsGrid).toBeInTheDocument();
  });

  it('renders table skeleton', () => {
    const { container } = render(<DashboardSkeleton />);
    const tableSkeleton = container.querySelector('.space-y-3');
    expect(tableSkeleton).toBeInTheDocument();
  });
});
