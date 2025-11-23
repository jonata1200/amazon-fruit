// modules/theme.js - Gerenciamento de Tema (Modo Escuro)

/**
 * Carrega a preferência de tema salva no localStorage
 */
function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        updateThemeIcon(true);
        updatePlotlyTheme(true);
    }
}

/**
 * Configura o botão de alternância de tema
 */
function setupThemeToggle() {
    const toggleButton = document.getElementById('btn-toggle-theme');
    if (!toggleButton) return;
    
    toggleButton.addEventListener('click', () => {
        toggleDarkMode();
    });
}

/**
 * Alterna entre modo escuro e claro
 */
function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-mode');
    
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
    updatePlotlyTheme(isDark);
    
    showNotification(
        isDark ? 'Modo escuro ativado' : 'Modo claro ativado',
        'info'
    );
}

/**
 * Atualiza o ícone do botão de tema
 */
function updateThemeIcon(isDark) {
    const toggleButton = document.getElementById('btn-toggle-theme');
    if (toggleButton) {
        const icon = toggleButton.querySelector('i');
        if (icon) {
            icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        } else {
            toggleButton.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }
        toggleButton.title = isDark ? 'Alternar para modo claro' : 'Alternar para modo escuro';
    }
}

/**
 * Cria um gráfico Plotly com tratamento de erros
 */
function createPlotlyChart(elementId, data, baseLayout, config = {}) {
    const chartElement = document.getElementById(elementId);
    if (!chartElement) {
        console.error(`Elemento ${elementId} não encontrado`);
        return;
    }
    
    try {
        const layout = getPlotlyTheme(baseLayout);
        Plotly.newPlot(elementId, data, layout, {responsive: true, ...config});
    } catch (error) {
        console.error(`Erro ao renderizar gráfico ${elementId}:`, error);
        chartElement.innerHTML = '<p class="text-danger">Erro ao renderizar gráfico.</p>';
    }
}

/**
 * Obtém o tema Plotly baseado no modo atual
 */
function getPlotlyTheme(baseLayout = {}) {
    const isDark = document.body.classList.contains('dark-mode');
    
    // Criar layout com tema aplicado
    const themedLayout = {
        ...baseLayout,
        plot_bgcolor: isDark ? '#252525' : (baseLayout.plot_bgcolor || 'white'),
        paper_bgcolor: isDark ? '#252525' : (baseLayout.paper_bgcolor || 'white'),
        font: {
            color: isDark ? '#e0e0e0' : '#333333',
            size: baseLayout.font?.size || 12,
            family: baseLayout.font?.family || 'Arial, sans-serif'
        }
    };
    
    // Aplicar tema aos eixos se existirem
    if (baseLayout.xaxis) {
        themedLayout.xaxis = {
            ...baseLayout.xaxis,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333',
            title: {
                ...baseLayout.xaxis.title,
                font: {
                    color: isDark ? '#e0e0e0' : '#333333'
                }
            }
        };
    } else {
        themedLayout.xaxis = {
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        };
    }
    
    if (baseLayout.yaxis) {
        themedLayout.yaxis = {
            ...baseLayout.yaxis,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333',
            title: {
                ...baseLayout.yaxis.title,
                font: {
                    color: isDark ? '#e0e0e0' : '#333333'
                }
            }
        };
    } else {
        themedLayout.yaxis = {
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        };
    }
    
    // Aplicar tema ao yaxis2 se existir
    if (baseLayout.yaxis2) {
        themedLayout.yaxis2 = {
            ...baseLayout.yaxis2,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        };
    }
    
    return themedLayout;
}

/**
 * Atualiza o tema dos gráficos Plotly existentes
 */
function updatePlotlyTheme(isDark) {
    const plotlyTheme = {
        plot_bgcolor: isDark ? '#252525' : 'white',
        paper_bgcolor: isDark ? '#252525' : 'white',
        font: {
            color: isDark ? '#e0e0e0' : '#333333'
        },
        xaxis: {
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        },
        yaxis: {
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        }
    };
    
    const chartContainers = document.querySelectorAll('[id^="chart-"]');
    chartContainers.forEach(container => {
        if (container.data && container.data.length > 0) {
            Plotly.relayout(container, plotlyTheme);
        }
    });
}

// Exportar para uso global
window.loadThemePreference = loadThemePreference;
window.setupThemeToggle = setupThemeToggle;
window.toggleDarkMode = toggleDarkMode;
window.updateThemeIcon = updateThemeIcon;
window.getPlotlyTheme = getPlotlyTheme;
window.updatePlotlyTheme = updatePlotlyTheme;
window.createPlotlyChart = createPlotlyChart;

