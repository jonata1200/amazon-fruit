// tests/integration/components/form-integration.test.tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

function TestForm() {
  const [value, setValue] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value) {
      setError('Campo obrigatório');
      return;
    }
    setSubmitted(true);
    setError('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-2">
        <Label htmlFor="test-input">Campo de Teste</Label>
        <Input
          id="test-input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          aria-invalid={!!error}
        />
        {error && <p className="text-sm text-red-600">{error}</p>}
        {submitted && <p className="text-sm text-green-600">Formulário enviado!</p>}
      </div>
      <Button type="submit" className="mt-4">
        Enviar
      </Button>
    </form>
  );
}

describe('Formulário Completo - Integração', () => {
  it('renderiza formulário com input, label e button', () => {
    renderWithProviders(<TestForm />);

    expect(screen.getByLabelText('Campo de Teste')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Enviar' })).toBeInTheDocument();
  });

  it('preenche e submete formulário', async () => {
    renderWithProviders(<TestForm />);

    const input = screen.getByLabelText('Campo de Teste');
    const submitButton = screen.getByRole('button', { name: 'Enviar' });

    await userEvent.type(input, 'Teste');
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Formulário enviado!')).toBeInTheDocument();
    });
  });

  it('exibe erro de validação quando campo está vazio', async () => {
    renderWithProviders(<TestForm />);

    const submitButton = screen.getByRole('button', { name: 'Enviar' });
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Campo obrigatório')).toBeInTheDocument();
    });
  });

  it('associa label corretamente com input', () => {
    renderWithProviders(<TestForm />);

    const input = screen.getByLabelText('Campo de Teste');
    expect(input).toHaveAttribute('id', 'test-input');
  });
});
