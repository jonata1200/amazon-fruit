// recursos_humanos.js - Dashboard de Recursos Humanos

async function initRecursosHumanosDashboard(startDate, endDate) {
    console.log('Carregando Dashboard de Recursos Humanos...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/recursos_humanos`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar gráficos
            await renderHeadcountChart(dashboardData.headcount_by_department);
            await renderCostChart(dashboardData.cost_by_department);
            await renderRoleChart(dashboardData.by_role);
            await renderHiringChart(dashboardData.hiring_over_time);
            
            // Carregar tabela de dados
            await loadHRTable();
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard de RH:', error);
        showNotification('Erro ao carregar dashboard de RH', 'error');
    }
}

// Renderizar gráfico de headcount por departamento
async function renderHeadcountChart(headcountData) {
    const chartContainer = document.getElementById('chart-headcount');
    
    if (!headcountData || Object.keys(headcountData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const departments = Object.keys(headcountData);
    const values = Object.values(headcountData);
    
    const trace = {
        x: values,
        y: departments,
        type: 'bar',
        orientation: 'h',
        marker: { color: ChartColors.primary }
    };
    
    const layout = {
        title: 'Nº de Funcionários por Departamento',
        xaxis: { title: 'Número de Funcionários' },
        yaxis: { title: 'Departamento' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-headcount', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-headcount', 'Headcount_Por_Departamento');
}

// Renderizar gráfico de custo por departamento
async function renderCostChart(costData) {
    const chartContainer = document.getElementById('chart-cost');
    
    if (!costData || Object.keys(costData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const departments = Object.keys(costData);
    const values = Object.values(costData);
    
    const trace = {
        x: values,
        y: departments,
        type: 'bar',
        orientation: 'h',
        marker: { color: ChartColors.info }
    };
    
    const layout = {
        title: 'Custo Mensal por Departamento',
        xaxis: { title: 'Custo Mensal (R$)' },
        yaxis: { title: 'Departamento' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-cost', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-cost', 'Custo_Por_Departamento');
}

// Renderizar gráfico de distribuição por cargo
async function renderRoleChart(roleData) {
    const chartContainer = document.getElementById('chart-role');
    
    if (!roleData || Object.keys(roleData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const roles = Object.keys(roleData);
    const values = Object.values(roleData);
    
    const trace = {
        x: values,
        y: roles,
        type: 'bar',
        orientation: 'h',
        marker: { color: ChartColors.success }
    };
    
    const layout = {
        title: 'Top 10 Cargos na Empresa',
        xaxis: { title: 'Número de Funcionários' },
        yaxis: { title: 'Cargo' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-role', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-role', 'Top_10_Cargos');
}

// Renderizar gráfico de histórico de contratações
async function renderHiringChart(hiringData) {
    const chartContainer = document.getElementById('chart-hiring');
    
    if (!hiringData || Object.keys(hiringData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const periods = Object.keys(hiringData).sort();
    const values = periods.map(period => hiringData[period]);
    
    const trace = {
        x: periods,
        y: values,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: '#E67E22', size: 8 },
        line: { width: 3 }
    };
    
    const layout = {
        title: 'Contratações ao Longo do Tempo',
        xaxis: { title: 'Período' },
        yaxis: { title: 'Número de Contratações' },
        height: 350,
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-hiring', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-hiring', 'Historico_Contratacoes');
}

// Carregar tabela de dados de RH
async function loadHRTable() {
    const tableBody = document.getElementById('hr-table-body');
    
    try {
        const data = await apiRequest(`/api/data/recursos_humanos`);
        
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
                    <td>${item.ID_Funcionario || '-'}</td>
                    <td>${item.Nome || '-'}</td>
                    <td>${item.Cargo || '-'}</td>
                    <td>${item.Departamento || '-'}</td>
                    <td>${formatCurrency(item.Salario)}</td>
                    <td>${formatDate(item.Data_Contratacao)}</td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum dado disponível.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao carregar tabela de RH:', error);
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
    }
}

// Exportar função principal
window.initRecursosHumanosDashboard = initRecursosHumanosDashboard;

