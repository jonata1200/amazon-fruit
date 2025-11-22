// financas.js - Dashboard de Finanças

async function initFinancasDashboard(startDate, endDate) {
    console.log('Carregando Dashboard de Finanças...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/financas?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar KPIs
            renderFinancialKPIs(dashboardData.financial_summary);
            
            // Renderizar gráficos
            await renderEvolutionChart(dashboardData.evolution_chart);
            await renderTopExpensesChart(dashboardData.top_expenses);
            await renderTopRevenuesChart(dashboardData.top_revenues);
            
            // Carregar tabela de dados
            await loadFinancialTable(startDate, endDate);
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard de finanças:', error);
        showNotification('Erro ao carregar dashboard de finanças', 'error');
    }
}

// Renderizar KPIs financeiros
function renderFinancialKPIs(summary) {
    const kpiContainer = document.getElementById('financial-kpis');
    
    if (!summary) {
        kpiContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value || 0);
    };
    
    const formatPercent = (value) => {
        if (value === null || value === undefined) return 'N/A';
        const sign = value >= 0 ? '+' : '';
        return `${sign}${(value * 100).toFixed(2)}%`;
    };
    
    const getChangeClass = (value) => {
        if (value === null || value === undefined) return 'neutral';
        return value >= 0 ? 'positive' : 'negative';
    };
    
    const getChangeIcon = (value) => {
        if (value === null || value === undefined) return '➡️';
        return value >= 0 ? '📈' : '📉';
    };
    
    kpiContainer.innerHTML = `
        <div class="kpi-widget success">
            <div class="kpi-label">Receita Total</div>
            <div class="kpi-value">${formatCurrency(summary.receita)}</div>
            <div class="kpi-change ${getChangeClass(summary.receita_change)}">
                ${getChangeIcon(summary.receita_change)} ${formatPercent(summary.receita_change)}
            </div>
        </div>
        
        <div class="kpi-widget danger">
            <div class="kpi-label">Despesa Total</div>
            <div class="kpi-value">${formatCurrency(summary.despesa)}</div>
            <div class="kpi-change ${getChangeClass(summary.despesa_change)}">
                ${getChangeIcon(summary.despesa_change)} ${formatPercent(summary.despesa_change)}
            </div>
        </div>
        
        <div class="kpi-widget ${summary.lucro >= 0 ? 'success' : 'danger'}">
            <div class="kpi-label">Lucro Líquido</div>
            <div class="kpi-value">${formatCurrency(summary.lucro)}</div>
            <div class="kpi-change ${getChangeClass(summary.lucro_change)}">
                ${getChangeIcon(summary.lucro_change)} ${formatPercent(summary.lucro_change)}
            </div>
        </div>
    `;
}

// Renderizar gráfico de evolução financeira
async function renderEvolutionChart(evolutionData) {
    const chartContainer = document.getElementById('chart-evolucao-financeira');
    
    if (!evolutionData || !evolutionData.months || evolutionData.months.length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível para o período selecionado.</p>';
        return;
    }
    
    // Criar gráfico com subplot (barras + linha) usando cores consistentes
    const trace1 = {
        x: evolutionData.months,
        y: evolutionData.receita,
        name: 'Receita',
        type: 'bar',
        marker: { color: ChartColors.receita },
        yaxis: 'y'
    };
    
    const trace2 = {
        x: evolutionData.months,
        y: evolutionData.despesa,
        name: 'Despesa',
        type: 'bar',
        marker: { color: ChartColors.despesa },
        yaxis: 'y'
    };
    
    const trace3 = {
        x: evolutionData.months,
        y: evolutionData.lucro,
        name: 'Lucro',
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: ChartColors.lucro, size: 8 },
        line: { width: 3 },
        yaxis: 'y2'
    };
    
    const layout = {
        title: 'Evolução Financeira Mensal',
        xaxis: { title: 'Mês' },
        yaxis: {
            title: 'Receita/Despesa (R$)',
            side: 'left'
        },
        yaxis2: {
            title: 'Lucro (R$)',
            overlaying: 'y',
            side: 'right'
        },
        barmode: 'group',
        hovermode: 'x unified',
        height: 400,
        legend: {
            x: 0.5,
            y: -0.2,
            xanchor: 'center',
            orientation: 'h'
        },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-evolucao-financeira', [trace1, trace2, trace3], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-evolucao-financeira', 'Evolucao_Financeira_Mensal');
}

