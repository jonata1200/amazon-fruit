// core/state.js - Estado Global da Aplicação

/**
 * Estado Global da Aplicação
 */
const AppState = {
    currentDashboard: 'geral',
    startDate: null,
    endDate: null,
    isLoading: false
};

// Exportar para uso global
window.AppState = AppState;

