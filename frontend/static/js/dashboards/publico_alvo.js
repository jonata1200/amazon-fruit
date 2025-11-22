// publico_alvo.js - Dashboard de Público-Alvo

async function initPublicoAlvoDashboard(startDate, endDate) {
    console.log('Carregando Dashboard de Público-Alvo...', { startDate, endDate });
    
    try {
        // Carregar dados do dashboard
        const dashboardData = await apiRequest(
            `/api/dashboard/publico_alvo?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (dashboardData.status === 'success') {
            // Renderizar gráficos
            await renderLocationChart(dashboardData.by_location);
            await renderGenderChart(dashboardData.by_gender);
            await renderChannelChart(dashboardData.by_channel);
            
            // Carregar tabela de dados
            await loadPublicTable(startDate, endDate);
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard de público-alvo:', error);
        showNotification('Erro ao carregar dashboard de público-alvo', 'error');
    }
}

// Renderizar gráfico de localização
async function renderLocationChart(locationData) {
    const chartContainer = document.getElementById('chart-location');
    
    if (!locationData || Object.keys(locationData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const cities = Object.keys(locationData);
    const values = Object.values(locationData);
    
    const trace = {
        x: values,
        y: cities,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#6A0DAD' }
    };
    
    const layout = {
        title: 'Top 10 Clientes por Localização',
        xaxis: { title: 'Número de Clientes' },
        yaxis: { title: 'Cidade' },
        height: 400,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-location', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-location', 'Clientes_Por_Localizacao');
}

// Renderizar gráfico de gênero (pizza)
async function renderGenderChart(genderData) {
    const chartContainer = document.getElementById('chart-gender');
    
    if (!genderData || Object.keys(genderData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const labels = Object.keys(genderData);
    const values = Object.values(genderData);
    
    const colors = labels.map(label => getGenderColor(label));
    
    const trace = {
        labels: labels,
        values: values,
        type: 'pie',
        marker: {
            colors: colors
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    };
    
    const layout = {
        title: 'Distribuição por Gênero',
        height: 400,
        showlegend: true,
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-gender', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-gender', 'Distribuicao_Por_Genero');
}

// Renderizar gráfico de canal
async function renderChannelChart(channelData) {
    const chartContainer = document.getElementById('chart-channel');
    
    if (!channelData || Object.keys(channelData).length === 0) {
        chartContainer.innerHTML = '<p class="text-muted">Nenhum dado disponível.</p>';
        return;
    }
    
    const channels = Object.keys(channelData);
    const values = Object.values(channelData);
    
    const trace = {
        x: values,
        y: channels,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#FFA500' }
    };
    
    const layout = {
        title: 'Contagem de Clientes por Canal de Venda',
        xaxis: { title: 'Número de Clientes' },
        yaxis: { title: 'Canal' },
        height: 350,
        margin: { l: 150, r: 20, t: 50, b: 50 },
        ...getPlotlyTheme()
    };
    
    Plotly.newPlot('chart-channel', [trace], layout, {responsive: true});
    
    // Adicionar botões de exportação
    addChartExportButtons('chart-channel', 'Clientes_Por_Canal');
}

// Carregar tabela de dados de público-alvo
async function loadPublicTable(startDate, endDate) {
    const tableBody = document.getElementById('public-table-body');
    
    try {
        const data = await apiRequest(
            `/api/data/publico_alvo?start_date=${startDate}&end_date=${endDate}`
        );
        
        if (data.status === 'success' && data.data && data.data.length > 0) {
            const formatCurrency = (value) => {
                return new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(value || 0);
            };
            
            tableBody.innerHTML = data.data.map(item => `
                <tr>
                    <td>${item.ID_Cliente || '-'}</td>
                    <td>${item.Genero || '-'}</td>
                    <td>${item.Idade || '-'}</td>
                    <td>${item.Cidade || '-'}</td>
                    <td>${item.Canal_de_venda || '-'}</td>
                    <td>${formatCurrency(item.Gasto_Medio || item.Ticket_Medio)}</td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum dado disponível para o período selecionado.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao carregar tabela de público-alvo:', error);
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados.</td></tr>';
    }
}

// Exportar função principal
window.initPublicoAlvoDashboard = initPublicoAlvoDashboard;

