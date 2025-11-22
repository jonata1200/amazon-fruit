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
    console.log('Inicializando aplicação...');
    
    // Configurar menu de navegação
    setupNavigation();
    
    // Configurar barra de período
    setupPeriodBar();
    
    // Garantir que os elementos existem antes de tentar definir valores
    let attempts = 0;
    while (attempts < 10) {
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        
        if (startDateInput && endDateInput) {
            console.log('Elementos encontrados, carregando range de datas...');
            break;
        }
        
        console.log(`Tentativa ${attempts + 1}: elementos ainda não encontrados, aguardando...`);
        await new Promise(resolve => setTimeout(resolve, 100));
        attempts++;
    }
    
    // Carregar range de datas disponível ANTES de carregar o dashboard
    await loadDateRange();
    
    // Aguardar um pouco para garantir que os campos de data foram atualizados
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Forçar atualização dos valores novamente após um delay
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    
    if (AppState.startDate && AppState.endDate) {
        if (startDateInput) {
            startDateInput.value = AppState.startDate;
            startDateInput.setAttribute('value', AppState.startDate);
            // Disparar evento para garantir que o navegador atualize
            startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        if (endDateInput) {
            endDateInput.value = AppState.endDate;
            endDateInput.setAttribute('value', AppState.endDate);
            // Disparar evento para garantir que o navegador atualize
            endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Verificar valores finais
    console.log('Valores finais nos campos:', {
        startDate: startDateInput ? startDateInput.value : 'não encontrado',
        endDate: endDateInput ? endDateInput.value : 'não encontrado',
        appState: { startDate: AppState.startDate, endDate: AppState.endDate }
    });
    
    // Carregar dashboard inicial com as datas corretas
    await loadDashboard('geral', AppState.startDate, AppState.endDate);
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
    console.log('Iniciando carregamento do range de datas...');
    
    try {
        const response = await fetch('/api/data/date-range');
        console.log('Resposta da API recebida:', response.status);
        
        const data = await response.json();
        console.log('Dados da API:', data);
        
        if (data.status === 'success' && data.min_date && data.max_date) {
            // Usar o range completo de datas disponível no banco
            const startDate = data.min_date;
            const endDate = data.max_date;
            
            console.log('Datas extraídas da API:', { startDate, endDate });
            
            // Aguardar um pouco para garantir que o DOM está pronto
            await new Promise(resolve => setTimeout(resolve, 50));
            
            // Atualizar campos de data no DOM
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            console.log('Elementos encontrados:', {
                startDateInput: !!startDateInput,
                endDateInput: !!endDateInput
            });
            
            if (startDateInput) {
                // Definir valor múltiplas vezes para garantir
                startDateInput.setAttribute('value', startDate);
                startDateInput.value = startDate;
                startDateInput.setAttribute('value', startDate);
                
                // Disparar eventos para garantir atualização
                startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Data inicial definida:', startDateInput.value);
                console.log('Atributo value:', startDateInput.getAttribute('value'));
            } else {
                console.error('Elemento start-date não encontrado!');
            }
            
            if (endDateInput) {
                // Definir valor múltiplas vezes para garantir
                endDateInput.setAttribute('value', endDate);
                endDateInput.value = endDate;
                endDateInput.setAttribute('value', endDate);
                
                // Disparar eventos para garantir atualização
                endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Data final definida:', endDateInput.value);
                console.log('Atributo value:', endDateInput.getAttribute('value'));
            } else {
                console.error('Elemento end-date não encontrado!');
            }
            
            // Atualizar estado da aplicação
            AppState.startDate = startDate;
            AppState.endDate = endDate;
            
            console.log('Range de datas carregado com sucesso:', { startDate, endDate });
            console.log('AppState atualizado:', AppState);
        } else {
            console.warn('API não retornou dados válidos:', data);
            // Fallback: usar último ano se não houver dados
            const endDate = new Date().toISOString().split('T')[0];
            const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
            
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            if (startDateInput) {
                startDateInput.value = startDate;
            }
            if (endDateInput) {
                endDateInput.value = endDate;
            }
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
            
            console.warn('Range de datas não encontrado, usando fallback:', { startDate, endDate });
        }
    } catch (error) {
        console.error('Erro ao carregar range de datas:', error);
        // Em caso de erro, usar fallback
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
        
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        
        if (startDateInput) {
            startDateInput.value = startDate;
        }
        if (endDateInput) {
            endDateInput.value = endDate;
        }
        
        AppState.startDate = startDate;
        AppState.endDate = endDate;
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

