// estoque.js - Dashboard de Estoque

async function initEstoqueDashboard(startDate, endDate) {
    console.log('Carregando Dashboard de Estoque...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/estoque?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar KPIs
            renderInventoryKPIs(dashboardData.kpis);
            
            // Renderizar gráficos
            await renderTopSellingChart(dashboardData.top_selling);
            await renderLeastSellingChart(dashboardData.least_selling);
            await renderStockRuptureChart(dashboardData.low_stock);
            
            // Carregar tabela de dados
            await loadInventoryTable(startDate, endDate);
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard de estoque:', error);
        showNotification('Erro ao carregar dashboard de estoque', 'error');
    }
}

// Renderizar KPIs de estoque
function renderInventoryKPIs(kpis) {
    const kpiContainer = document.getElementById('inventory-kpis');
    
    if (!kpis) {
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
        <div class="kpi-widget info">
            <div class="kpi-label">Produtos Únicos</div>
            <div class="kpi-value">${kpis.unique_products || 0}</div>
        </div>
        
        <div class="kpi-widget success">
            <div class="kpi-label">Valor Total do Estoque</div>
            <div class="kpi-value">${formatCurrency(kpis.total_value)}</div>
            <div class="kpi-change ${getChangeClass(kpis.total_value_change)}">
                ${getChangeIcon(kpis.total_value_change)} ${formatPercent(kpis.total_value_change)}
            </div>
        </div>
        
        <div class="kpi-widget danger">
            <div class="kpi-label">Itens com Estoque Baixo</div>
            <div class="kpi-value">${kpis.low_stock_count || 0}</div>
            <div class="kpi-change ${getChangeClass(kpis.low_stock_count_change)}">
                ${getChangeIcon(kpis.low_stock_count_change)} ${formatPercent(kpis.low_stock_count_change)}
            </div>
        </div>
    `;
}

// Renderizar gráfico de top produtos vendidos
async function renderTopSellingChart(topSellingData) {
    const chartContainer = document.getElementById('chart-top-vendidos');
    
    if (!topSellingData || Object.keys(topSellingData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const products = Object.keys(topSellingData);
    const values = Object.values(topSellingData);
    
    const trace = {
        x: values,
        y: products,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#2ECC71' }
    };
    
    const layout = {
        title: 'Top 10 Produtos por Faturamento',
        xaxis: { title: 'Faturamento Total (R$)' },
        yaxis: { title: 'Produto' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 400,
        margin: { l: 150, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-top-vendidos', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-top-vendidos', 'Top_10_Produtos_Vendidos');
}

// Renderizar gráfico de produtos menos vendidos
async function renderLeastSellingChart(leastSellingData) {
    const chartContainer = document.getElementById('chart-menos-vendidos');
    
    if (!leastSellingData || Object.keys(leastSellingData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const products = Object.keys(leastSellingData);
    const values = Object.values(leastSellingData);
    
    const trace = {
        x: values,
        y: products,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#F39C12' }
    };
    
    const layout = {
        title: '10 Produtos com Menor Faturamento',
        xaxis: { title: 'Faturamento Total (R$)' },
        yaxis: { title: 'Produto' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 400,
        margin: { l: 150, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-menos-vendidos', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-menos-vendidos', 'Produtos_Menos_Vendidos');
}

// Renderizar gráfico de rupturas de estoque
async function renderStockRuptureChart(lowStockData) {
    const chartContainer = document.getElementById('chart-ruptura');
    
    if (!lowStockData || lowStockData.length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhuma ruptura de estoque no período selecionado.</p>';
        return;
    }
    
    // Ordenar por gap (maior para menor)
    const sortedData = [...lowStockData].sort((a, b) => (b.gap || 0) - (a.gap || 0));
    
    const products = sortedData.map(item => item.Produto || 'N/A');
    const gaps = sortedData.map(item => item.gap || 0);
    
    const trace = {
        x: gaps,
        y: products,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#E74C3C' }
    };
    
    const layout = {
        title: 'Maiores Rupturas de Estoque (Gap)',
        xaxis: { title: 'Gap (Quantidade)' },
        yaxis: { title: 'Produto' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 400,
        margin: { l: 150, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-ruptura', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-ruptura', 'Rupturas_Estoque');
}

// Carregar tabela de dados de estoque
async function loadInventoryTable(startDate, endDate) {
    const tableBody = document.getElementById('inventory-table-body');
    
    try {
        const data = await apiRequest(
            `/api/data/estoque?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (data.status === 'success' && data.data && data.data.length > 0) {
            const formatCurrency = (value) => {
                return new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(value || 0);
            };
            
            // Pegar apenas o registro mais recente de cada produto
            const latestRecords = {};
            data.data.forEach(item => {
                const produto = item.Produto || 'N/A';
                if (!latestRecords[produto] || new Date(item.Data_Snapshot) > new Date(latestRecords[produto].Data_Snapshot)) {
                    latestRecords[produto] = item;
                }
            });
            
            const records = Object.values(latestRecords);
            
            tableBody.innerHTML = records.map(item => `
                <tr>
                    <td data-filter="produto">${item.Produto || '-'}</td>
                    <td data-filter="estoque">${item.Quantidade_Estoque || 0}</td>
                    <td data-filter="minimo">${item.Nivel_Minimo_Estoque || 0}</td>
                    <td data-filter="custo">${formatCurrency(item.Preco_Custo)}</td>
                    <td data-filter="venda">${formatCurrency(item.Preco_Venda)}</td>
                    <td data-filter="vendido">${item.Quantidade_Vendida || 0}</td>
                </tr>
            `).join('');
            
            // Adicionar filtros
            addEstoqueFilters();
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum dado disponível para o período selecionado.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao carregar tabela de estoque:', error);
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
    }
}

// Adicionar filtros ao dashboard de estoque
function addEstoqueFilters() {
    const tableCard = document.querySelector('#inventory-table-body')?.closest('.dashboard-card');
    if (!tableCard) return;
    
    if (document.getElementById('filters-estoque')) return;
    
    const table = document.querySelector('#inventory-table-body')?.closest('table');
    if (!table) return;
    
    const produtos = new Set();
    table.querySelectorAll('tbody tr').forEach(row => {
        const produto = row.querySelector('[data-filter="produto"]')?.textContent.trim();
        if (produto) produtos.add(produto);
    });
    
    const filtersHTML = `
        <div class="filters-panel mb-3" id="filters-estoque" data-table-id="table-estoque">
            <div class="filters-header d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">🔍 Filtros</h6>
                <button class="btn btn-sm btn-outline-secondary" onclick="FilterManager.clearFilters('filters-estoque')">
                    Limpar
                </button>
            </div>
            <div class="filters-content d-flex gap-2 flex-wrap">
                <div class="filter-item">
                    <input type="text" class="form-control form-control-sm" data-filter="produto" 
                           placeholder="Buscar produto..." 
                           oninput="applyFilter('estoque')" style="width: 250px;">
                </div>
                <div class="filter-item">
                    <input type="number" class="form-control form-control-sm" data-filter="estoque" 
                           placeholder="Estoque mínimo..." 
                           oninput="applyFilter('estoque')" style="width: 150px;">
                </div>
            </div>
        </div>
    `;
    
    const tableContainer = tableCard.querySelector('.data-table');
    if (tableContainer) {
        tableContainer.insertAdjacentHTML('beforebegin', filtersHTML);
    }
    
    if (table && !table.id) {
        table.id = 'table-estoque';
    }
}

// Exportar função principal
window.initEstoqueDashboard = initEstoqueDashboard;

