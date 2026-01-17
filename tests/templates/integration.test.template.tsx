// tests/templates/integration.test.template.tsx
/**
 * Template para testes de integração
 * 
 * INSTRUÇÕES:
 * 1. Copie este arquivo para tests/integration/[categoria]/[nome-feature].test.tsx
 * 2. Substitua [FeatureName] pelo nome da feature
 * 3. Substitua [feature-path] pelo caminho da feature
 * 4. Implemente os testes seguindo o padrão
 * 5. Remova este comentário após implementar
 */

import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { [FeatureName] } from '@/components/[feature-path]';
import { resetStore, setStoreState } from '../helpers/mock-store';

// Mocks necessários
jest.mock('@/lib/hooks/useSomeHook');
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn() }),
  usePathname: () => '/test',
}));

describe('[FeatureName] - Integração', () => {
  beforeEach(() => {
    // Reset store e mocks
    resetStore();
    jest.clearAllMocks();
  });

  // Teste de renderização completa
  it('renders feature correctly', () => {
    // Arrange
    setStoreState({ /* estado inicial */ });

    // Act
    renderWithProviders(<[FeatureName] />);

    // Assert
    expect(screen.getByText('...')).toBeInTheDocument();
  });

  // Teste de fluxo completo
  it('completes full user flow', async () => {
    // Arrange
    const user = userEvent.setup();
    setStoreState({ /* estado inicial */ });

    // Act
    renderWithProviders(<[FeatureName] />);
    
    // Interações do usuário
    const button = screen.getByRole('button', { name: '...' });
    await user.click(button);

    // Assert
    await waitFor(() => {
      expect(screen.getByText('...')).toBeInTheDocument();
    });
  });

  // Teste de integração com store
  it('updates store correctly', async () => {
    // Arrange
    setStoreState({ /* estado inicial */ });

    // Act
    renderWithProviders(<[FeatureName] />);
    // Interagir com componente

    // Assert
    await waitFor(() => {
      const { useAppStore } = require('@/store');
      expect(useAppStore.getState().someState).toBe('expected value');
    });
  });

  // Teste de integração com API
  it('integrates with API correctly', async () => {
    // Arrange
    // Mock da API
    const mockApiResponse = { data: '...' };
    jest.spyOn(require('@/lib/api/services'), 'someService').mockResolvedValue(mockApiResponse);

    // Act
    renderWithProviders(<[FeatureName] />);

    // Assert
    await waitFor(() => {
      expect(screen.getByText('...')).toBeInTheDocument();
    });
  });
});
