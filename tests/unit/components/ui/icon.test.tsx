// tests/unit/components/ui/icon.test.tsx
import { render } from '@testing-library/react';
import { Icon } from '@/components/ui/icon';
import { Search, Home, User } from 'lucide-react';

describe('Icon', () => {
  it('renders icon with default size', () => {
    const { container } = render(<Icon icon={Search} />);
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
    // Verifica se tem as classes de tamanho md (h-5 w-5)
    const classes = svg?.className || '';
    expect(classes).toContain('h-5');
    expect(classes).toContain('w-5');
  });

  it('renders icon with xs size', () => {
    const { container } = render(<Icon icon={Search} size="xs" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('h-3', 'w-3');
  });

  it('renders icon with sm size', () => {
    const { container } = render(<Icon icon={Search} size="sm" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('h-4', 'w-4');
  });

  it('renders icon with lg size', () => {
    const { container } = render(<Icon icon={Search} size="lg" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('h-6', 'w-6');
  });

  it('renders icon with xl size', () => {
    const { container } = render(<Icon icon={Search} size="xl" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('h-8', 'w-8');
  });

  it('applies custom className', () => {
    const { container } = render(<Icon icon={Search} className="custom-class" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('custom-class');
  });

  it('renders different icons', () => {
    const { container: container1 } = render(<Icon icon={Search} />);
    const { container: container2 } = render(<Icon icon={Home} />);
    const { container: container3 } = render(<Icon icon={User} />);

    expect(container1.querySelector('svg')).toBeInTheDocument();
    expect(container2.querySelector('svg')).toBeInTheDocument();
    expect(container3.querySelector('svg')).toBeInTheDocument();
  });

  it('passes through other props', () => {
    const { container } = render(<Icon icon={Search} data-testid="icon" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('data-testid', 'icon');
  });
});
