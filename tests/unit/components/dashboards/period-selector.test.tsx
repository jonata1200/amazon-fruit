// tests/unit/components/dashboards/period-selector.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { useAppStore } from '@/store';

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

// Mock do next/navigation
jest.mock('next/navigation', () => ({
  usePathname: () => '/geral',
}));

// Mock do analytics
jest.mock('@/lib/analytics/events', () => ({
  analytics: {
    dashboardPeriodChanged: jest.fn(),
  },
}));

describe('PeriodSelector', () => {
  const mockSetDateRange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          dateRange: {
            start: '2024-01-01',
            end: '2024-12-31',
          },
          setDateRange: mockSetDateRange,
        });
      }
    });
  });

  it('renders period selector', () => {
    render(<PeriodSelector />);
    expect(screen.getByText('Data Inicial')).toBeInTheDocument();
    expect(screen.getByText('Data Final')).toBeInTheDocument();
  });

  it('displays current date range', () => {
    render(<PeriodSelector />);
    const startInput = screen.getByLabelText('Data Inicial') as HTMLInputElement;
    const endInput = screen.getByLabelText('Data Final') as HTMLInputElement;
    expect(startInput.value).toBe('2024-01-01');
    expect(endInput.value).toBe('2024-12-31');
  });

  it('updates start date on input change', () => {
    render(<PeriodSelector />);
    const startInput = screen.getByLabelText('Data Inicial') as HTMLInputElement;
    fireEvent.change(startInput, { target: { value: '2024-06-01' } });
    expect(startInput.value).toBe('2024-06-01');
  });

  it('calls setDateRange when apply button is clicked', () => {
    render(<PeriodSelector />);
    const applyButton = screen.getByText('Aplicar Período');
    fireEvent.click(applyButton);
    expect(mockSetDateRange).toHaveBeenCalled();
  });

  it('resets to current year when reset button is clicked', () => {
    render(<PeriodSelector />);
    const resetButton = screen.getByText('Resetar');
    fireEvent.click(resetButton);
    expect(mockSetDateRange).toHaveBeenCalled();
  });
});
