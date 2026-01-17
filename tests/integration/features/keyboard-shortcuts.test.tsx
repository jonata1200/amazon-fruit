// tests/integration/features/keyboard-shortcuts.test.tsx
import { renderWithProviders } from '../helpers/render-with-providers';
import { KeyboardShortcutsHelp } from '@/components/features/keyboard/keyboard-shortcuts-help';
import { resetStore } from '../helpers/mock-store';

describe('Atalhos de Teclado - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
  });

  it('renderiza componente de ajuda de atalhos', () => {
    const { container } = renderWithProviders(
      <div>
        <KeyboardShortcutsHelp />
      </div>
    );
    
    // Verificar se o componente renderiza
    expect(container).toBeInTheDocument();
  });

  it('componente está presente no DOM', () => {
    const { container } = renderWithProviders(<KeyboardShortcutsHelp />);
    
    // Verificar estrutura básica
    expect(container.firstChild).toBeInTheDocument();
  });
});
