// modules/export.js - Exportação de Dados e Gráficos

/**
 * Exporta dados de uma tabela para Excel ou CSV
 */
async function exportTable(tableName, format = 'xlsx', startDate = null, endDate = null) {
    try {
        showNotification('Preparando exportação...', 'info');
        
        let url = `/api/export/${tableName}?format=${format}`;
        if (startDate && endDate) {
            url += `&start_date=${startDate}&end_date=${endDate}`;
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao exportar dados');
        }
        
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `${tableName}_${new Date().toISOString().split('T')[0]}.${format}`;
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
        
        showNotification(`Dados exportados com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar tabela:', error);
        showNotification(`Erro ao exportar: ${error.message}`, 'error');
    }
}

/**
 * Exporta todos os dados de um dashboard
 */
async function exportDashboard(dashboardName, format = 'xlsx', startDate = null, endDate = null) {
    try {
        showNotification('Preparando exportação do dashboard...', 'info');
        
        let url = `/api/export/dashboard/${dashboardName}?format=${format}`;
        if (startDate && endDate) {
            url += `&start_date=${startDate}&end_date=${endDate}`;
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao exportar dashboard');
        }
        
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `dashboard_${dashboardName}_${new Date().toISOString().split('T')[0]}.${format}`;
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
        
        showNotification(`Dashboard exportado com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar dashboard:', error);
        showNotification(`Erro ao exportar: ${error.message}`, 'error');
    }
}

/**
 * Exporta um gráfico Plotly para PNG, SVG ou PDF
 */
async function exportChart(chartId, format = 'png', filename = null) {
    try {
        const chartElement = document.getElementById(chartId);
        
        if (!chartElement) {
            throw new Error(`Gráfico com ID '${chartId}' não encontrado`);
        }
        
        const chartData = chartElement.data;
        if (!chartData || chartData.length === 0) {
            showNotification('Gráfico ainda não foi carregado', 'warning');
            return;
        }
        
        showNotification(`Exportando gráfico como ${format.toUpperCase()}...`, 'info');
        
        if (!filename) {
            const timestamp = new Date().toISOString().split('T')[0];
            filename = `grafico_${chartId}_${timestamp}.${format}`;
        }
        
        const config = {
            format: format,
            width: chartElement.offsetWidth || 800,
            height: chartElement.offsetHeight || 600,
            filename: filename
        };
        
        await Plotly.downloadImage(chartElement, config);
        
        showNotification(`Gráfico exportado com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar gráfico:', error);
        showNotification(`Erro ao exportar gráfico: ${error.message}`, 'error');
    }
}

/**
 * Adiciona botões de exportação a um gráfico
 */
function addChartExportButtons(chartId, chartTitle = null) {
    const chartContainer = document.getElementById(chartId);
    
    if (!chartContainer) {
        console.warn(`Container do gráfico '${chartId}' não encontrado`);
        return;
    }
    
    let buttonContainer = chartContainer.parentElement.querySelector('.chart-export-buttons');
    
    if (!buttonContainer) {
        buttonContainer = document.createElement('div');
        buttonContainer.className = 'chart-export-buttons mb-2';
        buttonContainer.style.textAlign = 'right';
        chartContainer.parentElement.insertBefore(buttonContainer, chartContainer);
    }
    
    buttonContainer.innerHTML = '';
    
    const formats = [
        { format: 'png', label: 'PNG', icon: '🖼️' },
        { format: 'svg', label: 'SVG', icon: '📐' },
        { format: 'pdf', label: 'PDF', icon: '📄' }
    ];
    
    formats.forEach(({ format, label, icon }) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-sm btn-outline-secondary me-1';
        button.title = `Exportar como ${label}`;
        button.innerHTML = `${icon} ${label}`;
        button.onclick = () => {
            const filename = chartTitle 
                ? `${chartTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_${new Date().toISOString().split('T')[0]}.${format}`
                : null;
            exportChart(chartId, format, filename);
        };
        buttonContainer.appendChild(button);
    });
}

/**
 * Exporta o dashboard atual
 */
function exportCurrentDashboard() {
    const dashboard = AppState.currentDashboard;
    const startDate = AppState.startDate;
    const endDate = AppState.endDate;
    
    if (dashboard) {
        exportDashboard(dashboard, 'xlsx', startDate, endDate);
        showNotification('Exportando dashboard...', 'info');
    } else {
        showNotification('Nenhum dashboard selecionado', 'warning');
    }
}

// Exportar para uso global
window.exportTable = exportTable;
window.exportDashboard = exportDashboard;
window.exportChart = exportChart;
window.addChartExportButtons = addChartExportButtons;
window.exportCurrentDashboard = exportCurrentDashboard;

