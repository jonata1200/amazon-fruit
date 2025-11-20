# Guia de Teste - Endpoints de Análise

## ✅ Endpoints Disponíveis

### Análise Financeira

#### 1. Resumo Financeiro
```
GET /api/analysis/financial/summary?start_date=2020-01-01&end_date=2020-12-31
```

**Retorna:**
- Receita, despesa, lucro
- Variações percentuais comparadas ao período anterior

#### 2. Top Despesas
```
GET /api/analysis/financial/top-expenses?start_date=2020-01-01&end_date=2020-12-31&top_n=5
```

**Retorna:**
- Top N categorias de despesas ordenadas por valor

#### 3. Top Receitas
```
GET /api/analysis/financial/top-revenues?start_date=2020-01-01&end_date=2020-12-31&top_n=5
```

**Retorna:**
- Top N categorias de receitas ordenadas por valor

### Análise de Estoque

#### 4. Top Produtos Vendidos
```
GET /api/analysis/inventory/top-selling?start_date=2020-01-01&end_date=2020-12-31&top_n=10
```

**Retorna:**
- Top N produtos por faturamento total

#### 5. Produtos com Estoque Baixo
```
GET /api/analysis/inventory/low-stock?start_date=2020-01-01&end_date=2020-12-31&top_n=10
```

**Retorna:**
- Produtos com estoque abaixo do nível mínimo (rupturas)

#### 6. KPIs de Estoque
```
GET /api/analysis/inventory/kpis?start_date=2020-01-01&end_date=2020-12-31
```

**Retorna:**
- Produtos únicos, valor total do estoque, itens com estoque baixo
- Variações percentuais

### Análise de Fornecedores

#### 7. Top e Bottom Fornecedores
```
GET /api/analysis/suppliers/top-bottom?n=5
```

**Retorna:**
- Top N melhores fornecedores
- Top N piores fornecedores (por avaliação)

#### 8. Distribuição por Estado
```
GET /api/analysis/suppliers/by-state
```

**Retorna:**
- Contagem de fornecedores por estado

### Análise de Público-Alvo

#### 9. Clientes por Localização
```
GET /api/analysis/public/by-location?start_date=2020-01-01&end_date=2020-12-31&top_n=10
```

**Retorna:**
- Top N cidades com mais clientes

#### 10. Distribuição por Gênero
```
GET /api/analysis/public/by-gender?start_date=2020-01-01&end_date=2020-12-31
```

**Retorna:**
- Contagem de clientes por gênero

#### 11. Distribuição por Canal
```
GET /api/analysis/public/by-channel?start_date=2020-01-01&end_date=2020-12-31
```

**Retorna:**
- Contagem de clientes por canal de venda

### Análise de Recursos Humanos

#### 12. Headcount por Departamento
```
GET /api/analysis/hr/by-department
```

**Retorna:**
- Número de funcionários por departamento

#### 13. Custo por Departamento
```
GET /api/analysis/hr/cost-by-department
```

**Retorna:**
- Custo mensal total por departamento

#### 14. Distribuição por Cargo
```
GET /api/analysis/hr/by-role
```

**Retorna:**
- Top 10 cargos na empresa

#### 15. Histórico de Contratações
```
GET /api/analysis/hr/hiring-over-time
```

**Retorna:**
- Contagem de contratações por período (mês/ano)

## 🧪 Como Testar

### Opção 1: Swagger UI (Recomendado)

1. Acesse: http://localhost:8000/docs
2. Procure pela seção **"analysis"**
3. Expanda o endpoint desejado
4. Clique em **"Try it out"**
5. Preencha os parâmetros (datas, top_n, etc.)
6. Clique em **"Execute"**
7. Veja a resposta JSON

### Opção 2: Navegador

Copie e cole a URL completa no navegador:
```
http://localhost:8000/api/analysis/financial/summary?start_date=2020-01-01&end_date=2020-12-31
```

### Opção 3: cURL (Terminal)

```bash
curl "http://localhost:8000/api/analysis/financial/summary?start_date=2020-01-01&end_date=2020-12-31"
```

## 📋 Checklist de Testes

### Análise Financeira
- [ ] Resumo financeiro retorna receita, despesa, lucro
- [ ] Variações percentuais calculadas corretamente
- [ ] Top despesas ordenadas corretamente
- [ ] Top receitas ordenadas corretamente

### Análise de Estoque
- [ ] Top produtos retorna produtos mais vendidos
- [ ] Estoque baixo retorna produtos em ruptura
- [ ] KPIs incluem produtos únicos e valor total

### Análise de Fornecedores
- [ ] Top/bottom fornecedores ordenados por avaliação
- [ ] Distribuição por estado funciona

### Análise de Público-Alvo
- [ ] Clientes por localização retorna top cidades
- [ ] Distribuição por gênero funciona
- [ ] Distribuição por canal funciona

### Análise de RH
- [ ] Headcount por departamento funciona
- [ ] Custo por departamento calculado corretamente
- [ ] Distribuição por cargo retorna top 10
- [ ] Histórico de contratações agrupado por período

## ⚠️ Notas Importantes

1. **Datas obrigatórias:** A maioria dos endpoints requer `start_date` e `end_date`
2. **Formato de data:** Use formato ISO (YYYY-MM-DD)
3. **Top N:** Parâmetro opcional, padrão varia por endpoint
4. **Período anterior:** Endpoints comparativos calculam automaticamente o período anterior

## 🎯 Próximos Passos

Após testar os endpoints de análise:
- ✅ Continuar com conversão de gráficos
- ✅ Criar endpoints de dashboards agregados
- ✅ Implementar sistema de relatórios PDF

