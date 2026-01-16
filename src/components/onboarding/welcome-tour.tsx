// src/components/onboarding/welcome-tour.tsx
'use client';

import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion, AnimatePresence } from 'framer-motion';

interface TourStep {
  id: string;
  title: string;
  content: string;
  target?: string; // Seletor CSS do elemento alvo
}

const TOUR_STORAGE_KEY = 'amazon-fruit-tour-completed';

const defaultSteps: TourStep[] = [
  {
    id: 'welcome',
    title: 'Bem-vindo ao Amazon Fruit!',
    content: 'Este é um sistema completo de dashboards para gestão de negócios. Vamos começar com um tour rápido.',
  },
  {
    id: 'sidebar',
    title: 'Navegação',
    content: 'Use o menu lateral para navegar entre os diferentes dashboards: Visão Geral, Finanças, Estoque, e muito mais.',
    target: 'aside nav',
  },
  {
    id: 'period',
    title: 'Seleção de Período',
    content: 'Use o seletor de período para filtrar dados por datas específicas. Você pode escolher um período personalizado.',
    target: 'input[type="date"]',
  },
  {
    id: 'export',
    title: 'Exportação de Dados',
    content: 'Você pode exportar relatórios em diferentes formatos: PDF, Excel ou CSV. Use o botão "Exportar" quando disponível.',
  },
  {
    id: 'shortcuts',
    title: 'Atalhos de Teclado',
    content: 'Use Ctrl+K para busca global, Ctrl+T para alternar tema, e ESC para fechar painéis abertos.',
  },
];

interface WelcomeTourProps {
  onComplete?: () => void;
}

export function WelcomeTour({ onComplete }: WelcomeTourProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [shouldShow, setShouldShow] = useState(false);

  useEffect(() => {
    // Verificar se o tour já foi completado
    const completed = localStorage.getItem(TOUR_STORAGE_KEY) === 'true';
    if (!completed) {
      // Mostrar após um pequeno delay
      const timer = setTimeout(() => {
        setShouldShow(true);
        setIsOpen(true);
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleNext = () => {
    if (currentStep < defaultSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handleSkip = () => {
    handleComplete();
  };

  const handleComplete = () => {
    localStorage.setItem(TOUR_STORAGE_KEY, 'true');
    setIsOpen(false);
    setShouldShow(false);
    if (onComplete) {
      onComplete();
    }
  };

  if (!shouldShow || !isOpen) {
    return null;
  }

  const currentStepData = defaultSteps[currentStep];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-40"
            onClick={handleSkip}
          />

          {/* Tour Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md"
          >
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>{currentStepData.title}</CardTitle>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleSkip}
                    aria-label="Fechar tour"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-muted-foreground">{currentStepData.content}</p>

                {/* Progress indicator */}
                <div className="flex gap-1">
                  {defaultSteps.map((_, index) => (
                    <div
                      key={index}
                      className={cn(
                        'h-2 flex-1 rounded-full transition-colors',
                        index === currentStep
                          ? 'bg-primary'
                          : index < currentStep
                            ? 'bg-primary/50'
                            : 'bg-muted'
                      )}
                      aria-hidden="true"
                    />
                  ))}
                </div>

                {/* Actions */}
                <div className="flex justify-between gap-2">
                  <Button variant="outline" onClick={handleSkip}>
                    Pular tour
                  </Button>
                  <Button onClick={handleNext}>
                    {currentStep === defaultSteps.length - 1 ? 'Concluir' : 'Próximo'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// Helper necessário para cn
import { cn } from '@/lib/utils';
