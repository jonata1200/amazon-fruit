// src/components/ui/__tests__/dropdown-menu.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '../dropdown-menu';
import { Button } from '../button';

describe('DropdownMenu', () => {
  it('opens when trigger is clicked', () => {
    render(
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button>Open Menu</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Item 1</DropdownMenuItem>
          <DropdownMenuItem>Item 2</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );

    expect(screen.queryByText('Item 1')).not.toBeInTheDocument();

    fireEvent.click(screen.getByText('Open Menu'));

    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
  });

  it('calls onClick when menu item is clicked', () => {
    const handleClick = jest.fn();

    render(
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button>Open Menu</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={handleClick}>Item 1</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );

    fireEvent.click(screen.getByText('Open Menu'));
    fireEvent.click(screen.getByText('Item 1'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when item is disabled', () => {
    const handleClick = jest.fn();

    render(
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button>Open Menu</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={handleClick} disabled>
            Item 1
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );

    fireEvent.click(screen.getByText('Open Menu'));
    fireEvent.click(screen.getByText('Item 1'));

    expect(handleClick).not.toHaveBeenCalled();
  });
});
