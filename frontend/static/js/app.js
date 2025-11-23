// app.js - Arquivo Principal
// Inicializa a aplicação após todos os módulos serem carregados

// ============================================================================
// INICIALIZAÇÃO DA APLICAÇÃO
// ============================================================================

// Aguardar DOM estar pronto
document.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();
});

/**
 * Inicializar aplicação
 */
async function initializeApp() {
    console.log('Inicializando aplicação...');
    
    // Verificar se todos os módulos necessários estão disponíveis
    if (typeof AppState === 'undefined' || typeof CacheManager === 'undefined') {
        console.error('Módulos core não carregados. Verifique se os scripts foram carregados na ordem correta.');
        return;
    }
    
    // Carregar preferência de tema
    if (typeof loadThemePreference === 'function') {
        loadThemePreference();
    }
    
    // Configurar alternância de tema
    if (typeof setupThemeToggle === 'function') {
        setupThemeToggle();
    }
    
    // Configurar menu de navegação
    if (typeof setupNavigation === 'function') {
        setupNavigation();
    }
    
    // Configurar barra de período
    if (typeof setupPeriodBar === 'function') {
        setupPeriodBar();
    }
    
    // Configurar atalhos de teclado
    if (typeof setupKeyboardShortcuts === 'function') {
        setupKeyboardShortcuts();
    }
    
    // Configurar busca global
    if (typeof setupGlobalSearch === 'function') {
        setupGlobalSearch();
    }
    
    // Carregar alertas periodicamente
    if (typeof loadAlerts === 'function') {
        loadAlerts();
        setInterval(loadAlerts, 60000); // Atualizar a cada minuto
    }
    
    // Limpar cache antigo ao iniciar
    if (typeof CacheManager !== 'undefined') {
        CacheManager.clearOld();
    }
    
    // Configurar sidebar para mobile
    if (typeof setupMobileSidebar === 'function') {
        setupMobileSidebar();
    }
    
    // Aguardar elementos do DOM estarem prontos
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
    if (typeof loadDateRange === 'function') {
        await loadDateRange();
    }
    
    // Aguardar um pouco para garantir que os campos de data foram atualizados
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Forçar atualização dos valores novamente após um delay
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    
    if (AppState && AppState.startDate && AppState.endDate) {
        if (startDateInput) {
            startDateInput.value = AppState.startDate;
            startDateInput.setAttribute('value', AppState.startDate);
            startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        if (endDateInput) {
            endDateInput.value = AppState.endDate;
            endDateInput.setAttribute('value', AppState.endDate);
            endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Verificar valores finais
    console.log('Valores finais nos campos:', {
        startDate: startDateInput ? startDateInput.value : 'não encontrado',
        endDate: endDateInput ? endDateInput.value : 'não encontrado',
        appState: AppState ? { startDate: AppState.startDate, endDate: AppState.endDate } : 'não disponível'
    });
    
    // Carregar dashboard inicial com as datas corretas
    if (typeof loadDashboard === 'function' && AppState) {
        await loadDashboard('geral', AppState.startDate, AppState.endDate);
    }
}
