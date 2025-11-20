// fornecedores.js - Dashboard de Fornecedores

async function initFornecedoresDashboard(startDate, endDate) {
    console.log('Carregando Dashboard de Fornecedores...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/fornecedores`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar gráficos
            await renderTopSuppliersChart(dashboardData.top_suppliers);
            await renderBottomSuppliersChart(dashboardData.bottom_suppliers);
            await renderSuppliersStateChart(dashboardData.by_state);
            
            // Carregar tabela de dados
            await loadSuppliersTable();
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard de fornecedores:', error);
        showNotification('Erro ao carregar dashboard de fornecedores', 'error');
    }
}

// Renderizar gráfico de top fornecedores
async function renderTopSuppliersChart(topSuppliersData) {
    const chartContainer = document.getElementById('chart-top-suppliers');
    
    if (!topSuppliersData || topSuppliersData.length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    // Ordenar por avaliação (menor para maior para exibir de baixo para cima)
    const sorted = [...topSuppliersData].sort((a, b) => (a.Avaliacao || 0) - (b.Avaliacao || 0));
    
    const names = sorted.map(s => s.Nome_Fornecedor || 'N/A');
    const ratings = sorted.map(s => s.Avaliacao || 0);
    
    const trace = {
        x: ratings,
        y: names,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#2ECC71' }
    };
    
    const layout = {
        title: 'Top 5 Melhores Fornecedores',
        xaxis: { 
            title: 'Avaliação',
            range: [0, 5]
        },
        yaxis: { title: 'Fornecedor' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 300,
        margin: { l: 150, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-top-suppliers', [trace], layout, {responsive: true});
}

// Renderizar gráfico de bottom fornecedores
async function renderBottomSuppliersChart(bottomSuppliersData) {
    const chartContainer = document.getElementById('chart-bottom-suppliers');
    
    if (!bottomSuppliersData || bottomSuppliersData.length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    // Ordenar por avaliação (maior para menor para exibir de baixo para cima)
    const sorted = [...bottomSuppliersData].sort((a, b) => (b.Avaliacao || 0) - (a.Avaliacao || 0));
    
    const names = sorted.map(s => s.Nome_Fornecedor || 'N/A');
    const ratings = sorted.map(s => s.Avaliacao || 0);
    
    const trace = {
        x: ratings,
        y: names,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#E74C3C' }
    };
    
    const layout = {
        title: 'Top 5 Piores Fornecedores',
        xaxis: { 
            title: 'Avaliação',
            range: [0, 5]
        },
        yaxis: { title: 'Fornecedor' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 300,
        margin: { l: 150, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-bottom-suppliers', [trace], layout, {responsive: true});
}

// Renderizar gráfico de distribuição por estado
async function renderSuppliersStateChart(stateData) {
    const chartContainer = document.getElementById('chart-suppliers-state');
    
    if (!stateData || Object.keys(stateData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const states = Object.keys(stateData);
    const values = Object.values(stateData);
    
    const trace = {
        x: values,
        y: states,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#3498DB' }
    };
    
    const layout = {
        title: 'Distribuição de Fornecedores por Estado',
        xaxis: { title: 'Número de Fornecedores' },
        yaxis: { title: 'Estado' },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 400,
        margin: { l: 100, r: 20, t: 50, b: 50 }
    };
    
    Plotly.newPlot('chart-suppliers-state', [trace], layout, {responsive: true});
}

// Carregar tabela de dados de fornecedores
async function loadSuppliersTable() {
    const tableBody = document.getElementById('suppliers-table-body');
    
    try {
        const data = await apiRequest(`/api/data/fornecedores`);
        
        if (data.status === 'success' && data.data && data.data.length > 0) {
            tableBody.innerHTML = data.data.map(item => `
                <tr>
                    <td>${item.ID_Fornecedor || '-'}</td>
                    <td>${item.Nome_Fornecedor || '-'}</td>
                    <td>
                        <span class="badge ${(item.Avaliacao || 0) >= 4 ? 'bg-success' : (item.Avaliacao || 0) >= 3 ? 'bg-warning' : 'bg-danger'}">
                            ${item.Avaliacao ? item.Avaliacao.toFixed(1) : 'N/A'}
                        </span>
                    </td>
                    <td>${item.Cidade || '-'}</td>
                    <td>${item.Estado || '-'}</td>
                    <td>${item.Produtos_Fornecidos || '-'}</td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum dado disponível.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao carregar tabela de fornecedores:', error);
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
    }
}

// Exportar função principal
window.initFornecedoresDashboard = initFornecedoresDashboard;

