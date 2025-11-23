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
 * Obtém o tema Plotly baseado no modo atual
 */
function getPlotlyTheme(baseLayout = {}) {
    const isDark = document.body.classList.contains('dark-mode');
    
    return {
        ...baseLayout,
        plot_bgcolor: isDark ? '#252525' : (baseLayout.plot_bgcolor || 'white'),
        paper_bgcolor: isDark ? '#252525' : (baseLayout.paper_bgcolor || 'white'),
        font: {
            color: isDark ? '#e0e0e0' : '#333333',
            ...baseLayout.font
        },
        xaxis: {
            ...baseLayout.xaxis,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        },
        yaxis: {
            ...baseLayout.yaxis,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        },
        yaxis2: baseLayout.yaxis2 ? {
            ...baseLayout.yaxis2,
            gridcolor: isDark ? '#404040' : '#e0e0e0',
            linecolor: isDark ? '#606060' : '#333333'
        } : undefined
    };
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

