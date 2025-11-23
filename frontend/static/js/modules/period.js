// modules/period.js - Gerenciamento de Período

/**
 * Configurar barra de período
 */
function setupPeriodBar() {
    const btnApply = document.getElementById('btn-apply-period');
    const btnReset = document.getElementById('btn-reset-period');
    
    if (btnApply) {
        btnApply.addEventListener('click', async () => {
            const startDate = document.getElementById('start-date')?.value;
            const endDate = document.getElementById('end-date')?.value;
            
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
    }
    
    if (btnReset) {
        btnReset.addEventListener('click', async () => {
            await resetPeriod();
        });
    }
}

/**
 * Carregar range de datas disponível
 */
async function loadDateRange() {
    console.log('Iniciando carregamento do range de datas...');
    
    try {
        const response = await fetch('/api/data/date-range');
        console.log('Resposta da API recebida:', response.status);
        
        const data = await response.json();
        console.log('Dados da API:', data);
        
        if (data.status === 'success' && data.min_date && data.max_date) {
            const startDate = data.min_date;
            const endDate = data.max_date;
            
            console.log('Datas extraídas da API:', { startDate, endDate });
            
            await new Promise(resolve => setTimeout(resolve, 50));
            
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            if (startDateInput) {
                startDateInput.setAttribute('value', startDate);
                startDateInput.value = startDate;
                startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            if (endDateInput) {
                endDateInput.setAttribute('value', endDate);
                endDateInput.value = endDate;
                endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
            
            console.log('Range de datas carregado com sucesso:', { startDate, endDate });
        } else {
            // Fallback: usar último ano
            const endDate = new Date().toISOString().split('T')[0];
            const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
            
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            if (startDateInput) startDateInput.value = startDate;
            if (endDateInput) endDateInput.value = endDate;
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
        }
    } catch (error) {
        console.error('Erro ao carregar range de datas:', error);
        // Fallback em caso de erro
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
        
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        
        if (startDateInput) startDateInput.value = startDate;
        if (endDateInput) endDateInput.value = endDate;
        
        AppState.startDate = startDate;
        AppState.endDate = endDate;
    }
}

/**
 * Aplicar período e recarregar dashboard
 */
async function applyPeriod(startDate, endDate) {
    const loadingIndicator = document.getElementById('period-loading');
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    
    try {
        await loadDashboard(AppState.currentDashboard, startDate, endDate);
        showNotification('Período atualizado com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao aplicar período:', error);
        showNotification('Erro ao atualizar período', 'error');
    } finally {
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * Resetar período
 */
async function resetPeriod() {
    await loadDateRange();
    await loadDashboard(AppState.currentDashboard);
    showNotification('Período resetado', 'info');
}

// Exportar para uso global
window.setupPeriodBar = setupPeriodBar;
window.loadDateRange = loadDateRange;
window.applyPeriod = applyPeriod;
window.resetPeriod = resetPeriod;

