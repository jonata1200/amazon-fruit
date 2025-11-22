// app.js - Sistema de Navegação e Gerenciamento de Estado

// Estado Global da Aplicação
const AppState = {
    currentDashboard: 'geral',
    startDate: null,
    endDate: null,
    isLoading: false
};

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();
});

// Inicializar aplicação
async function initializeApp() {
    // Configurar menu de navegação
    setupNavigation();
    
    // Configurar barra de período
    setupPeriodBar();
    
    // Carregar range de datas disponível
    await loadDateRange();
    
    // Carregar dashboard inicial
    await loadDashboard('geral');
}

// Configurar navegação do menu
function setupNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', async (e) => {
            e.preventDefault();
            const dashboard = item.getAttribute('data-dashboard');
            
            // Atualizar menu ativo
            menuItems.forEach(mi => mi.classList.remove('active'));
            item.classList.add('active');
            
            // Carregar dashboard
            await loadDashboard(dashboard);
        });
    });
}

// Configurar barra de período
function setupPeriodBar() {
    const btnApply = document.getElementById('btn-apply-period');
    const btnReset = document.getElementById('btn-reset-period');
    
    btnApply.addEventListener('click', async () => {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        
        if (!startDate || !endDate) {
            alert('Por favor, selecione ambas as datas.');
            return;
        }
        
        if (new Date(startDate) > new Date(endDate)) {
            alert('A data inicial deve ser anterior à data final.');
            return;
        }
        
        AppState.startDate = startDate;
        AppState.endDate = endDate;
        
        await applyPeriod(startDate, endDate);
    });
    
    btnReset.addEventListener('click', async () => {
        await resetPeriod();
    });
}

// Carregar range de datas disponível
async function loadDateRange() {
    try {
        const response = await fetch('/api/data/date-range');
        const data = await response.json();
        
        if (data.status === 'success' && data.min_date && data.max_date) {
            // Usar o range completo de datas disponível no banco
            const startDate = data.min_date;
            const endDate = data.max_date;
            
            document.getElementById('start-date').value = startDate;
            document.getElementById('end-date').value = endDate;
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
        } else {
            // Fallback: usar último ano se não houver dados
            const endDate = new Date().toISOString().split('T')[0];
            const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
            
            document.getElementById('start-date').value = startDate;
            document.getElementById('end-date').value = endDate;
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
        }
    } catch (error) {
        console.error('Erro ao carregar range de datas:', error);
    }
}

// Aplicar período e recarregar dashboard
async function applyPeriod(startDate, endDate) {
    const loadingIndicator = document.getElementById('period-loading');
    loadingIndicator.style.display = 'block';
    
    try {
        // Recarregar dashboard atual com novo período
        await loadDashboard(AppState.currentDashboard, startDate, endDate);
        
        // Mostrar feedback de sucesso
        showNotification('Período atualizado com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao aplicar período:', error);
        showNotification('Erro ao atualizar período', 'error');
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

// Resetar período
async function resetPeriod() {
    await loadDateRange();
    await loadDashboard(AppState.currentDashboard);
    showNotification('Período resetado', 'info');
}

// Carregar dashboard
async function loadDashboard(dashboardName, startDate = null, endDate = null) {
    AppState.currentDashboard = dashboardName;
    AppState.isLoading = true;
    
    // Atualizar título da página
    updatePageTitle(dashboardName);
    
    // Mostrar loading
    const content = document.getElementById('dashboard-content');
    content.innerHTML = `
        <div class="loading-screen">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p>Carregando dashboard...</p>
        </div>
    `;
    
    // Usar datas do estado se não fornecidas
    const start = startDate || AppState.startDate;
    const end = endDate || AppState.endDate;
    
    try {
        // Carregar conteúdo do dashboard
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

// Carregar conteúdo do dashboard
async function loadDashboardContent(dashboardName, startDate, endDate) {
    const content = document.getElementById('dashboard-content');
    
    // Carregar HTML do dashboard (se existir)
    try {
        const response = await fetch(`/templates/dashboards/${dashboardName}.html`);
        if (response.ok) {
            const html = await response.text();
            content.innerHTML = html;
        } else {
            // Se não encontrar HTML, criar estrutura básica
            content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
        }
    } catch (error) {
        // Se erro, criar estrutura básica
        content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
    }
    
    // Carregar JavaScript específico do dashboard
    await loadDashboardScript(dashboardName, startDate, endDate);
}

// Carregar script do dashboard
async function loadDashboardScript(dashboardName, startDate, endDate) {
    // Remover script anterior se existir
    const oldScript = document.getElementById('dashboard-script');
    if (oldScript) {
        oldScript.remove();
    }
    
    // Criar novo script
    const script = document.createElement('script');
    script.id = 'dashboard-script';
    script.src = `/static/js/dashboards/${dashboardName}.js`;
    script.onload = () => {
        // Mapear nomes de dashboard para nomes de função
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
            window[functionName](startDate, endDate);
        } else {
            console.warn(`Função de inicialização não encontrada para: ${dashboardName}`);
        }
    };
    document.body.appendChild(script);
}

// Atualizar título da página
function updatePageTitle(dashboardName) {
    const titles = {
        'geral': 'Visão Geral do Negócio',
        'financas': 'Finanças',
        'estoque': 'Estoque',
        'publico_alvo': 'Público-Alvo',
        'fornecedores': 'Fornecedores',
        'recursos_humanos': 'Recursos Humanos'
    };
    
    document.getElementById('page-title').textContent = titles[dashboardName] || 'Dashboard';
    
    // Mostrar/ocultar botão de relatório
    const btnReport = document.getElementById('btn-report');
    if (dashboardName === 'geral') {
        btnReport.style.display = 'block';
        btnReport.onclick = () => generateReport(startDate, endDate);
    } else {
        btnReport.style.display = 'none';
    }
}

// Mostrar notificação
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Função auxiliar para fazer requisições à API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição API:', error);
        throw error;
    }
}

// Gerar relatório (placeholder)
async function generateReport(startDate, endDate) {
    showNotification('Funcionalidade de relatório será implementada na Fase 4', 'info');
}

// Exportar funções úteis
window.AppState = AppState;
window.apiRequest = apiRequest;
window.showNotification = showNotification;

