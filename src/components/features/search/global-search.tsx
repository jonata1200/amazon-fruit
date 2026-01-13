// src/components/features/search/global-search.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAppStore } from '@/store';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, X, Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { useDebounce } from '@/lib/hooks/useDebounce';

export function GlobalSearch() {
  const router = useRouter();
  const searchOpen = useAppStore((state) => state.searchOpen);
  const setSearchOpen = useAppStore((state) => state.setSearchOpen);

  const [query, setQuery] = useState('');
  const [results, setResults] = useState<
    Array<{ id: string; title: string; description: string; url: string }>
  >([]);
  const [isLoading, setIsLoading] = useState(false);

  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery.length >= 3) {
      performSearch(debouncedQuery);
    } else {
      setResults([]);
    }
  }, [debouncedQuery]);

  const performSearch = async (searchQuery: string) => {
    setIsLoading(true);
    try {
      // Simular busca por enquanto (API será implementada no backend)
      const mockResults = [
        {
          id: '1',
          title: 'Dashboard Geral',
          description: 'Visão geral do negócio com KPIs principais',
          url: '/geral',
        },
        {
          id: '2',
          title: 'Dashboard de Finanças',
          description: 'Análise financeira detalhada',
          url: '/financas',
        },
        {
          id: '3',
          title: 'Dashboard de Estoque',
          description: 'Controle de estoque e produtos',
          url: '/estoque',
        },
        {
          id: '4',
          title: 'Dashboard de Público-Alvo',
          description: 'Análise de público e segmentação',
          url: '/publico-alvo',
        },
        {
          id: '5',
          title: 'Dashboard de Fornecedores',
          description: 'Gestão de fornecedores',
          url: '/fornecedores',
        },
        {
          id: '6',
          title: 'Dashboard de RH',
          description: 'Recursos humanos e colaboradores',
          url: '/recursos-humanos',
        },
      ];

      const filtered = mockResults.filter(
        (item) =>
          item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.toLowerCase())
      );

      setResults(filtered);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResultClick = (url: string) => {
    router.push(url);
    setSearchOpen(false);
    setQuery('');
    setResults([]);
  };

  const handleClose = () => {
    setSearchOpen(false);
    setQuery('');
    setResults([]);
  };

  if (!searchOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm" onClick={handleClose}>
      <div className="container mx-auto max-w-2xl px-4 py-20" onClick={(e) => e.stopPropagation()}>
        <Card>
          <CardContent className="p-6">
            {/* Search Input */}
            <div className="flex items-center gap-2 mb-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Buscar em todos os dashboards..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="pl-10"
                  autoFocus
                />
              </div>
              <Button variant="ghost" size="icon" onClick={handleClose}>
                <X className="h-5 w-5" />
              </Button>
            </div>

            {/* Results */}
            <div className="space-y-2">
              {isLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              ) : results.length > 0 ? (
                results.map((result) => (
                  <button
                    key={result.id}
                    onClick={() => handleResultClick(result.url)}
                    className="w-full text-left p-3 rounded-lg hover:bg-muted transition-colors"
                  >
                    <p className="font-medium">{result.title}</p>
                    <p className="text-sm text-muted-foreground">{result.description}</p>
                  </button>
                ))
              ) : query.length >= 3 ? (
                <div className="py-8 text-center text-muted-foreground">
                  Nenhum resultado encontrado
                </div>
              ) : (
                <div className="py-8 text-center text-muted-foreground">
                  Digite pelo menos 3 caracteres para buscar
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
