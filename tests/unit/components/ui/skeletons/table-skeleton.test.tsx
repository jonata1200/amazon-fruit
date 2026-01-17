// tests/unit/components/ui/skeletons/table-skeleton.test.tsx
import { render } from '@testing-library/react';
import { TableSkeleton } from '@/components/ui/skeletons/table-skeleton';

describe('TableSkeleton', () => {
  it('renders table skeleton', () => {
    const { container } = render(<TableSkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders with title by default', () => {
    const { container } = render(<TableSkeleton />);
    const titleSkeleton = container.querySelector('.h-6.w-48');
    expect(titleSkeleton).toBeInTheDocument();
  });

  it('does not render title when title is false', () => {
    const { container } = render(<TableSkeleton title={false} />);
    const titleSkeleton = container.querySelector('.h-6.w-48');
    expect(titleSkeleton).not.toBeInTheDocument();
  });

  it('renders default number of rows (5)', () => {
    const { container } = render(<TableSkeleton />);
    const rows = container.querySelectorAll('.space-y-3 > div');
    // 1 header + 5 rows = 6 divs
    expect(rows.length).toBe(6);
  });

  it('renders custom number of rows', () => {
    const { container } = render(<TableSkeleton rows={10} />);
    const rows = container.querySelectorAll('.space-y-3 > div');
    // 1 header + 10 rows = 11 divs
    expect(rows.length).toBe(11);
  });

  it('renders default number of columns (4)', () => {
    const { container } = render(<TableSkeleton />);
    const firstRow = container.querySelector('.space-y-3 > div');
    const columns = firstRow?.querySelectorAll('.h-4.flex-1');
    expect(columns?.length).toBe(4);
  });

  it('renders custom number of columns', () => {
    const { container } = render(<TableSkeleton columns={6} />);
    const firstRow = container.querySelector('.space-y-3 > div');
    const columns = firstRow?.querySelectorAll('.h-4.flex-1');
    expect(columns?.length).toBe(6);
  });
});
