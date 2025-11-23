// utils/api.js - Funções auxiliares para requisições à API

/**
 * Função auxiliar para fazer requisições à API com cache
 */
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

// Exportar para uso global
window.apiRequest = apiRequest;
window.invalidateCache = invalidateCache;