// Renderizar gráfico de top despesas
async function renderTopExpensesChart(expensesData) {
    const chartContainer = document.getElementById('chart-top-despesas');
    
    if (!expensesData || Object.keys(expensesData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const categories = Object.keys(expensesData);
    const values = Object.values(expensesData);
    
    const trace = {
        x: values,
        y: categories,
        type: 'bar',
        orientation: 'h',
        marker: { color: ChartColors.despesa }
    };
    
    const layout = {
        title: 'Top 5 Despesas por Categoria',
        xaxis: { title: 'Valor (R$)' },
        yaxis: { title: 'Categoria' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-top-despesas', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-top-despesas', 'Top_5_Despesas');
}

// Renderizar gráfico de top receitas
async function renderTopRevenuesChart(revenuesData) {
    const chartContainer = document.getElementById('chart-top-receitas');
    
    if (!revenuesData || Object.keys(revenuesData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const categories = Object.keys(revenuesData);
    const values = Object.values(revenuesData);
    
    const trace = {
        x: values,
        y: categories,
        type: 'bar',
        orientation: 'h',
        marker: { color: ChartColors.receita }
    };
    
    const layout = {
        title: 'Top 5 Receitas por Categoria',
        xaxis: { title: 'Valor (R$)' },
        yaxis: { title: 'Categoria' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-top-receitas', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-top-receitas', 'Top_5_Receitas');
}

// Carregar tabela de dados financeiros
async function loadFinancialTable(startDate, endDate) {
    const tableBody = document.getElementById('financial-table-body');
    
    try {
        const data = await apiRequest(
            `/api/data/financas?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (data.status === 'success' && data.data && data.data.length > 0) {
            const formatCurrency = (value) => {
                return new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(value || 0);
            };
            
            const formatDate = (dateStr) => {
                if (!dateStr) return '-';
                const date = new Date(dateStr);
                return date.toLocaleDateString('pt-BR');
            };
            
            tableBody.innerHTML = data.data.map(item => `
                <tr>
                    <td data-filter="data">${formatDate(item.Data)}</td>
                    <td data-filter="tipo"><span class="badge ${item.Tipo === 'Receita' ? 'bg-success' : 'bg-danger'}">${item.Tipo || '-'}</span></td>
                    <td data-filter="categoria">${item.Categoria || '-'}</td>
                    <td data-filter="valor">${formatCurrency(item.Valor)}</td>
                    <td data-filter="descricao">${item.Descricao || '-'}</td>
                </tr>
            `).join('');
            
            // Adicionar filtros se ainda não existirem
            addFinancialFilters();
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum dado disponível para o período selecionado.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao carregar tabela financeira:', error);
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
    }
}

// Adicionar filtros ao dashboard de finanças
function addFinancialFilters() {
    const tableCard = document.querySelector('#financial-table-body')?.closest('.dashboard-card');
    if (!tableCard) return;
    
    // Verificar se já existe painel de filtros
    if (document.getElementById('filters-financas')) return;
    
    // Obter categorias e tipos únicos para os selects
    const table = document.querySelector('#financial-table-body')?.closest('table');
    if (!table) return;
    
    const categorias = new Set();
    const tipos = new Set();
    
    table.querySelectorAll('tbody tr').forEach(row => {
        const categoria = row.querySelector('[data-filter="categoria"]')?.textContent.trim();
        const tipo = row.querySelector('[data-filter="tipo"]')?.textContent.trim();
        if (categoria) categorias.add(categoria);
        if (tipo) tipos.add(tipo);
    });
    
    const filtersHTML = `
        <div class="filters-panel mb-3" id="filters-financas" data-table-id="table-financas">
            <div class="filters-header d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">🔍 Filtros</h6>
                <button class="btn btn-sm btn-outline-secondary" onclick="FilterManager.clearFilters('filters-financas')">
                    Limpar
                </button>
            </div>
            <div class="filters-content d-flex gap-2 flex-wrap">
                <div class="filter-item">
                    <select class="form-control form-control-sm" data-filter="tipo" onchange="applyFilter('financas')" style="width: 150px;">
                        <option value="">Todos os Tipos</option>
                        ${Array.from(tipos).map(t => `<option value="${t}">${t}</option>`).join('')}
                    </select>
                </div>
                <div class="filter-item">
                    <select class="form-control form-control-sm" data-filter="categoria" onchange="applyFilter('financas')" style="width: 200px;">
                        <option value="">Todas as Categorias</option>
                        ${Array.from(categorias).sort().map(c => `<option value="${c}">${c}</option>`).join('')}
                    </select>
                </div>
                <div class="filter-item">
                    <input type="text" class="form-control form-control-sm" data-filter="descricao" 
                           placeholder="Buscar na descrição..." 
                           oninput="applyFilter('financas')" style="width: 250px;">
                </div>
            </div>
        </div>
    `;
    
    const tableContainer = tableCard.querySelector('.data-table');
    if (tableContainer) {
        tableContainer.insertAdjacentHTML('beforebegin', filtersHTML);
    }
    
    // Adicionar ID à tabela
    if (table && !table.id) {
        table.id = 'table-financas';
    }
}

// Exportar função principal
window.initFinancasDashboard = initFinancasDashboard;

