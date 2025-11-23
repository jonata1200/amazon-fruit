// modules/comparison.js - Comparação de Períodos

let compareMode = false;

/**
 * Alterna o modo de comparação
 */
function toggleCompareMode() {
    compareMode = !compareMode;
    const comparePanel = document.getElementById('compare-periods');
    const compareButton = document.getElementById('btn-compare-mode');
    
    if (comparePanel) {
        comparePanel.style.display = compareMode ? 'block' : 'none';
    }
    
    if (compareButton) {
        if (compareMode) {
            compareButton.classList.add('active');
            compareButton.textContent = '✕ Cancelar';
        } else {
            compareButton.classList.remove('active');
            compareButton.textContent = '🔄 Comparar';
        }
    }
    
    if (!compareMode) {
        clearComparisonResults();
    }
}

/**
 * Aplica comparação de períodos
 */
async function applyComparison() {
    const start1 = document.getElementById('compare-start-1')?.value;
    const end1 = document.getElementById('compare-end-1')?.value;
    const start2 = document.getElementById('compare-start-2')?.value;
    const end2 = document.getElementById('compare-end-2')?.value;
    
    if (!start1 || !end1 || !start2 || !end2) {
        showNotification('Preencha todos os campos de data para comparar', 'warning');
        return;
    }
    
    try {
        showNotification('Carregando comparação...', 'info');
        
        const [data1, data2] = await Promise.all([
            apiRequest(`/api/dashboard/${AppState.currentDashboard}?start_date=${start1}&end_date=${end1}`),
            apiRequest(`/api/dashboard/${AppState.currentDashboard}?start_date=${start2}&end_date=${end2}`)
        ]);
        
        if (data1.status === 'success' && data2.status === 'success') {
            displayComparison(data1, data2, start1, end1, start2, end2);
        }
    } catch (error) {
        console.error('Erro ao comparar períodos:', error);
        showNotification('Erro ao comparar períodos', 'error');
    }
}

/**
 * Exibe resultados da comparação
 */
function displayComparison(data1, data2, start1, end1, start2, end2) {
    const content = document.getElementById('dashboard-content');
    if (!content) return;
    
    const summary1 = data1.financial_summary || {};
    const summary2 = data2.financial_summary || {};
    
    const comparisonHTML = `
        <div class="compare-results-container">
            <div class="dashboard-card">
                <h2>Comparação de Períodos</h2>
                <div class="compare-periods-info mb-3">
                    <span class="badge bg-primary">Período 1: ${formatDateRange(start1, end1)}</span>
                    <span class="badge bg-secondary ms-2">Período 2: ${formatDateRange(start2, end2)}</span>
                </div>
                
                ${summary1.receita !== undefined ? `
                    <div class="compare-results">
                        <div class="compare-card">
                            <h4>💰 Receita</h4>
                            <div class="mb-2">
                                <div class="fs-4">${formatCurrency(summary1.receita)}</div>
                                <small class="text-muted">Período 1</small>
                            </div>
                            <div>
                                <div class="fs-4">${formatCurrency(summary2.receita)}</div>
                                <small class="text-muted">Período 2</small>
                            </div>
                            ${getVariationBadge(summary1.receita, summary2.receita)}
                        </div>
                        
                        <div class="compare-card">
                            <h4>💸 Despesa</h4>
                            <div class="mb-2">
                                <div class="fs-4">${formatCurrency(summary1.despesa)}</div>
                                <small class="text-muted">Período 1</small>
                            </div>
                            <div>
                                <div class="fs-4">${formatCurrency(summary2.despesa)}</div>
                                <small class="text-muted">Período 2</small>
                            </div>
                            ${getVariationBadge(summary1.despesa, summary2.despesa)}
                        </div>
                        
                        <div class="compare-card">
                            <h4>📈 Lucro</h4>
                            <div class="mb-2">
                                <div class="fs-4 ${summary1.lucro >= 0 ? 'text-success' : 'text-danger'}">${formatCurrency(summary1.lucro)}</div>
                                <small class="text-muted">Período 1</small>
                            </div>
                            <div>
                                <div class="fs-4 ${summary2.lucro >= 0 ? 'text-success' : 'text-danger'}">${formatCurrency(summary2.lucro)}</div>
                                <small class="text-muted">Período 2</small>
                            </div>
                            ${getVariationBadge(summary1.lucro, summary2.lucro)}
                        </div>
                    </div>
                ` : ''}
                
                <div class="mt-3">
                    <button class="btn btn-secondary" onclick="exitComparison()">
                        Voltar ao Dashboard
                    </button>
                </div>
            </div>
        </div>
    `;
    
    content.innerHTML = comparisonHTML;
}

/**
 * Limpa resultados de comparação
 */
function clearComparisonResults() {
    loadDashboard(AppState.currentDashboard);
}

/**
 * Sai do modo de comparação
 */
function exitComparison() {
    toggleCompareMode();
    clearComparisonResults();
}

// Exportar para uso global
window.toggleCompareMode = toggleCompareMode;
window.applyComparison = applyComparison;
window.exitComparison = exitComparison;
window.clearComparisonResults = clearComparisonResults;

