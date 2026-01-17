// tests/integration/components/dialog.test.tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

function TestDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button onClick={() => setOpen(true)}>Abrir Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Teste Dialog</DialogTitle>
        </DialogHeader>
        <p>Conteúdo do dialog</p>
      </DialogContent>
    </Dialog>
  );
}

describe('Dialog - Integração', () => {
  it('abre dialog ao clicar no trigger', async () => {
    renderWithProviders(<TestDialog />);

    const trigger = screen.getByText('Abrir Dialog');
    await userEvent.click(trigger);

    await waitFor(() => {
      expect(screen.getByText('Teste Dialog')).toBeInTheDocument();
      expect(screen.getByText('Conteúdo do dialog')).toBeInTheDocument();
    }, { timeout: 2000 });
  });
});
