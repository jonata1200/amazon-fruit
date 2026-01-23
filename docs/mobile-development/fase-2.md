# 🧩 Fase 2: Otimização de Componentes Base

**Duração Estimada**: 5-7 dias  
**Objetivo**: Garantir que todos os componentes UI base funcionem perfeitamente em mobile

---

## 📋 Checklist

### Componentes de Layout
- [x] Otimizar `Header` para mobile (menu hambúrguer, logo reduzido)
- [x] Adaptar `Sidebar` para drawer mobile (slide-in menu)
- [x] Otimizar `Footer` para mobile (layout vertical, links empilhados)
- [ ] Criar componente `BottomNavigation` (se necessário - opcional)
- [ ] Implementar `MobileLayout` wrapper (opcional)

### Componentes UI Base
- [x] Otimizar `Button` para touch targets (mínimo 44x44px)
- [x] Adaptar `Card` para mobile (padding, espaçamento)
- [x] Otimizar `Input` para mobile (tamanho de fonte, zoom desabilitado)
- [x] Adaptar `Dialog`/`Modal` para mobile (fullscreen ou bottom sheet)
- [x] Otimizar `Dropdown` para mobile (touch-friendly)
- [x] Adaptar `DataTable` para mobile (scroll horizontal ou cards)
- [x] Otimizar `Tooltip` para mobile (touch interactions)

### Componentes de Feedback
- [x] Adaptar `Toast`/`Notification` para mobile (posicionamento)
- [x] Otimizar `Loading` states para mobile
- [x] Adaptar `Skeleton` loaders para mobile
- [x] Otimizar `EmptyState` para mobile

### Componentes de Navegação
- [ ] Criar/otimizar `Breadcrumbs` para mobile (componente não existe)
- [ ] Adaptar `Tabs` para mobile (scroll horizontal se necessário - componente não existe)
- [ ] Otimizar `Pagination` para mobile (componente não existe)
- [ ] Criar componente `FloatingActionButton` (se necessário - opcional)

### Acessibilidade Mobile
- [x] Garantir touch targets adequados (mínimo 44x44px)
- [ ] Testar com leitores de tela mobile (requer testes manuais)
- [ ] Verificar contraste de cores em telas mobile (requer validação)
- [x] Otimizar navegação por teclado virtual (Input com font-size adequado)

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
