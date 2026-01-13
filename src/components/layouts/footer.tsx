// src/components/layouts/footer.tsx
export function Footer() {
  return (
    <footer className="border-t py-4 px-6">
      <p className="text-center text-sm text-muted-foreground">
        &copy; {new Date().getFullYear()} Amazon Fruit - Sistema de Análise de Dados
      </p>
    </footer>
  );
}
