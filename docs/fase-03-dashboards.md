# Fase 3: Migração dos Dashboards

## Objetivo

Converter todos os dashboards PyQt6 em interfaces web responsivas e interativas, mantendo toda a funcionalidade e melhorando a experiência do usuário.

## Duração Estimada

**3-4 semanas**

## Tarefas Detalhadas

### 3.1 Estrutura Base do Frontend

#### 3.1.1 Template Base HTML

**Arquivo:** `frontend/templates/base.html`

**Estrutura:**
- Layout responsivo
- Menu lateral de navegação (equivalente ao PyQt6)
- Área de conteúdo principal
- Barra de período (equivalente ao PeriodBar)
- Footer

**Componentes necessários:**
- [ ] Header com logo
- [ ] Menu lateral (sidebar) com navegação
- [ ] Área de conteúdo principal
- [ ] Barra de filtro de período
- [ ] Sistema de rotas/tabs

**Tarefas:**
- [ ] Criar template base HTML
- [ ] Adicionar CSS básico
- [ ] Implementar layout responsivo
- [ ] Adicionar JavaScript para navegação
- [ ] Testar em diferentes tamanhos de tela

#### 3.1.2 Sistema de Navegação

**Estratégia:**
- Usar JavaScript vanilla ou framework leve
- Implementar sistema de rotas simples
- Manter estado da página atual

**Arquivo:** `frontend/static/js/app.js`

**Funcionalidades:**
- [ ] Navegação entre dashboards
- [ ] Highlight do menu ativo
- [ ] Histórico de navegação (opcional)
- [ ] Carregamento dinâmico de conteúdo

### 3.2 Barra de Período (PeriodBar)

#### 3.2.1 Componente HTML/CSS

**Arquivo:** `frontend/templates/components/period_bar.html`

**Equivalente ao:** `modules/ui/widgets/period_bar.py`

**Funcionalidades:**
- [ ] Input de data inicial
- [ ] Input de data final
- [ ] Botão "Aplicar"
- [ ] Indicador de carregamento
- [ ] Mensagens de sucesso/erro

**Tarefas:**
- [ ] Criar HTML do componente
- [ ] Estilizar com CSS
- [ ] Implementar JavaScript para comunicação com API
- [ ] Adicionar validação de datas
- [ ] Adicionar feedback visual

#### 3.2.2 Integração com API

**JavaScript:**
```javascript
async function applyPeriod(startDate, endDate) {
    // Mostrar loading
    showLoading();
    
    try {
        // Atualizar período na API
        await fetch(`/api/data/period?start=${startDate}&end=${endDate}`, {
            method: 'POST'
        });
        
        // Recarregar todos os dashboards
        await refreshAllDashboards();
        
        // Mostrar sucesso
        showSuccess('Período atualizado com sucesso!');
    } catch (error) {
        showError('Erro ao atualizar período');
    } finally {
        hideLoading();
    }
}
```

### 3.3 Dashboard Geral

#### 3.3.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/geral.html`

**Componentes:**
- [ ] Título "Visão Geral do Negócio"
- [ ] Botão "Gerar Relatório"
- [ ] Container para gráfico de evolução
- [ ] Área para KPIs (opcional)

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Estilizar com CSS
- [ ] Adicionar botão de relatório

#### 3.3.2 Gráfico de Evolução

**JavaScript:** `frontend/static/js/dashboards/geral.js`

**Funcionalidades:**
- [ ] Buscar dados da API (`/api/dashboard/geral`)
- [ ] Renderizar gráfico Plotly
- [ ] Atualizar ao mudar período
- [ ] Tratamento de erros

**Código exemplo:**
```javascript
async function loadGeralDashboard(startDate, endDate) {
    try {
        const response = await fetch(
            `/api/dashboard/geral?start_date=${startDate}&end_date=${endDate}`
        );
        const data = await response.json();
        
        // Renderizar gráfico Plotly
        Plotly.newPlot('chart-evolucao', data.chart_data, data.layout);
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}
```

**Tarefas:**
- [ ] Implementar função de carregamento
- [ ] Integrar com Plotly.js
- [ ] Adicionar tratamento de erros
- [ ] Adicionar loading state
- [ ] Testar com dados reais

#### 3.3.3 Geração de Relatório

**Funcionalidade:**
- [ ] Botão "Gerar Relatório" faz requisição para API
- [ ] API retorna PDF
- [ ] Download automático do PDF

