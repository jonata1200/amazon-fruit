// filters.js - Sistema de Filtros Avançados

/**
 * Gerenciador de filtros avançados
 */
const FilterManager = {
    currentFilters: {},
    
    /**
     * Aplica filtros a uma tabela HTML
     */
    applyTableFilters(tableId, filters) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.forEach(row => {
            let show = true;
            
            // Aplicar cada filtro
            Object.keys(filters).forEach(key => {
                const filterValue = filters[key];
                if (!filterValue || filterValue === '') return;
                
                const cell = row.querySelector(`td[data-filter="${key}"]`);
                if (!cell) {
                    // Tentar encontrar por índice de coluna
                    const header = table.querySelector(`th[data-filter="${key}"]`);
                    if (header) {
                        const colIndex = Array.from(header.parentElement.children).indexOf(header);
                        const cells = row.querySelectorAll('td');
                        if (cells[colIndex]) {
                            const cellText = cells[colIndex].textContent.toLowerCase();
                            if (!cellText.includes(filterValue.toLowerCase())) {
                                show = false;
                            }
                        }
                    }
                } else {
                    const cellText = cell.textContent.toLowerCase();
                    if (!cellText.includes(filterValue.toLowerCase())) {
                        show = false;
                    }
                }
            });
            
            row.style.display = show ? '' : 'none';
        });
        
        // Atualizar contador
        const visibleRows = rows.filter(r => r.style.display !== 'none').length;
        this.updateFilterCount(tableId, visibleRows, rows.length);
    },
    
    /**
     * Atualiza contador de resultados filtrados
     */
    updateFilterCount(tableId, visible, total) {
        let counter = document.getElementById(`${tableId}-filter-count`);
        if (!counter) {
            const table = document.getElementById(tableId);
            if (table) {
                counter = document.createElement('div');
                counter.id = `${tableId}-filter-count`;
                counter.className = 'filter-count';
                table.parentElement.insertBefore(counter, table);
            }
        }
        
        if (counter) {
            if (visible < total) {
                counter.textContent = `Mostrando ${visible} de ${total} resultados`;
                counter.style.display = 'block';
            } else {
                counter.style.display = 'none';
            }
        }
    },
    
    /**
     * Limpa todos os filtros
     */
    clearFilters(filterContainerId) {
        const container = document.getElementById(filterContainerId);
        if (!container) return;
        
        const inputs = container.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.value = '';
        });
        
        this.currentFilters = {};
        
        // Recarregar tabela sem filtros
        const tableId = container.getAttribute('data-table-id');
        if (tableId) {
            const table = document.getElementById(tableId);
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => row.style.display = '');
                this.updateFilterCount(tableId, rows.length, rows.length);
            }
        }
    },
    
    /**
     * Salva filtros no localStorage
     */
    saveFilters(dashboardName, filters) {
        try {
            const key = `filters_${dashboardName}`;
            localStorage.setItem(key, JSON.stringify(filters));
        } catch (e) {
            console.error('Erro ao salvar filtros:', e);
        }
    },
    
    /**
     * Carrega filtros salvos do localStorage
     */
    loadFilters(dashboardName) {
        try {
            const key = `filters_${dashboardName}`;
            const saved = localStorage.getItem(key);
            if (saved) {
                return JSON.parse(saved);
            }
        } catch (e) {
            console.error('Erro ao carregar filtros:', e);
        }
        return {};
    }
};

/**
 * Cria componente de filtros para um dashboard
 */
function createFilterPanel(dashboardName, filtersConfig) {
    const filterHTML = `
        <div class="filters-panel" id="filters-${dashboardName}" data-table-id="table-${dashboardName}">
            <div class="filters-header">
                <h5>🔍 Filtros Avançados</h5>
                <button class="btn btn-sm btn-outline-secondary" onclick="FilterManager.clearFilters('filters-${dashboardName}')">
                    Limpar
                </button>
            </div>
            <div class="filters-content">
                ${filtersConfig.map(filter => {
                    if (filter.type === 'select') {
                        return `
                            <div class="filter-item">
                                <label>${filter.label}:</label>
                                <select class="form-control form-control-sm" data-filter="${filter.key}" onchange="applyFilter('${dashboardName}')">
                                    <option value="">Todos</option>
                                    ${filter.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                                </select>
                            </div>
                        `;
                    } else {
                        return `
                            <div class="filter-item">
                                <label>${filter.label}:</label>
                                <input type="${filter.type || 'text'}" class="form-control form-control-sm" 
                                       data-filter="${filter.key}" 
                                       placeholder="${filter.placeholder || ''}"
                                       oninput="applyFilter('${dashboardName}')">
                            </div>
                        `;
                    }
                }).join('')}
            </div>
        </div>
    `;
    
    return filterHTML;
}

/**
 * Aplica filtros de um dashboard
 */
function applyFilter(dashboardName) {
    const filterPanel = document.getElementById(`filters-${dashboardName}`);
    if (!filterPanel) return;
    
    const filters = {};
    const inputs = filterPanel.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        const key = input.getAttribute('data-filter');
        const value = input.value.trim();
        if (key && value) {
            filters[key] = value;
        }
    });
    
    FilterManager.currentFilters = filters;
    FilterManager.saveFilters(dashboardName, filters);
    
    const tableId = `table-${dashboardName}`;
    FilterManager.applyTableFilters(tableId, filters);
}

// Exportar para uso global
window.FilterManager = FilterManager;
window.createFilterPanel = createFilterPanel;
window.applyFilter = applyFilter;

