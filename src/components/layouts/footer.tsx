// src/components/layouts/footer.tsx
'use client';

import { useEffect, useState } from 'react';

export function Footer() {
  const [year, setYear] = useState<number | null>(null);

  useEffect(() => {
    // Só definir o ano no cliente para evitar problemas de hidratação
    setYear(new Date().getFullYear());
  }, []);

  // Usar um valor estático no servidor para evitar diferenças de hidratação
  const displayYear = year ?? '2024';

  return (
    <footer className="border-t py-4 px-6">
      <p className="text-center text-sm text-muted-foreground">
        &copy; {displayYear} Amazon Fruit - Sistema de Análise de Dados
      </p>
    </footer>
  );
}
