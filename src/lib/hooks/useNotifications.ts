// src/lib/hooks/useNotifications.ts
import { toast } from 'sonner';

export const useNotifications = () => {
  const showSuccess = (message: string) => {
    toast.success(message);
  };

  const showError = (message: string) => {
    toast.error(message);
  };

  const showWarning = (message: string) => {
    toast.warning(message);
  };

  const showInfo = (message: string) => {
    toast.info(message);
  };

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };
};