**JavaScript:**
```javascript
async function generateReport(startDate, endDate) {
    try {
        const response = await fetch(
            `/api/reports/full?start_date=${startDate}&end_date=${endDate}`
        );
        const blob = await response.blob();
        
        // Criar link de download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Relatorio_Geral_${startDate}_${endDate}.pdf`;
        a.click();
    } catch (error) {
        alert('Erro ao gerar relatório');
    }
}
```

### 3.4 Dashboard de Finanças

#### 3.4.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/financas.html`

**Componentes:**
- [ ] Título "Finanças"
- [ ] Seção de KPIs (Receita, Despesa, Lucro)
- [ ] Gráfico de Evolução Financeira
- [ ] Gráfico Top 5 Despesas
- [ ] Gráfico Top 5 Receitas
- [ ] Tabela de dados financeiros

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Estilizar com CSS
- [ ] Criar layout responsivo (grid)

#### 3.4.2 Widgets de KPI

**Componente:** `frontend/templates/components/kpi_widget.html`

**Equivalente ao:** `modules/ui/widgets/kpi_widget.py`

**Funcionalidades:**
- [ ] Exibir valor principal
- [ ] Exibir variação percentual
- [ ] Indicador visual (seta para cima/baixo)
- [ ] Cores diferentes para positivo/negativo

**Tarefas:**
- [ ] Criar componente HTML/CSS
- [ ] Implementar JavaScript para atualização
- [ ] Adicionar animações (opcional)

#### 3.4.3 Gráficos

**JavaScript:** `frontend/static/js/dashboards/financas.js`

**Gráficos necessários:**
- [ ] Evolução Financeira Mensal
- [ ] Top 5 Despesas por Categoria
- [ ] Top 5 Receitas por Categoria

**Tarefas:**
- [ ] Implementar carregamento de cada gráfico
- [ ] Integrar com Plotly.js
- [ ] Adicionar tratamento de erros
- [ ] Testar atualização dinâmica

#### 3.4.4 Tabela de Dados

**Componente:** Tabela HTML responsiva ou DataTables.js

**Funcionalidades:**
- [ ] Exibir dados financeiros
- [ ] Ordenação por colunas
- [ ] Busca/filtro
- [ ] Paginação (se necessário)

**Tarefas:**
- [ ] Criar tabela HTML
- [ ] Adicionar funcionalidades de ordenação/busca
- [ ] Estilizar com CSS
- [ ] Testar com grandes volumes de dados

### 3.5 Dashboard de Estoque

#### 3.5.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/estoque.html`

**Componentes:**
- [ ] Título "Estoque"
- [ ] Gráfico Top 10 Produtos por Faturamento
- [ ] Gráfico 10 Produtos com Menor Faturamento
- [ ] Gráfico Maiores Rupturas de Estoque
- [ ] Tabela de dados de estoque

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Estilizar com CSS
- [ ] Implementar layout de grid

#### 3.5.2 Gráficos de Estoque

**JavaScript:** `frontend/static/js/dashboards/estoque.js`

**Gráficos:**
- [ ] Top 10 Produtos por Faturamento
- [ ] 10 Produtos com Menor Faturamento
- [ ] Maiores Rupturas de Estoque

**Tarefas:**
- [ ] Implementar carregamento de gráficos
- [ ] Integrar com Plotly.js
- [ ] Adicionar interatividade
- [ ] Testar atualização

### 3.6 Dashboard de Público-Alvo

#### 3.6.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/publico_alvo.html`

**Componentes:**
- [ ] Título "Público-Alvo"
- [ ] Gráfico Top 10 Clientes por Localização
- [ ] Gráfico Distribuição por Gênero (pizza)
- [ ] Gráfico Contagem por Canal de Venda
- [ ] Tabela de dados de clientes

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Estilizar com CSS
- [ ] Implementar gráficos

### 3.7 Dashboard de Fornecedores

#### 3.7.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/fornecedores.html`

**Componentes:**
- [ ] Título "Fornecedores"
- [ ] Gráfico Top 5 Melhores Fornecedores
- [ ] Gráfico Top 5 Piores Fornecedores
- [ ] Gráfico Distribuição por Estado
- [ ] Heatmap Matriz de Fornecedores por Produtos
- [ ] Tabela de dados de fornecedores

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Implementar heatmap com Plotly
- [ ] Estilizar com CSS

### 3.8 Dashboard de Recursos Humanos

#### 3.8.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/recursos_humanos.html`

