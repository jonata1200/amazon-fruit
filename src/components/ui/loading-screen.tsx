// src/components/ui/loading-screen.tsx
import { Spinner } from './spinner';

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = 'Carregando...' }: LoadingScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Spinner size="lg" />
      <p className="mt-4 text-muted-foreground">{message}</p>
    </div>
  );
}
