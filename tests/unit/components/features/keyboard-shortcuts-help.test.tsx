// tests/unit/components/features/keyboard-shortcuts-help.test.tsx
import { render, screen } from '@testing-library/react';
import { KeyboardShortcutsHelp } from '@/components/features/keyboard/keyboard-shortcuts-help';

describe('KeyboardShortcutsHelp', () => {
  it('renders shortcuts help card', () => {
    render(<KeyboardShortcutsHelp />);
    expect(screen.getByText('Atalhos de Teclado')).toBeInTheDocument();
  });

  it('displays all shortcuts', () => {
    render(<KeyboardShortcutsHelp />);
    expect(screen.getByText('Abrir busca global')).toBeInTheDocument();
    expect(screen.getByText('Alternar tema')).toBeInTheDocument();
    expect(screen.getByText('Fechar painéis')).toBeInTheDocument();
  });

  it('displays shortcut keys', () => {
    render(<KeyboardShortcutsHelp />);
    expect(screen.getByText('Ctrl + K')).toBeInTheDocument();
    expect(screen.getByText('Ctrl + T')).toBeInTheDocument();
    expect(screen.getByText('ESC')).toBeInTheDocument();
  });
});
