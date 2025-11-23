// modules/alerts.js - Sistema de Alertas

let currentAlerts = [];

/**
 * Carrega alertas do sistema
 */
async function loadAlerts() {
    try {
        const startDate = AppState.startDate;
        const endDate = AppState.endDate;
        
        let url = '/api/alerts/';
        if (startDate && endDate) {
            url += `?start_date=${startDate}&end_date=${endDate}`;
        }
        
        const response = await apiRequest(url);
        
        if (response.status === 'success') {
            currentAlerts = response.alerts || [];
            updateAlertsBadge(currentAlerts.length);
            updateAlertsPanel();
        }
    } catch (error) {
        console.error('Erro ao carregar alertas:', error);
    }
}

/**
 * Atualiza o badge de alertas no botão
 */
function updateAlertsBadge(count) {
    const badge = document.getElementById('alerts-badge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'block';
            badge.classList.add('alerts-badge-pulse');
        } else {
            badge.style.display = 'none';
            badge.classList.remove('alerts-badge-pulse');
        }
    }
}

/**
 * Atualiza o painel de alertas
 */
function updateAlertsPanel() {
    const alertsList = document.getElementById('alerts-list');
    if (!alertsList) return;
    
    if (currentAlerts.length === 0) {
        alertsList.innerHTML = `
            <div class="text-center text-muted p-4">
                <p class="mb-0">✅ Nenhum alerta no momento</p>
            </div>
        `;
        return;
    }
    
    alertsList.innerHTML = currentAlerts.map(alert => {
        const severityClass = `severity-${alert.severity || 'info'}`;
        const icon = alert.severity === 'danger' ? '🔴' : alert.severity === 'warning' ? '🟡' : '🔵';
        
        return `
            <div class="alert-item ${severityClass}" onclick="navigateToAlert('${alert.dashboard || ''}')">
                <div class="alert-item-title">
                    ${icon} ${alert.title || 'Alerta'}
                </div>
                <p class="alert-item-message">${alert.message || ''}</p>
                ${alert.dashboard ? `<div class="alert-item-dashboard">📊 ${getDashboardDisplayName(alert.dashboard)}</div>` : ''}
            </div>
        `;
    }).join('');
}

/**
 * Alterna a exibição do painel de alertas
 */
function toggleAlertsPanel() {
    const panel = document.getElementById('alerts-panel');
    if (panel) {
        const isVisible = panel.style.display !== 'none';
        panel.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            loadAlerts();
        }
    }
}

/**
 * Navega para o dashboard relacionado ao alerta
 */
function navigateToAlert(dashboardName) {
    if (dashboardName) {
        toggleAlertsPanel();
        navigateToDashboard(dashboardName);
    }
}

// Exportar para uso global
window.loadAlerts = loadAlerts;
window.updateAlertsBadge = updateAlertsBadge;
window.updateAlertsPanel = updateAlertsPanel;
window.toggleAlertsPanel = toggleAlertsPanel;
window.navigateToAlert = navigateToAlert;

