// tests/unit/lib/hooks/useKeyboardShortcuts.test.ts
import { renderHook } from '@testing-library/react';
import { useKeyboardShortcuts } from '@/lib/hooks/useKeyboardShortcuts';
import { useAppStore } from '@/store';

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

describe('useKeyboardShortcuts', () => {
  const mockToggleTheme = jest.fn();
  const mockToggleSearch = jest.fn();
  const mockSetSearchOpen = jest.fn();
  const mockSetAlertsOpen = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          toggleTheme: mockToggleTheme,
          toggleSearch: mockToggleSearch,
          searchOpen: false,
          alertsOpen: false,
          setSearchOpen: mockSetSearchOpen,
          setAlertsOpen: mockSetAlertsOpen,
        });
      }
      return {
        getState: () => ({
          searchOpen: false,
          alertsOpen: false,
          setSearchOpen: mockSetSearchOpen,
          setAlertsOpen: mockSetAlertsOpen,
        }),
      };
    });
  });

  it('registers keyboard event listener', () => {
    const addEventListenerSpy = jest.spyOn(window, 'addEventListener');
    renderHook(() => useKeyboardShortcuts());

    expect(addEventListenerSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
    addEventListenerSpy.mockRestore();
  });

  it('calls toggleSearch on Ctrl+K', () => {
    renderHook(() => useKeyboardShortcuts());

    const event = new KeyboardEvent('keydown', {
      key: 'k',
      ctrlKey: true,
    });
    window.dispatchEvent(event);

    expect(mockToggleSearch).toHaveBeenCalledTimes(1);
  });

  it('calls toggleSearch on Cmd+K (Mac)', () => {
    renderHook(() => useKeyboardShortcuts());

    const event = new KeyboardEvent('keydown', {
      key: 'k',
      metaKey: true,
    });
    window.dispatchEvent(event);

    expect(mockToggleSearch).toHaveBeenCalledTimes(1);
  });

  it('calls toggleTheme on Ctrl+T', () => {
    renderHook(() => useKeyboardShortcuts());

    const event = new KeyboardEvent('keydown', {
      key: 't',
      ctrlKey: true,
    });
    window.dispatchEvent(event);

    expect(mockToggleTheme).toHaveBeenCalledTimes(1);
  });

  it('closes search on Escape when search is open', () => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          toggleTheme: mockToggleTheme,
          toggleSearch: mockToggleSearch,
          searchOpen: true,
          alertsOpen: false,
          setSearchOpen: mockSetSearchOpen,
          setAlertsOpen: mockSetAlertsOpen,
        });
      }
      return {
        getState: () => ({
          searchOpen: true,
          alertsOpen: false,
          setSearchOpen: mockSetSearchOpen,
          setAlertsOpen: mockSetAlertsOpen,
        }),
      };
    });

    renderHook(() => useKeyboardShortcuts());

    const event = new KeyboardEvent('keydown', {
      key: 'Escape',
    });
    window.dispatchEvent(event);

    expect(mockSetSearchOpen).toHaveBeenCalledWith(false);
  });

  it('cleans up event listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    const { unmount } = renderHook(() => useKeyboardShortcuts());

    unmount();

    expect(removeEventListenerSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
    removeEventListenerSpy.mockRestore();
  });
});
