// app.js - Sistema de Navegação e Gerenciamento de Estado

// Estado Global da Aplicação
const AppState = {
    currentDashboard: 'geral',
    startDate: null,
    endDate: null,
    isLoading: false
};

// Sistema de Cache
const CacheManager = {
    prefix: 'amazon_fruit_',
    ttl: 5 * 60 * 1000, // 5 minutos
    
    /**
     * Obtém item do cache
     */
    get(key) {
        try {
            const item = localStorage.getItem(this.prefix + key);
            if (!item) return null;
            
            const cached = JSON.parse(item);
            const now = Date.now();
            
            // Verificar se expirou
            if (now > cached.expires) {
                localStorage.removeItem(this.prefix + key);
                return null;
            }
            
            return cached.data;
        } catch (e) {
            console.error('Erro ao ler cache:', e);
            return null;
        }
    },
    
    /**
     * Salva item no cache
     */
    set(key, data, customTTL = null) {
        try {
            const ttl = customTTL || this.ttl;
            const item = {
                data: data,
                expires: Date.now() + ttl,
                timestamp: Date.now()
            };
            localStorage.setItem(this.prefix + key, JSON.stringify(item));
        } catch (e) {
            console.error('Erro ao salvar cache:', e);
            // Se storage estiver cheio, limpar cache antigo
            this.clearOld();
        }
    },
    
    /**
     * Remove item do cache
     */
    remove(key) {
        localStorage.removeItem(this.prefix + key);
    },
    
    /**
     * Limpa cache expirado
     */
    clearOld() {
        try {
            const keys = Object.keys(localStorage);
            const now = Date.now();
            
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    try {
                        const item = JSON.parse(localStorage.getItem(key));
                        if (now > item.expires) {
                            localStorage.removeItem(key);
                        }
                    } catch (e) {
                        // Item inválido, remover
                        localStorage.removeItem(key);
                    }
                }
            });
        } catch (e) {
            console.error('Erro ao limpar cache:', e);
        }
    },
    
    /**
     * Limpa todo o cache
     */
    clear() {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.startsWith(this.prefix)) {
                localStorage.removeItem(key);
            }
        });
    },
    
    /**
     * Gera chave de cache baseada em parâmetros
     */
    generateKey(endpoint, params = {}) {
        const paramStr = Object.keys(params)
            .sort()
            .map(k => `${k}=${params[k]}`)
            .join('&');
        return `${endpoint}${paramStr ? '?' + paramStr : ''}`;
    }
};

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();
});

