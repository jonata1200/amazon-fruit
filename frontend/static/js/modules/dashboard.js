// modules/dashboard.js - Carregamento de Dashboards

/**
 * Carregar dashboard
 */
async function loadDashboard(dashboardName, startDate = null, endDate = null) {
    AppState.currentDashboard = dashboardName;
    AppState.isLoading = true;
    
    updatePageTitle(dashboardName);
    
    const content = document.getElementById('dashboard-content');
    if (!content) {
        console.error('Elemento dashboard-content não encontrado');
        return;
    }
    
    content.innerHTML = `
        <div class="loading-screen">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p>Carregando dashboard...</p>
        </div>
    `;
    
    const start = startDate || AppState.startDate;
    const end = endDate || AppState.endDate;
    
    try {
        await loadDashboardContent(dashboardName, start, end);
    } catch (error) {
        console.error(`Erro ao carregar dashboard ${dashboardName}:`, error);
        content.innerHTML = `
            <div class="alert alert-danger">
                <h4>Erro ao carregar dashboard</h4>
                <p>${error.message}</p>
            </div>
        `;
    } finally {
        AppState.isLoading = false;
    }
}

/**
 * Carregar conteúdo do dashboard
 */
async function loadDashboardContent(dashboardName, startDate, endDate) {
    const content = document.getElementById('dashboard-content');
    if (!content) return;
    
    showSkeletonLoading(content);
    
    try {
        const response = await fetch(`/templates/dashboards/${dashboardName}.html`);
        if (response.ok) {
            const html = await response.text();
            content.innerHTML = html;
        } else {
            content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
        }
    } catch (error) {
        content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
    }
    
    await loadDashboardScript(dashboardName, startDate, endDate);
}

/**
 * Mostra skeleton loading no conteúdo
 */
function showSkeletonLoading(container) {
    container.innerHTML = `
        <div class="dashboard-card skeleton-card">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text" style="width: 80%;"></div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="dashboard-card skeleton-card">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-chart"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="dashboard-card skeleton-card">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-chart"></div>
                </div>
            </div>
        </div>
        <div class="dashboard-card skeleton-card">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text" style="width: 60%;"></div>
        </div>
    `;
}

/**
 * Carregar script do dashboard
 */
async function loadDashboardScript(dashboardName, startDate, endDate) {
    const oldScript = document.getElementById('dashboard-script');
    if (oldScript) {
        oldScript.remove();
    }
    
    const script = document.createElement('script');
    script.id = 'dashboard-script';
    script.src = `/static/js/dashboards/${dashboardName}.js`;
    script.onload = () => {
        const functionMap = {
            'geral': 'initGeralDashboard',
            'financas': 'initFinancasDashboard',
            'estoque': 'initEstoqueDashboard',
            'publico_alvo': 'initPublicoAlvoDashboard',
            'fornecedores': 'initFornecedoresDashboard',
            'recursos_humanos': 'initRecursosHumanosDashboard'
        };
        
        const functionName = functionMap[dashboardName];
        if (functionName && window[functionName]) {
            // Garantir que as datas sejam válidas
            const finalStartDate = startDate || AppState?.startDate;
            const finalEndDate = endDate || AppState?.endDate;
            
            if (!finalStartDate || !finalEndDate) {
                console.warn(`Datas não disponíveis para ${dashboardName}, aguardando...`);
                setTimeout(() => {
                    const retryStartDate = AppState?.startDate;
                    const retryEndDate = AppState?.endDate;
                    if (retryStartDate && retryEndDate && window[functionName]) {
                        window[functionName](retryStartDate, retryEndDate);
                    } else {
                        console.error(`Não foi possível carregar ${dashboardName}: datas não disponíveis`);
                    }
                }, 500);
            } else {
                window[functionName](finalStartDate, finalEndDate);
            }
        } else {
            console.warn(`Função de inicialização não encontrada para: ${dashboardName}`);
        }
    };
    document.body.appendChild(script);
}

/**
 * Atualizar título da página
 */
function updatePageTitle(dashboardName) {
    const titles = {
        'geral': 'Visão Geral do Negócio',
        'financas': 'Finanças',
        'estoque': 'Estoque',
        'publico_alvo': 'Público-Alvo',
        'fornecedores': 'Fornecedores',
        'recursos_humanos': 'Recursos Humanos'
    };
    
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
        pageTitle.textContent = titles[dashboardName] || 'Dashboard';
    }
    
    const btnReport = document.getElementById('btn-report');
    if (btnReport) {
        if (dashboardName === 'geral') {
            btnReport.style.display = 'block';
            btnReport.onclick = () => generateReport(AppState.startDate, AppState.endDate);
        } else {
            btnReport.style.display = 'none';
        }
    }
}

/**
 * Gerar relatório (placeholder)
 */
async function generateReport(startDate, endDate) {
    showNotification('Funcionalidade de relatório será implementada na Fase 4', 'info');
}

// Exportar para uso global
window.loadDashboard = loadDashboard;
window.loadDashboardContent = loadDashboardContent;
window.showSkeletonLoading = showSkeletonLoading;
window.updatePageTitle = updatePageTitle;
window.generateReport = generateReport;

