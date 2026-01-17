// tests/unit/components/ui/tooltip.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Tooltip, HelpTooltip } from '@/components/ui/tooltip';

describe('Tooltip', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  it('renders children', () => {
    render(
      <Tooltip content="Tooltip content">
        <button>Hover me</button>
      </Tooltip>
    );
    expect(screen.getByText('Hover me')).toBeInTheDocument();
  });

  it('shows tooltip on hover after delay', async () => {
    const user = userEvent.setup({ delay: null });
    render(
      <Tooltip content="Tooltip content" delay={200}>
        <button>Hover me</button>
      </Tooltip>
    );

    const button = screen.getByText('Hover me');
    await user.hover(button);

    jest.advanceTimersByTime(200);

    await waitFor(() => {
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
      expect(screen.getByText('Tooltip content')).toBeInTheDocument();
    });
  });

  it('hides tooltip on mouse leave', async () => {
    const user = userEvent.setup({ delay: null });
    render(
      <Tooltip content="Tooltip content">
        <button>Hover me</button>
      </Tooltip>
    );

    const button = screen.getByText('Hover me');
    await user.hover(button);

    jest.advanceTimersByTime(200);

    await waitFor(() => {
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
    });

    await user.unhover(button);

    await waitFor(() => {
      expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
    });
  });

  it('applies side positioning classes', async () => {
    const user = userEvent.setup({ delay: null });
    const { rerender } = render(
      <Tooltip content="Content" side="top">
        <button>Button</button>
      </Tooltip>
    );

    await user.hover(screen.getByText('Button'));
    jest.advanceTimersByTime(200);

    await waitFor(() => {
      const tooltip = screen.getByRole('tooltip');
      expect(tooltip).toHaveClass('bottom-full');
    });

    rerender(
      <Tooltip content="Content" side="bottom">
        <button>Button</button>
      </Tooltip>
    );

    await user.hover(screen.getByText('Button'));
    jest.advanceTimersByTime(200);

    await waitFor(() => {
      const tooltip = screen.getByRole('tooltip');
      expect(tooltip).toHaveClass('top-full');
    });
  });

  it('applies custom className', async () => {
    const user = userEvent.setup({ delay: null });
    render(
      <Tooltip content="Content" className="custom-class">
        <button>Button</button>
      </Tooltip>
    );

    await user.hover(screen.getByText('Button'));
    jest.advanceTimersByTime(200);

    await waitFor(() => {
      const tooltip = screen.getByRole('tooltip');
      expect(tooltip).toHaveClass('custom-class');
    });
  });
});

describe('HelpTooltip', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  it('renders help icon', () => {
    render(<HelpTooltip content="Help text" />);
    expect(screen.getByText('?')).toBeInTheDocument();
  });

  it('shows tooltip content on hover', async () => {
    const user = userEvent.setup({ delay: null });
    render(<HelpTooltip content="Help text" />);

    const helpIcon = screen.getByText('?');
    await user.hover(helpIcon);

    jest.advanceTimersByTime(200);

    await waitFor(() => {
      expect(screen.getByText('Help text')).toBeInTheDocument();
    });
  });
});
