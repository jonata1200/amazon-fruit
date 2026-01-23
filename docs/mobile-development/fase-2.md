# 🧩 Fase 2: Otimização de Componentes Base

**Duração Estimada**: 5-7 dias  
**Objetivo**: Garantir que todos os componentes UI base funcionem perfeitamente em mobile

---

## 📋 Checklist

### Componentes de Layout
- [ ] Otimizar `Header` para mobile (menu hambúrguer, logo reduzido)
- [ ] Adaptar `Sidebar` para drawer mobile (slide-in menu)
- [ ] Otimizar `Footer` para mobile (layout vertical, links empilhados)
- [ ] Criar componente `BottomNavigation` (se necessário)
- [ ] Implementar `MobileLayout` wrapper

### Componentes UI Base
- [ ] Otimizar `Button` para touch targets (mínimo 44x44px)
- [ ] Adaptar `Card` para mobile (padding, espaçamento)
- [ ] Otimizar `Input` para mobile (tamanho de fonte, zoom desabilitado)
- [ ] Adaptar `Dialog`/`Modal` para mobile (fullscreen ou bottom sheet)
- [ ] Otimizar `Dropdown` para mobile (touch-friendly)
- [ ] Adaptar `DataTable` para mobile (scroll horizontal ou cards)
- [ ] Otimizar `Tooltip` para mobile (touch interactions)

### Componentes de Feedback
- [ ] Adaptar `Toast`/`Notification` para mobile (posicionamento)
- [ ] Otimizar `Loading` states para mobile
- [ ] Adaptar `Skeleton` loaders para mobile
- [ ] Otimizar `EmptyState` para mobile

### Componentes de Navegação
- [ ] Criar/otimizar `Breadcrumbs` para mobile
- [ ] Adaptar `Tabs` para mobile (scroll horizontal se necessário)
- [ ] Otimizar `Pagination` para mobile
- [ ] Criar componente `FloatingActionButton` (se necessário)

### Acessibilidade Mobile
- [ ] Garantir touch targets adequados (mínimo 44x44px)
- [ ] Testar com leitores de tela mobile
- [ ] Verificar contraste de cores em telas mobile
- [ ] Otimizar navegação por teclado virtual

---

## 📝 Notas

Esta fase estabelece a base para todas as outras fases. Garanta que todos os componentes fundamentais estejam funcionando perfeitamente antes de prosseguir.

### Dicas
- Use o Chrome DevTools para testar diferentes tamanhos de tela
- Teste em dispositivos reais sempre que possível
- Mantenha consistência com o design system existente
- Documente mudanças significativas nos componentes

---

**Fase Anterior**: [Fase 1: Análise e Planejamento](./fase-1.md)  
**Próxima Fase**: [Fase 3: Adaptação de Layouts e Navegação](./fase-3.md)  
**Voltar**: [Índice](./index.md)
