// src/components/ui/loading-screen.tsx
import { Spinner } from './spinner';

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = 'Carregando...' }: LoadingScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center h-screen p-4">
      <Spinner size="lg" />
      <p className="mt-4 text-sm sm:text-base text-muted-foreground text-center">{message}</p>
    </div>
  );
}
