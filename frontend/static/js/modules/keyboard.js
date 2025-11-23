// modules/keyboard.js - Atalhos de Teclado

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
    
    const existingModal = document.getElementById('keyboardShortcutsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = new bootstrap.Modal(document.getElementById('keyboardShortcutsModal'));
    modal.show();
    
    document.getElementById('keyboardShortcutsModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Adicionar estilo para kbd se não existir
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

// Exportar para uso global
window.setupKeyboardShortcuts = setupKeyboardShortcuts;
window.handleEscapeKey = handleEscapeKey;
window.generateReportShortcut = generateReportShortcut;
window.showKeyboardShortcutsHelp = showKeyboardShortcutsHelp;

