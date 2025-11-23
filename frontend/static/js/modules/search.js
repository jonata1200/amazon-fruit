// modules/search.js - Busca Global

let searchTimeout = null;

/**
 * Configura busca global
 */
function setupGlobalSearch() {
    const searchInput = document.getElementById('global-search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        if (query.length < 2) {
            hideSearchResults();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performGlobalSearch(query);
        }, 300);
    });
    
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggleSearch();
        }
    });
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

// Exportar para uso global
window.setupGlobalSearch = setupGlobalSearch;
window.toggleSearch = toggleSearch;
window.performGlobalSearch = performGlobalSearch;
window.hideSearchResults = hideSearchResults;

