// geral.js - Dashboard Geral

async function initGeralDashboard(startDate, endDate) {
    console.log('Carregando Dashboard Geral...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/geral?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar gráfico de evolução
            await renderEvolutionChart(dashboardData.evolution_chart);
            
            // Renderizar KPIs
            renderFinancialKPIs(dashboardData.financial_summary);
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard geral:', error);
        showNotification('Erro ao carregar dashboard geral', 'error');
    }
}

// Renderizar gráfico de evolução
async function renderEvolutionChart(evolutionData) {
    const chartContainer = document.getElementById('chart-evolucao');
    
    if (!evolutionData || !evolutionData.months || evolutionData.months.length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível para o período selecionado.</p>';
        return;
    }
    
    // Preparar dados para Plotly com cores consistentes
    const trace1 = {
        x: evolutionData.months,
        y: evolutionData.receita,
        name: 'Faturamento (Receita)',
        type: 'bar',
        marker: { color: ChartColors.receita },
        offsetgroup: 1
    };
    
    // Criar cores dinâmicas para lucro (vermelho se negativo, azul se positivo)
    const profitColors = evolutionData.lucro.map(val => 
        val < 0 ? ChartColors.lucroNegativo : ChartColors.lucro
    );
    
    const trace2 = {
        x: evolutionData.months,
        y: evolutionData.lucro,
        name: 'Lucro Líquido',
        type: 'bar',
        marker: { color: profitColors },
        offsetgroup: 2
    };
    
    // Criar layout base primeiro
    const baseLayout = {
        title: 'Evolução Mensal: Faturamento vs. Lucro',
        xaxis: { title: 'Mês' },
        yaxis: { title: 'Valor (R$)' },
        barmode: 'group',
        hovermode: 'x unified',
        height: 400
    };
    
    // Aplicar tema Plotly
    const layout = getPlotlyTheme(baseLayout);
    
    // Garantir que o elemento existe antes de plotar
    const chartElement = document.getElementById('chart-evolucao');
    if (!chartElement) {
        console.error('Elemento chart-evolucao não encontrado');
        return;
    }
    
    try {
        Plotly.newPlot('chart-evolucao', [trace1, trace2], layout, {responsive: true});
    } catch (error) {
        console.error('Erro ao renderizar gráfico:', error);
        chartElement.innerHTML = '<p class="text-danger">Erro ao renderizar gráfico. Por favor, recarregue a página.</p>';
    }
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-evolucao', 'Evolucao_Mensal_Faturamento_Lucro');
}

// Renderizar KPIs financeiros
function renderFinancialKPIs(summary) {
    const kpiContainer = document.getElementById('financial-summary');
    
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

// Exportar função principal
window.initGeralDashboard = initGeralDashboard;

