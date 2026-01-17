// tests/unit/components/ui/empty-state.test.tsx
import { render, screen } from '@testing-library/react';
import { EmptyState } from '@/components/ui/empty-state';
import { Search } from 'lucide-react';
import { Button } from '@/components/ui/button';

describe('EmptyState', () => {
  it('renders title', () => {
    render(<EmptyState title="No data found" />);
    expect(screen.getByText('No data found')).toBeInTheDocument();
  });

  it('renders description when provided', () => {
    render(<EmptyState title="Title" description="Description text" />);
    expect(screen.getByText('Description text')).toBeInTheDocument();
  });

  it('renders icon when provided', () => {
    render(<EmptyState title="Title" icon={Search} />);
    const icon = screen.getByRole('img', { hidden: true }) || document.querySelector('svg');
    expect(icon).toBeInTheDocument();
  });

  it('renders action button when provided', () => {
    render(
      <EmptyState
        title="Title"
        action={<Button>Action Button</Button>}
      />
    );
    expect(screen.getByText('Action Button')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(<EmptyState title="Title" className="custom-class" />);
    expect(container.firstChild).toHaveClass('custom-class');
  });

  it('renders all props together', () => {
    render(
      <EmptyState
        title="Complete Title"
        description="Complete description"
        icon={Search}
        action={<Button>Action</Button>}
      />
    );
    expect(screen.getByText('Complete Title')).toBeInTheDocument();
    expect(screen.getByText('Complete description')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
  });
});