// Inicializar aplicação
async function initializeApp() {
    console.log('Inicializando aplicação...');
    
    // Carregar preferência de tema
    loadThemePreference();
    
    // Configurar alternância de tema
    setupThemeToggle();
    
    // Configurar menu de navegação
    setupNavigation();
    
    // Configurar barra de período
    setupPeriodBar();
    
    // Configurar atalhos de teclado
    setupKeyboardShortcuts();
    
    // Configurar busca global
    setupGlobalSearch();
    
    // Carregar alertas periodicamente
    loadAlerts();
    setInterval(loadAlerts, 60000); // Atualizar a cada minuto
    
    // Limpar cache antigo ao iniciar
    CacheManager.clearOld();
    
    // Garantir que os elementos existem antes de tentar definir valores
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
    await loadDateRange();
    
    // Aguardar um pouco para garantir que os campos de data foram atualizados
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Forçar atualização dos valores novamente após um delay
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    
    if (AppState.startDate && AppState.endDate) {
        if (startDateInput) {
            startDateInput.value = AppState.startDate;
            startDateInput.setAttribute('value', AppState.startDate);
            // Disparar evento para garantir que o navegador atualize
            startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        if (endDateInput) {
            endDateInput.value = AppState.endDate;
            endDateInput.setAttribute('value', AppState.endDate);
            // Disparar evento para garantir que o navegador atualize
            endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
            endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Verificar valores finais
    console.log('Valores finais nos campos:', {
        startDate: startDateInput ? startDateInput.value : 'não encontrado',
        endDate: endDateInput ? endDateInput.value : 'não encontrado',
        appState: { startDate: AppState.startDate, endDate: AppState.endDate }
    });
    
    // Carregar dashboard inicial com as datas corretas
    await loadDashboard('geral', AppState.startDate, AppState.endDate);
}

// Configurar navegação do menu
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

// Configurar barra de período
function setupPeriodBar() {
    const btnApply = document.getElementById('btn-apply-period');
    const btnReset = document.getElementById('btn-reset-period');
    
    btnApply.addEventListener('click', async () => {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        
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
    
    btnReset.addEventListener('click', async () => {
        await resetPeriod();
    });
}

// Carregar range de datas disponível
async function loadDateRange() {
    console.log('Iniciando carregamento do range de datas...');
    
    try {
        const response = await fetch('/api/data/date-range');
        console.log('Resposta da API recebida:', response.status);
        
        const data = await response.json();
        console.log('Dados da API:', data);
        
        if (data.status === 'success' && data.min_date && data.max_date) {
            // Usar o range completo de datas disponível no banco
            const startDate = data.min_date;
            const endDate = data.max_date;
            
            console.log('Datas extraídas da API:', { startDate, endDate });
            
            // Aguardar um pouco para garantir que o DOM está pronto
            await new Promise(resolve => setTimeout(resolve, 50));
            
            // Atualizar campos de data no DOM
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            console.log('Elementos encontrados:', {
                startDateInput: !!startDateInput,
                endDateInput: !!endDateInput
            });
            
            if (startDateInput) {
                // Definir valor múltiplas vezes para garantir
                startDateInput.setAttribute('value', startDate);
                startDateInput.value = startDate;
                startDateInput.setAttribute('value', startDate);
                
                // Disparar eventos para garantir atualização
                startDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                startDateInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Data inicial definida:', startDateInput.value);
                console.log('Atributo value:', startDateInput.getAttribute('value'));
            } else {
                console.error('Elemento start-date não encontrado!');
            }
            
            if (endDateInput) {
                // Definir valor múltiplas vezes para garantir
                endDateInput.setAttribute('value', endDate);
                endDateInput.value = endDate;
                endDateInput.setAttribute('value', endDate);
                
                // Disparar eventos para garantir atualização
                endDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                endDateInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                console.log('Data final definida:', endDateInput.value);
                console.log('Atributo value:', endDateInput.getAttribute('value'));
            } else {
                console.error('Elemento end-date não encontrado!');
            }
            
            // Atualizar estado da aplicação
            AppState.startDate = startDate;
            AppState.endDate = endDate;
            
            console.log('Range de datas carregado com sucesso:', { startDate, endDate });
            console.log('AppState atualizado:', AppState);
        } else {
            console.warn('API não retornou dados válidos:', data);
            // Fallback: usar último ano se não houver dados
            const endDate = new Date().toISOString().split('T')[0];
            const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
            
            const startDateInput = document.getElementById('start-date');
            const endDateInput = document.getElementById('end-date');
            
            if (startDateInput) {
                startDateInput.value = startDate;
            }
            if (endDateInput) {
                endDateInput.value = endDate;
            }
            
            AppState.startDate = startDate;
            AppState.endDate = endDate;
            
            console.warn('Range de datas não encontrado, usando fallback:', { startDate, endDate });
        }
    } catch (error) {
        console.error('Erro ao carregar range de datas:', error);
        // Em caso de erro, usar fallback
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().split('T')[0];
        
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        
        if (startDateInput) {
            startDateInput.value = startDate;
        }
        if (endDateInput) {
            endDateInput.value = endDate;
        }
        
        AppState.startDate = startDate;
        AppState.endDate = endDate;
    }
}

// Aplicar período e recarregar dashboard
async function applyPeriod(startDate, endDate) {
    const loadingIndicator = document.getElementById('period-loading');
    loadingIndicator.style.display = 'block';
    
    try {
        // Recarregar dashboard atual com novo período
        await loadDashboard(AppState.currentDashboard, startDate, endDate);
        
        // Mostrar feedback de sucesso
        showNotification('Período atualizado com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao aplicar período:', error);
        showNotification('Erro ao atualizar período', 'error');
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

// Resetar período
async function resetPeriod() {
    await loadDateRange();
    await loadDashboard(AppState.currentDashboard);
    showNotification('Período resetado', 'info');
}

// ============================================================================
// FUNÇÕES DE EXPORTAÇÃO
// ============================================================================

/**
 * Exporta dados de uma tabela para Excel ou CSV
 * @param {string} tableName - Nome da tabela (financas, estoque, etc.)
 * @param {string} format - Formato: 'xlsx' ou 'csv'
 * @param {string} startDate - Data inicial (opcional)
 * @param {string} endDate - Data final (opcional)
 */
async function exportTable(tableName, format = 'xlsx', startDate = null, endDate = null) {
    try {
        showNotification('Preparando exportação...', 'info');
        
        // Construir URL com parâmetros
        let url = `/api/export/${tableName}?format=${format}`;
        if (startDate && endDate) {
            url += `&start_date=${startDate}&end_date=${endDate}`;
        }
        
        // Fazer requisição e baixar arquivo
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao exportar dados');
        }
        
        // Obter nome do arquivo do header ou gerar
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `${tableName}_${new Date().toISOString().split('T')[0]}.${format}`;
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Criar blob e fazer download
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
        
        showNotification(`Dados exportados com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar tabela:', error);
        showNotification(`Erro ao exportar: ${error.message}`, 'error');
    }
}

/**
 * Exporta todos os dados de um dashboard
 * @param {string} dashboardName - Nome do dashboard
 * @param {string} format - Formato: 'xlsx' ou 'csv'
 * @param {string} startDate - Data inicial (opcional)
 * @param {string} endDate - Data final (opcional)
 */
async function exportDashboard(dashboardName, format = 'xlsx', startDate = null, endDate = null) {
    try {
        showNotification('Preparando exportação do dashboard...', 'info');
        
        // Construir URL com parâmetros
        let url = `/api/export/dashboard/${dashboardName}?format=${format}`;
        if (startDate && endDate) {
            url += `&start_date=${startDate}&end_date=${endDate}`;
        }
        
        // Fazer requisição e baixar arquivo
        const response = await fetch(url);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao exportar dashboard');
        }
        
        // Obter nome do arquivo do header ou gerar
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `dashboard_${dashboardName}_${new Date().toISOString().split('T')[0]}.${format}`;
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Criar blob e fazer download
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
        
        showNotification(`Dashboard exportado com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar dashboard:', error);
        showNotification(`Erro ao exportar: ${error.message}`, 'error');
    }
}

// Carregar dashboard
async function loadDashboard(dashboardName, startDate = null, endDate = null) {
    AppState.currentDashboard = dashboardName;
    AppState.isLoading = true;
    
    // Atualizar título da página
    updatePageTitle(dashboardName);
    
    // Mostrar loading
    const content = document.getElementById('dashboard-content');
    content.innerHTML = `
        <div class="loading-screen">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p>Carregando dashboard...</p>
        </div>
    `;
    
    // Usar datas do estado se não fornecidas
    const start = startDate || AppState.startDate;
    const end = endDate || AppState.endDate;
    
    try {
        // Carregar conteúdo do dashboard
        await loadDashboardContent(dashboardName, start, end);
    } catch (error) {
        console.error(`Erro ao carregar dashboard ${dashboardName}:`, error);
        content.innerHTML = `
            <div class="alert alert-danger">
                <h4>Erro ao carregar dashboard</h4>
                <p>${error.message}</p>
            </div>
        `;
    } finally {
        AppState.isLoading = false;
    }
}

// Carregar conteúdo do dashboard
async function loadDashboardContent(dashboardName, startDate, endDate) {
    const content = document.getElementById('dashboard-content');
    
    // Carregar HTML do dashboard (se existir)
    try {
        const response = await fetch(`/templates/dashboards/${dashboardName}.html`);
        if (response.ok) {
            const html = await response.text();
            content.innerHTML = html;
        } else {
            // Se não encontrar HTML, criar estrutura básica
            content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
        }
    } catch (error) {
        // Se erro, criar estrutura básica
        content.innerHTML = `<div class="dashboard-card"><h2>Dashboard ${dashboardName}</h2><p>Carregando...</p></div>`;
    }
    
    // Carregar JavaScript específico do dashboard
    await loadDashboardScript(dashboardName, startDate, endDate);
}

// Carregar script do dashboard
async function loadDashboardScript(dashboardName, startDate, endDate) {
    // Remover script anterior se existir
    const oldScript = document.getElementById('dashboard-script');
    if (oldScript) {
        oldScript.remove();
    }
    
    // Criar novo script
    const script = document.createElement('script');
    script.id = 'dashboard-script';
    script.src = `/static/js/dashboards/${dashboardName}.js`;
    script.onload = () => {
        // Mapear nomes de dashboard para nomes de função
        const functionMap = {
            'geral': 'initGeralDashboard',
            'financas': 'initFinancasDashboard',
            'estoque': 'initEstoqueDashboard',
            'publico_alvo': 'initPublicoAlvoDashboard',
            'fornecedores': 'initFornecedoresDashboard',
            'recursos_humanos': 'initRecursosHumanosDashboard'
        };
        
        const functionName = functionMap[dashboardName];
        if (functionName && window[functionName]) {
            window[functionName](startDate, endDate);
        } else {
            console.warn(`Função de inicialização não encontrada para: ${dashboardName}`);
        }
    };
    document.body.appendChild(script);
}

// Atualizar título da página
function updatePageTitle(dashboardName) {
    const titles = {
        'geral': 'Visão Geral do Negócio',
        'financas': 'Finanças',
        'estoque': 'Estoque',
        'publico_alvo': 'Público-Alvo',
        'fornecedores': 'Fornecedores',
        'recursos_humanos': 'Recursos Humanos'
    };
    
    document.getElementById('page-title').textContent = titles[dashboardName] || 'Dashboard';
    
    // Mostrar/ocultar botão de relatório
    const btnReport = document.getElementById('btn-report');
    if (dashboardName === 'geral') {
        btnReport.style.display = 'block';
        btnReport.onclick = () => generateReport(startDate, endDate);
    } else {
        btnReport.style.display = 'none';
    }
}

// Mostrar notificação
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Função auxiliar para fazer requisições à API com cache
async function apiRequest(endpoint, options = {}) {
    // Verificar se deve usar cache (apenas GET)
    const useCache = !options.method || options.method === 'GET';
    const cacheKey = useCache ? CacheManager.generateKey(endpoint, options.params) : null;
    
    // Tentar obter do cache
    if (useCache && cacheKey) {
        const cached = CacheManager.get(cacheKey);
        if (cached !== null) {
            console.log('Cache hit:', cacheKey);
            return cached;
        }
    }
    
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Salvar no cache se for GET
        if (useCache && cacheKey) {
            CacheManager.set(cacheKey, data);
        }
        
        return data;
    } catch (error) {
        console.error('Erro na requisição API:', error);
        throw error;
    }
}

/**
 * Invalida cache de um endpoint específico
 */
function invalidateCache(endpoint) {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
        if (key.startsWith(CacheManager.prefix) && key.includes(endpoint)) {
            CacheManager.remove(key.replace(CacheManager.prefix, ''));
        }
    });
}

// Gerar relatório (placeholder)
async function generateReport(startDate, endDate) {
    showNotification('Funcionalidade de relatório será implementada na Fase 4', 'info');
}

// ============================================================================
// FUNÇÕES DE EXPORTAÇÃO DE GRÁFICOS
// ============================================================================

/**
 * Exporta um gráfico Plotly para PNG, SVG ou PDF
 * @param {string} chartId - ID do elemento do gráfico
 * @param {string} format - Formato: 'png', 'svg' ou 'pdf'
 * @param {string} filename - Nome do arquivo (opcional)
 */
async function exportChart(chartId, format = 'png', filename = null) {
    try {
        const chartElement = document.getElementById(chartId);
        
        if (!chartElement) {
            throw new Error(`Gráfico com ID '${chartId}' não encontrado`);
        }
        
        // Verificar se o gráfico existe no Plotly
        const chartData = chartElement.data;
        if (!chartData || chartData.length === 0) {
            showNotification('Gráfico ainda não foi carregado', 'warning');
            return;
        }
        
        showNotification(`Exportando gráfico como ${format.toUpperCase()}...`, 'info');
        
        // Gerar nome do arquivo se não fornecido
        if (!filename) {
            const timestamp = new Date().toISOString().split('T')[0];
            filename = `grafico_${chartId}_${timestamp}.${format}`;
        }
        
        // Configurações de exportação
        const config = {
            format: format,
            width: chartElement.offsetWidth || 800,
            height: chartElement.offsetHeight || 600,
            filename: filename
        };
        
        // Exportar usando Plotly
        await Plotly.downloadImage(chartElement, config);
        
        showNotification(`Gráfico exportado com sucesso! (${filename})`, 'success');
    } catch (error) {
        console.error('Erro ao exportar gráfico:', error);
        showNotification(`Erro ao exportar gráfico: ${error.message}`, 'error');
    }
}

/**
 * Adiciona botões de exportação a um gráfico
 * @param {string} chartId - ID do elemento do gráfico
 * @param {string} chartTitle - Título do gráfico (para nome do arquivo)
 */
function addChartExportButtons(chartId, chartTitle = null) {
    const chartContainer = document.getElementById(chartId);
    
    if (!chartContainer) {
        console.warn(`Container do gráfico '${chartId}' não encontrado`);
        return;
    }
    
    // Verificar se já existe um container de botões
    let buttonContainer = chartContainer.parentElement.querySelector('.chart-export-buttons');
    
    if (!buttonContainer) {
        // Criar container de botões
        buttonContainer = document.createElement('div');
        buttonContainer.className = 'chart-export-buttons mb-2';
        buttonContainer.style.textAlign = 'right';
        
        // Inserir antes do gráfico
        chartContainer.parentElement.insertBefore(buttonContainer, chartContainer);
    }
    
    // Limpar botões existentes
    buttonContainer.innerHTML = '';
    
    // Criar botões de exportação
    const formats = [
        { format: 'png', label: 'PNG', icon: '🖼️' },
        { format: 'svg', label: 'SVG', icon: '📐' },
        { format: 'pdf', label: 'PDF', icon: '📄' }
    ];
    
    formats.forEach(({ format, label, icon }) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-sm btn-outline-secondary me-1';
        button.title = `Exportar como ${label}`;
        button.innerHTML = `${icon} ${label}`;
        button.onclick = () => {
            const filename = chartTitle 
                ? `${chartTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_${new Date().toISOString().split('T')[0]}.${format}`
                : null;
            exportChart(chartId, format, filename);
        };
        buttonContainer.appendChild(button);
    });
}

// ============================================================================
// FUNÇÕES DE MODO ESCURO
// ============================================================================

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
    
    // Salvar preferência
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    // Atualizar ícone
    updateThemeIcon(isDark);
    
    // Atualizar gráficos Plotly
    updatePlotlyTheme(isDark);
    
    // Notificação
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
        toggleButton.textContent = isDark ? '☀️' : '🌙';
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
    
    // Atualizar todos os gráficos existentes
    const chartContainers = document.querySelectorAll('[id^="chart-"]');
    chartContainers.forEach(container => {
        if (container.data && container.data.length > 0) {
            Plotly.relayout(container, plotlyTheme);
        }
    });
}

// Exportar funções úteis
window.AppState = AppState;
window.apiRequest = apiRequest;
window.showNotification = showNotification;
window.exportTable = exportTable;
window.exportDashboard = exportDashboard;
window.exportChart = exportChart;
window.addChartExportButtons = addChartExportButtons;
window.toggleDarkMode = toggleDarkMode;
window.getPlotlyTheme = getPlotlyTheme;
window.showKeyboardShortcutsHelp = showKeyboardShortcutsHelp;

// ============================================================================
// SISTEMA DE ALERTAS
// ============================================================================

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
        
        // Se abrindo, atualizar alertas
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

window.toggleAlertsPanel = toggleAlertsPanel;
window.navigateToAlert = navigateToAlert;
window.toggleSearch = toggleSearch;

// ============================================================================
// COMPARAÇÃO DE PERÍODOS
// ============================================================================

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
    
    // Se desativando, limpar resultados de comparação
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
        
        // Carregar dados dos dois períodos
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
    
    // Obter resumos financeiros se disponíveis
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
 * Formata range de datas
 */
function formatDateRange(start, end) {
    const startDate = new Date(start).toLocaleDateString('pt-BR');
    const endDate = new Date(end).toLocaleDateString('pt-BR');
    return `${startDate} - ${endDate}`;
}

/**
 * Formata moeda (função auxiliar global)
 */
function formatCurrency(value) {
    if (value === null || value === undefined) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value || 0);
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

/**
 * Limpa resultados de comparação
 */
function clearComparisonResults() {
    // Voltar ao dashboard normal
    loadDashboard(AppState.currentDashboard);
}

/**
 * Sai do modo de comparação
 */
function exitComparison() {
    toggleCompareMode();
    clearComparisonResults();
}

window.toggleCompareMode = toggleCompareMode;
window.applyComparison = applyComparison;
window.exitComparison = exitComparison;
window.formatCurrency = formatCurrency;

// ============================================================================
// ATALHOS DE TECLADO
// ============================================================================

// Mapeamento de dashboards
const DASHBOARD_MAP = {
    '1': 'geral',
    '2': 'financas',
    '3': 'estoque',
    '4': 'publico_alvo',
    '5': 'fornecedores',
    '6': 'recursos_humanos'
};

/**
 * Configura os atalhos de teclado da aplicação
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ignorar se estiver digitando em um input/textarea
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            // Permitir Esc mesmo em inputs
            if (e.key === 'Escape') {
                handleEscapeKey(e);
            }
            return;
        }
        
        // Ctrl + número (1-6): Navegar entre dashboards
        if (e.ctrlKey && /^[1-6]$/.test(e.key)) {
            e.preventDefault();
            const dashboard = DASHBOARD_MAP[e.key];
            if (dashboard) {
                navigateToDashboard(dashboard);
            }
        }
        
        // Ctrl + F: Abrir busca
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            toggleSearch();
        }
        
        // Ctrl + E: Exportar dados do dashboard atual
        if (e.ctrlKey && e.key === 'e') {
            e.preventDefault();
            exportCurrentDashboard();
        }
        
        // Ctrl + R: Gerar relatório
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            generateReportShortcut();
        }
        
        // Ctrl + T: Alternar tema (modo escuro)
        if (e.ctrlKey && e.key === 't') {
            e.preventDefault();
            toggleDarkMode();
        }
        
        // Ctrl + ? ou Ctrl + Shift + /: Mostrar ajuda de atalhos
        if ((e.ctrlKey && e.key === '?') || (e.ctrlKey && e.shiftKey && e.key === '/')) {
            e.preventDefault();
            showKeyboardShortcutsHelp();
        }
        
        // Esc: Fechar modais/limpar busca
        if (e.key === 'Escape') {
            handleEscapeKey(e);
        }
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
 * Alterna a exibição da busca global
 */
function toggleSearch() {
    const searchInput = document.getElementById('global-search-input');
    if (searchInput) {
        const isVisible = searchInput.style.display !== 'none';
        searchInput.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            searchInput.focus();
        } else {
            searchInput.value = '';
            hideSearchResults();
        }
    }
}

/**
 * Realiza busca global
 */
let searchTimeout = null;

function setupGlobalSearch() {
    const searchInput = document.getElementById('global-search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        // Limpar timeout anterior
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        // Se query muito curta, limpar resultados
        if (query.length < 2) {
            hideSearchResults();
            return;
        }
        
        // Debounce: aguardar 300ms antes de buscar
        searchTimeout = setTimeout(() => {
            performGlobalSearch(query);
        }, 300);
    });
    
    // Fechar ao pressionar Esc
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggleSearch();
        }
    });
}

