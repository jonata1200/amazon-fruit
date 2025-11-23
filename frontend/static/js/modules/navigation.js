// modules/navigation.js - Sistema de Navegação

/**
 * Configurar navegação do menu
 */
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

/**
 * Navega para um dashboard específico
 */
function navigateToDashboard(dashboardName) {
    // Atualizar menu ativo
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-dashboard') === dashboardName) {
            item.classList.add('active');
        }
    });
    
    // Carregar dashboard
    loadDashboard(dashboardName);
    
    // Feedback visual
    showNotification(`Navegando para: ${getDashboardDisplayName(dashboardName)}`, 'info');
}

// Exportar para uso global
window.setupNavigation = setupNavigation;
window.navigateToDashboard = navigateToDashboard;

