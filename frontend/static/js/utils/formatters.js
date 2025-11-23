// utils/formatters.js - Funções de Formatação

/**
 * Formata moeda
 */
function formatCurrency(value) {
    if (value === null || value === undefined) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value || 0);
}

/**
 * Formata range de datas
 */
function formatDateRange(start, end) {
    const startDate = new Date(start).toLocaleDateString('pt-BR');
    const endDate = new Date(end).toLocaleDateString('pt-BR');
    return `${startDate} - ${endDate}`;
}

/**
 * Retorna o nome de exibição de um dashboard
 */
function getDashboardDisplayName(dashboardName) {
    const names = {
        'geral': 'Visão Geral',
        'financas': 'Finanças',
        'estoque': 'Estoque',
        'publico_alvo': 'Público-Alvo',
        'fornecedores': 'Fornecedores',
        'recursos_humanos': 'Recursos Humanos'
    };
    return names[dashboardName] || dashboardName;
}

/**
 * Gera badge de variação
 */
function getVariationBadge(value1, value2) {
    if (value1 === 0) return '<span class="compare-variation">N/A</span>';
    
    const variation = ((value2 - value1) / value1) * 100;
    const isPositive = variation >= 0;
    const sign = isPositive ? '+' : '';
    
    return `<span class="compare-variation ${isPositive ? 'positive' : 'negative'}">
        ${sign}${variation.toFixed(2)}%
    </span>`;
}

// Exportar para uso global
window.formatCurrency = formatCurrency;
window.formatDateRange = formatDateRange;
window.getDashboardDisplayName = getDashboardDisplayName;
window.getVariationBadge = getVariationBadge;

