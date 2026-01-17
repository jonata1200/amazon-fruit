// tests/unit/lib/hooks/useNotifications.test.ts
import { renderHook } from '@testing-library/react';
import { useNotifications } from '@/lib/hooks/useNotifications';
import { toast } from 'sonner';

// Mock do sonner
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    warning: jest.fn(),
    info: jest.fn(),
  },
}));

describe('useNotifications', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns notification functions', () => {
    const { result } = renderHook(() => useNotifications());

    expect(result.current.showSuccess).toBeDefined();
    expect(result.current.showError).toBeDefined();
    expect(result.current.showWarning).toBeDefined();
    expect(result.current.showInfo).toBeDefined();
  });

  it('calls toast.success when showSuccess is called', () => {
    const { result } = renderHook(() => useNotifications());

    result.current.showSuccess('Success message');

    expect(toast.success).toHaveBeenCalledWith('Success message');
    expect(toast.success).toHaveBeenCalledTimes(1);
  });

  it('calls toast.error when showError is called', () => {
    const { result } = renderHook(() => useNotifications());

    result.current.showError('Error message');

    expect(toast.error).toHaveBeenCalledWith('Error message');
    expect(toast.error).toHaveBeenCalledTimes(1);
  });

  it('calls toast.warning when showWarning is called', () => {
    const { result } = renderHook(() => useNotifications());

    result.current.showWarning('Warning message');

    expect(toast.warning).toHaveBeenCalledWith('Warning message');
    expect(toast.warning).toHaveBeenCalledTimes(1);
  });

  it('calls toast.info when showInfo is called', () => {
    const { result } = renderHook(() => useNotifications());

    result.current.showInfo('Info message');

    expect(toast.info).toHaveBeenCalledWith('Info message');
    expect(toast.info).toHaveBeenCalledTimes(1);
  });
});