**Componentes:**
- [ ] Título "Recursos Humanos"
- [ ] Gráfico Nº de Funcionários por Departamento
- [ ] Gráfico Custo Mensal por Departamento
- [ ] Gráfico Top 10 Cargos
- [ ] Gráfico Histórico de Contratações
- [ ] Tabela de dados de RH

**Tarefas:**
- [ ] Criar estrutura HTML
- [ ] Implementar gráficos
- [ ] Estilizar com CSS

### 3.9 Dashboard de Insights

#### 3.9.1 Template HTML

**Arquivo:** `frontend/templates/dashboards/insights.html`

**Componentes:**
- [ ] Título "Insights"
- [ ] Análises avançadas
- [ ] Visualizações específicas

**Tarefas:**
- [ ] Analisar funcionalidades do dashboard original
- [ ] Criar estrutura HTML
- [ ] Implementar visualizações

### 3.10 Estilização e Design

#### 3.10.1 CSS Principal

**Arquivo:** `frontend/static/css/main.css`

**Estilos necessários:**
- [ ] Cores do tema (manter paleta similar)
- [ ] Tipografia
- [ ] Layout responsivo
- [ ] Componentes reutilizáveis
- [ ] Animações e transições

**Paleta de cores sugerida:**
```css
:root {
    --primary-color: #6A0DAD;
    --success-color: #2E8B57;
    --danger-color: #C21807;
    --warning-color: #F39C12;
    --info-color: #3498DB;
    --bg-color: #F7F7F9;
    --text-color: #333333;
}
```

#### 3.10.2 Framework CSS (Opcional)

**Opções:**
- **Bootstrap 5** - Framework completo, fácil de usar
- **Tailwind CSS** - Utility-first, mais flexível
- **CSS puro** - Mais controle, mais trabalho

**Recomendação:** Bootstrap 5 para agilizar desenvolvimento

**Tarefas:**
- [ ] Escolher framework (ou CSS puro)
- [ ] Integrar no projeto
- [ ] Criar tema customizado
- [ ] Aplicar em todos os dashboards

### 3.11 JavaScript e Interatividade

#### 3.11.1 Biblioteca de Gráficos

**Plotly.js** (recomendado)
- Compatível com Plotly Python
- Gráficos interativos
- Boa performance

**Alternativa:** Chart.js (mais leve, menos recursos)

**Tarefas:**
- [ ] Incluir Plotly.js no projeto
- [ ] Criar funções utilitárias para gráficos
- [ ] Implementar helpers de renderização

#### 3.11.2 Gerenciamento de Estado

**Estratégia simples:**
- Variáveis globais para estado atual
- Funções para atualizar estado
- Event listeners para mudanças

**Tarefas:**
- [ ] Criar sistema de estado simples
- [ ] Gerenciar período atual
- [ ] Gerenciar dashboard atual
- [ ] Implementar atualização automática

### 3.12 Responsividade

#### 3.12.1 Mobile First

**Breakpoints sugeridos:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Tarefas:**
- [ ] Testar em dispositivos móveis
- [ ] Ajustar layout para telas pequenas
- [ ] Otimizar gráficos para mobile
- [ ] Melhorar navegação mobile

### 3.13 Performance

#### 3.13.1 Otimizações

- [ ] Lazy loading de gráficos
- [ ] Cache de dados (localStorage)
- [ ] Debounce em filtros
- [ ] Compressão de assets
- [ ] Minificação de JS/CSS

**Tarefas:**
- [ ] Implementar cache local
- [ ] Otimizar carregamento inicial
- [ ] Reduzir requisições desnecessárias

## Entregas da Fase 3

- [ ] Template base HTML criado
- [ ] Sistema de navegação funcionando
- [ ] Barra de período implementada
- [ ] Todos os 7 dashboards migrados
- [ ] Todos os gráficos renderizando corretamente
- [ ] Tabelas funcionando
- [ ] Design responsivo implementado
- [ ] Geração de relatórios funcionando
- [ ] Interface visualmente atraente

## Critérios de Aceitação

1. ✅ Todos os dashboards carregam corretamente
2. ✅ Todos os gráficos são interativos e funcionais
3. ✅ Filtro de período atualiza todos os dashboards
4. ✅ Interface é responsiva (mobile, tablet, desktop)
5. ✅ Performance aceitável (< 3s para carregar dashboard)
6. ✅ Design consistente e profissional
7. ✅ Navegação fluida entre dashboards

## Próxima Fase

Após completar a Fase 3, seguir para **[Fase 4: Funcionalidades Avançadas](fase-04-funcionalidades.md)**

