// tests/templates/component.test.template.tsx
/**
 * Template para testes de componentes React
 * 
 * INSTRUÇÕES:
 * 1. Copie este arquivo para tests/unit/components/[categoria]/[nome-componente].test.tsx
 * 2. Substitua [ComponentName] pelo nome do componente
 * 3. Substitua [component-path] pelo caminho do componente
 * 4. Implemente os testes seguindo o padrão AAA (Arrange-Act-Assert)
 * 5. Remova este comentário após implementar
 */

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { [ComponentName] } from '@/components/[component-path]';

describe('[ComponentName]', () => {
  // Arrange: Preparar dados e mocks comuns
  const defaultProps = {
    // Adicione props padrão aqui
  };

  beforeEach(() => {
    // Setup antes de cada teste (se necessário)
    jest.clearAllMocks();
  });

  // Teste básico de renderização
  it('renders correctly with default props', () => {
    // Arrange
    const props = { ...defaultProps };

    // Act
    render(<[ComponentName] {...props} />);

    // Assert
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  // Teste de props
  it('applies props correctly', () => {
    // Arrange
    const props = {
      ...defaultProps,
      // Adicione props específicas aqui
    };

    // Act
    render(<[ComponentName] {...props} />);

    // Assert
    // Verifique se as props foram aplicadas corretamente
  });

  // Teste de interações do usuário
  it('handles user interactions', async () => {
    // Arrange
    const user = userEvent.setup();
    const props = { ...defaultProps };

    // Act
    render(<[ComponentName] {...props} />);
    const button = screen.getByRole('button');
    await user.click(button);

    // Assert
    // Verifique o resultado da interação
  });

  // Teste de estados
  it('handles different states', () => {
    // Arrange
    const props = {
      ...defaultProps,
      // Estado específico
    };

    // Act
    render(<[ComponentName] {...props} />);

    // Assert
    // Verifique o estado renderizado
  });

  // Teste de casos de borda
  it('handles edge cases', () => {
    // Arrange
    const props = {
      ...defaultProps,
      // Caso de borda (valores vazios, null, undefined, etc.)
    };

    // Act
    render(<[ComponentName] {...props} />);

    // Assert
    // Verifique o comportamento em casos de borda
  });

  // Teste de acessibilidade
  it('is accessible', () => {
    // Arrange
    const props = { ...defaultProps };

    // Act
    const { container } = render(<[ComponentName] {...props} />);

    // Assert
    // Verifique atributos de acessibilidade
    expect(container.querySelector('[aria-label]')).toBeInTheDocument();
  });
});
