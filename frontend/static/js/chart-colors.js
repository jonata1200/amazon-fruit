// chart-colors.js - Paleta de Cores Consistente para Gráficos Plotly

/**
 * Paleta de cores padrão para gráficos
 * Baseada no Design System do projeto
 */
const ChartColors = {
    // Cores principais do design system
    primary: '#6A0DAD',
    primaryLight: '#8B1FD4',
    primaryDark: '#4A0A7A',
    
    // Cores de status
    success: '#2E8B57',
    successLight: '#4CAF50',
    danger: '#C21807',
    dangerLight: '#E53935',
    warning: '#F39C12',
    warningLight: '#FF9800',
    info: '#3498DB',
    infoLight: '#42A5F5',
    
    // Cores para séries específicas
    receita: '#2E8B57',      // Verde (success)
    despesa: '#C21807',      // Vermelho (danger)
    lucro: '#3498DB',        // Azul (info)
    lucroNegativo: '#C21807', // Vermelho (danger)
    
    // Paleta para múltiplas séries
    palette: [
        '#6A0DAD',  // Roxo principal
        '#2E8B57',  // Verde
        '#3498DB',  // Azul
        '#F39C12',  // Laranja
        '#C21807',  // Vermelho
        '#8B1FD4',  // Roxo claro
        '#4CAF50',  // Verde claro
        '#42A5F5',  // Azul claro
        '#FF9800',  // Laranja claro
        '#E53935'   // Vermelho claro
    ],
    
    // Cores para gráficos de pizza/gênero
    gender: {
        'Feminino': '#FF69B4',
        'Masculino': '#1E90FF',
        'Outro': '#CCCCCC'
    },
    
    // Cores para categorias financeiras
    financial: {
        receita: '#2E8B57',
        despesa: '#C21807',
        lucro: '#3498DB'
    }
};

/**
 * Obtém cor da paleta baseada no índice
 */
function getColorFromPalette(index) {
    return ChartColors.palette[index % ChartColors.palette.length];
}

/**
 * Obtém cor para tipo de dado financeiro
 */
function getFinancialColor(type) {
    return ChartColors.financial[type] || ChartColors.primary;
}

/**
 * Obtém cor para gênero
 */
function getGenderColor(gender) {
    return ChartColors.gender[gender] || '#CCCCCC';
}

// Exportar para uso global
window.ChartColors = ChartColors;
window.getColorFromPalette = getColorFromPalette;
window.getFinancialColor = getFinancialColor;
window.getGenderColor = getGenderColor;

