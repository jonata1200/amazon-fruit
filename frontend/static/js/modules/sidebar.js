// modules/sidebar.js - Sidebar Mobile

/**
 * Configura sidebar para mobile
 */
function setupMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    
    if (!sidebar || !menuToggle) return;
    
    // Fechar sidebar ao clicar fora (mobile)
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (sidebar.classList.contains('open')) {
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            }
        }
    });
}

/**
 * Alterna sidebar (mobile)
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    if (sidebar && menuToggle) {
        const isOpen = sidebar.classList.toggle('open');
        menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
    }
}

// Exportar para uso global
window.setupMobileSidebar = setupMobileSidebar;
window.toggleSidebar = toggleSidebar;

