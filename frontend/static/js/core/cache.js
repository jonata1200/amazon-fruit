// core/cache.js - Sistema de Cache

/**
 * Sistema de Cache usando localStorage
 */
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

// Exportar para uso global
window.CacheManager = CacheManager;

