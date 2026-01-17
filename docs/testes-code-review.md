# 📋 Guia de Code Review para Testes

Checklist e diretrizes para revisar testes em Pull Requests.

## ✅ Checklist Básico

### Estrutura e Organização
- [ ] Testes seguem o padrão AAA (Arrange-Act-Assert)
- [ ] Testes estão no local correto (`tests/unit/` ou `tests/integration/`)
- [ ] Arquivo de teste tem nome descritivo (`*.test.tsx`)
- [ ] Testes estão agrupados logicamente com `describe`

### Qualidade dos Testes
- [ ] Nomes de testes são descritivos e claros
- [ ] Cada teste verifica um comportamento específico
- [ ] Testes são independentes (não dependem de outros)
- [ ] Testes não são duplicados ou redundantes
- [ ] Casos de borda são cobertos (valores vazios, null, undefined, etc.)

### Mocks e Fixtures
- [ ] Mocks são apropriados e não excessivos
- [ ] Mocks são limpos no `beforeEach` ou `afterEach`
- [ ] Fixtures são reutilizáveis quando possível
- [ ] Mocks não expõem detalhes de implementação

### Cobertura
- [ ] Novos componentes/hooks têm testes
- [ ] Cobertura não diminuiu significativamente
- [ ] Código crítico tem cobertura adequada
- [ ] Branches condicionais são testados

### Performance
- [ ] Testes são rápidos (< 1s cada, idealmente)
- [ ] Não há operações desnecessárias
- [ ] Mocks são usados em vez de implementações pesadas

### Acessibilidade
- [ ] Testes verificam atributos de acessibilidade quando relevante
- [ ] Navegação por teclado é testada quando aplicável
- [ ] ARIA labels são verificados quando presentes

## 🎯 Critérios de Aprovação

### Deve Aprovar Se:
- ✅ Todos os testes passam
- ✅ Cobertura mantém ou aumenta
- ✅ Testes seguem padrões do projeto
- ✅ Testes são claros e mantíveis
- ✅ Casos importantes são cobertos

### Deve Solicitar Mudanças Se:
- ❌ Testes falham ou são instáveis
- ❌ Cobertura diminui significativamente
- ❌ Testes testam implementação em vez de comportamento
- ❌ Testes são difíceis de entender
- ❌ Faltam testes para código crítico
- ❌ Testes são muito lentos

## 📝 Exemplos de Comentários Úteis

### Bom Teste
```typescript
// ✅ Bom exemplo
it('displays error message when API call fails', async () => {
  // Arrange
  mockApi.getData.mockRejectedValue(new Error('API Error'));
  
  // Act
  render(<Component />);
  
  // Assert
  await waitFor(() => {
    expect(screen.getByText('Erro ao carregar dados')).toBeInTheDocument();
  });
});
```

**Comentário:** "Ótimo teste! Cobre o caso de erro e usa waitFor corretamente."

### Teste que Precisa Melhorar
```typescript
// ❌ Precisa melhorar
it('test1', () => {
  render(<Component />);
  expect(screen.getByText('text')).toBeInTheDocument();
});
```

**Comentário:** "Por favor, melhore este teste:
1. Nome mais descritivo: `it('renders component with text')`
2. Adicione comentários AAA para clareza
3. Considere testar casos de borda também"

## 🔍 O Que Verificar

### 1. Nomes Descritivos
```typescript
// ✅ Bom
it('displays loading spinner while fetching data')

// ❌ Ruim
it('test1')
it('works')
```

### 2. Teste de Comportamento, Não Implementação
```typescript
// ✅ Bom - testa comportamento
expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();

// ❌ Ruim - testa implementação
expect(component.state.isLoading).toBe(true);
```

### 3. Casos de Borda
```typescript
// ✅ Bom - cobre casos de borda
it('handles empty data array')
it('handles null values')
it('handles undefined props')
```

### 4. Isolamento
```typescript
// ✅ Bom - isolado
beforeEach(() => {
  jest.clearAllMocks();
  resetStore();
});

// ❌ Ruim - depende de estado anterior
// Sem cleanup
```

## 🚨 Red Flags

Sinais de que o teste precisa de atenção:

1. **Teste muito longo** (> 50 linhas) - pode testar muitas coisas
2. **Muitos mocks** (> 5) - componente pode ter muitas dependências
3. **Teste instável** - pode ser flaky
4. **Sem cleanup** - pode afetar outros testes
5. **Testa detalhes internos** - frágil a mudanças
6. **Nomes genéricos** - difícil de entender

## 💡 Sugestões de Melhoria

Ao revisar, sugira:

- **Padrões:** "Considere usar o padrão AAA para clareza"
- **Cobertura:** "Este componente crítico poderia ter mais testes de casos de erro"
- **Performance:** "Este teste está lento, considere usar mocks"
- **Clareza:** "Este teste seria mais claro com comentários explicando cada etapa"

## 📚 Referências

- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Jest Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
- [Guia de Testes do Projeto](./testes.md)