/**
 * Executa a busca global
 */
async function performGlobalSearch(query) {
    try {
        const resultsContainer = getOrCreateSearchResults();
        resultsContainer.innerHTML = '<div class="text-center p-3"><div class="spinner-border spinner-border-sm"></div><p class="mt-2 mb-0">Buscando...</p></div>';
        
        const response = await apiRequest(`/api/search/?q=${encodeURIComponent(query)}&limit=5`);
        
        if (response.status === 'success') {
            displaySearchResults(response);
        }
    } catch (error) {
        console.error('Erro na busca:', error);
        const resultsContainer = getOrCreateSearchResults();
        resultsContainer.innerHTML = '<div class="text-danger p-3">Erro ao realizar busca</div>';
    }
}

/**
 * Obtém ou cria o container de resultados
 */
function getOrCreateSearchResults() {
    let container = document.getElementById('search-results');
    if (!container) {
        container = document.createElement('div');
        container.id = 'search-results';
        container.className = 'search-results';
        const searchContainer = document.querySelector('.search-container');
        if (searchContainer) {
            searchContainer.appendChild(container);
        }
    }
    return container;
}

/**
 * Exibe resultados da busca
 */
function displaySearchResults(data) {
    const container = getOrCreateSearchResults();
    const results = data.results;
    const total = data.total;
    
    if (total === 0) {
        container.innerHTML = '<div class="text-muted p-3">Nenhum resultado encontrado</div>';
        return;
    }
    
    let html = `<div class="search-results-header">${total} resultado(s) encontrado(s)</div>`;
    
    // Produtos
    if (results.products && results.products.length > 0) {
        html += '<div class="search-results-section"><strong>📦 Produtos</strong>';
        results.products.forEach(item => {
            html += `
                <div class="search-result-item" onclick="navigateToDashboard('estoque')">
                    <div class="search-result-title">${item.name}</div>
                    <div class="search-result-detail">Estoque: ${item.stock} | Preço: R$ ${item.price?.toFixed(2) || '0.00'}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Fornecedores
    if (results.suppliers && results.suppliers.length > 0) {
        html += '<div class="search-results-section"><strong>🚚 Fornecedores</strong>';
        results.suppliers.forEach(item => {
            html += `
                <div class="search-result-item" onclick="navigateToDashboard('fornecedores')">
                    <div class="search-result-title">${item.name}</div>
                    <div class="search-result-detail">${item.city}, ${item.state} | Avaliação: ${item.rating?.toFixed(1) || 'N/A'}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Clientes
    if (results.customers && results.customers.length > 0) {
        html += '<div class="search-results-section"><strong>👥 Clientes</strong>';
        results.customers.forEach(item => {
            html += `
                <div class="search-result-item" onclick="navigateToDashboard('publico_alvo')">
                    <div class="search-result-title">${item.city}</div>
                    <div class="search-result-detail">Canal: ${item.channel} | Gasto médio: R$ ${item.avg_spending?.toFixed(2) || '0.00'}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Funcionários
    if (results.employees && results.employees.length > 0) {
        html += '<div class="search-results-section"><strong>👔 Funcionários</strong>';
        results.employees.forEach(item => {
            html += `
                <div class="search-result-item" onclick="navigateToDashboard('recursos_humanos')">
                    <div class="search-result-title">${item.name}</div>
                    <div class="search-result-detail">${item.role} - ${item.department}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Categorias financeiras
    if (results.financial && results.financial.length > 0) {
        html += '<div class="search-results-section"><strong>💰 Categorias Financeiras</strong>';
        results.financial.forEach(item => {
            html += `
                <div class="search-result-item" onclick="navigateToDashboard('financas')">
                    <div class="search-result-title">${item.category}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    container.innerHTML = html;
}

/**
 * Esconde resultados da busca
 */
function hideSearchResults() {
    const container = document.getElementById('search-results');
    if (container) {
        container.innerHTML = '';
    }
}

/**
 * Exporta o dashboard atual
 */
function exportCurrentDashboard() {
    const dashboard = AppState.currentDashboard;
    const startDate = AppState.startDate;
    const endDate = AppState.endDate;
    
    if (dashboard) {
        exportDashboard(dashboard, 'xlsx', startDate, endDate);
        showNotification('Exportando dashboard...', 'info');
    } else {
        showNotification('Nenhum dashboard selecionado', 'warning');
    }
}

/**
 * Gera relatório (atalho)
 */
function generateReportShortcut() {
    const startDate = AppState.startDate;
    const endDate = AppState.endDate;
    
    if (startDate && endDate) {
        generateReport(startDate, endDate);
    } else {
        showNotification('Selecione um período antes de gerar o relatório', 'warning');
    }
}

/**
 * Trata a tecla Esc
 */
function handleEscapeKey(e) {
    // Fechar modais do Bootstrap se estiverem abertos
    const openModals = document.querySelectorAll('.modal.show');
    openModals.forEach(modal => {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    });
    
    // Limpar busca se houver campo de busca visível
    const searchInput = document.querySelector('#search-input');
    if (searchInput && searchInput.value) {
        searchInput.value = '';
        searchInput.blur();
    }
}

/**
 * Mostra ajuda de atalhos de teclado
 */
function showKeyboardShortcutsHelp() {
    const shortcuts = [
        { keys: 'Ctrl + 1-6', description: 'Navegar entre dashboards' },
        { keys: 'Ctrl + F', description: 'Abrir busca global' },
        { keys: 'Ctrl + E', description: 'Exportar dashboard atual (Excel)' },
        { keys: 'Ctrl + R', description: 'Gerar relatório PDF' },
        { keys: 'Ctrl + T', description: 'Alternar modo escuro/claro' },
        { keys: 'Ctrl + ?', description: 'Mostrar esta ajuda' },
        { keys: 'Esc', description: 'Fechar modais/limpar busca' }
    ];
    
    const helpHTML = `
        <div class="keyboard-shortcuts-help">
            <h4>⌨️ Atalhos de Teclado</h4>
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Atalho</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
                    ${shortcuts.map(s => `
                        <tr>
                            <td><kbd>${s.keys}</kbd></td>
                            <td>${s.description}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <p class="text-muted small mt-2">Pressione Esc para fechar</p>
        </div>
    `;
    
    // Criar modal de ajuda
    const modalHTML = `
        <div class="modal fade" id="keyboardShortcutsModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">⌨️ Atalhos de Teclado</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${helpHTML}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal existente se houver
    const existingModal = document.getElementById('keyboardShortcutsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Adicionar modal ao body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('keyboardShortcutsModal'));
    modal.show();
    
    // Remover modal do DOM quando fechar
    document.getElementById('keyboardShortcutsModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Adicionar estilo para kbd
if (!document.getElementById('keyboard-shortcuts-style')) {
    const style = document.createElement('style');
    style.id = 'keyboard-shortcuts-style';
    style.textContent = `
        kbd {
            background-color: #f7f7f7;
            border: 1px solid #ccc;
            border-radius: 3px;
            box-shadow: 0 1px 0 rgba(0,0,0,0.2), inset 0 0 0 2px #fff;
            color: #333;
            display: inline-block;
            font-family: monospace;
            font-size: 0.85em;
            font-weight: bold;
            line-height: 1.4;
            padding: 0.1em 0.6em;
            white-space: nowrap;
        }
        body.dark-mode kbd {
            background-color: #2d2d2d;
            border-color: #555;
            color: #e0e0e0;
            box-shadow: 0 1px 0 rgba(0,0,0,0.5), inset 0 0 0 2px #252525;
        }
        .keyboard-shortcuts-help table {
            margin-bottom: 0;
        }
        .keyboard-shortcuts-help kbd {
            font-size: 0.9em;
        }
    `;
    document.head.appendChild(style);
}

