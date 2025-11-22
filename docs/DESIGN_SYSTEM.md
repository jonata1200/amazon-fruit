# Design System - Amazon Fruit

## 🎨 Paleta de Cores

### Cores Principais

```css
--primary: #6A0DAD;        /* Roxo principal - identidade da marca */
--primary-dark: #4A0A7A;   /* Roxo escuro - hover/ativo */
--primary-light: #8B1FD4;   /* Roxo claro - estados hover */
--primary-gradient-start: #6A0DAD;
--primary-gradient-end: #8B2FD9;
```

**Uso:** Botões primários, links, elementos de destaque, sidebar

### Cores de Status

```css
--success: #2E8B57;        /* Verde - sucesso, positivo */
--success-light: #4CAF50;
--danger: #C21807;         /* Vermelho - erro, negativo */
--danger-light: #E53935;
--warning: #F39C12;        /* Laranja - aviso, atenção */
--warning-light: #FF9800;
--info: #3498DB;           /* Azul - informação */
--info-light: #42A5F5;
```

**Uso:** 
- Success: KPIs positivos, confirmações, badges de sucesso
- Danger: Alertas críticos, valores negativos, erros
- Warning: Avisos, estoque baixo, atenção necessária
- Info: Informações gerais, tooltips, badges informativos

### Cores Neutras (Modo Claro)

```css
--bg-primary: #FFFFFF;           /* Fundo principal */
--bg-secondary: #F7F7F9;          /* Fundo secundário */
--bg-tertiary: #F0F0F0;          /* Fundo terciário */
--text-primary: #333333;          /* Texto principal */
--text-secondary: #666666;        /* Texto secundário */
--text-tertiary: #999999;         /* Texto terciário */
--border: #E0E0E0;                /* Bordas */
--border-light: #F0F0F0;          /* Bordas claras */
--shadow: rgba(0, 0, 0, 0.1);    /* Sombras */
--shadow-hover: rgba(0, 0, 0, 0.15); /* Sombras hover */
```

### Cores Neutras (Modo Escuro)

```css
--bg-dark: #1a1a2e;              /* Fundo principal escuro */
--bg-dark-secondary: #16213e;    /* Fundo secundário escuro */
--bg-dark-card: #0f3460;         /* Fundo de cards escuro */
--text-dark: #e0e0e0;            /* Texto principal escuro */
--text-dark-secondary: #b0b0b0;   /* Texto secundário escuro */
--border-dark: #0f3460;           /* Bordas escuras */
--shadow-dark: rgba(0, 0, 0, 0.3); /* Sombras escuras */
```

## 📝 Tipografia

### Família de Fontes

```css
--font-family-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
--font-family-mono: 'Courier New', Courier, monospace;
```

**Uso:**
- Primary: Texto geral, interface
- Mono: Código, valores numéricos, dados técnicos

### Tamanhos de Fonte

```css
--font-size-xs: 0.75rem;    /* 12px - Labels pequenos */
--font-size-sm: 0.875rem;   /* 14px - Texto secundário */
--font-size-base: 1rem;     /* 16px - Texto padrão */
--font-size-lg: 1.125rem;    /* 18px - Texto destacado */
--font-size-xl: 1.25rem;     /* 20px - Subtítulos */
--font-size-2xl: 1.5rem;     /* 24px - Títulos de seção */
--font-size-3xl: 1.875rem;   /* 30px - Títulos principais */
--font-size-4xl: 2.25rem;    /* 36px - Títulos grandes */
```

### Pesos de Fonte

```css
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Hierarquia Tipográfica

| Elemento | Tamanho | Peso | Uso |
|----------|--------|------|-----|
| H1 | 2.25rem (36px) | 700 | Títulos principais |
| H2 | 1.875rem (30px) | 600 | Títulos de seção |
| H3 | 1.5rem (24px) | 600 | Subtítulos |
| H4 | 1.25rem (20px) | 500 | Títulos de card |
| Body | 1rem (16px) | 400 | Texto padrão |
| Small | 0.875rem (14px) | 400 | Texto secundário |
| Caption | 0.75rem (12px) | 400 | Labels, captions |

## 📐 Espaçamentos e Grid

### Sistema de Espaçamento (8px base)

```css
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
--spacing-3xl: 4rem;     /* 64px */
```

### Grid System

```css
--grid-columns: 12;
--grid-gap: 1.5rem;      /* 24px */
--container-max-width: 1400px;
--sidebar-width: 250px;
--header-height: 70px;
```

### Breakpoints

```css
--breakpoint-xs: 0px;      /* Mobile */
--breakpoint-sm: 576px;    /* Mobile grande */
--breakpoint-md: 768px;    /* Tablet */
--breakpoint-lg: 992px;    /* Desktop */
--breakpoint-xl: 1200px;   /* Desktop grande */
--breakpoint-xxl: 1400px;  /* Desktop extra grande */
```

## 🧩 Componentes

### Botões

#### Botão Primário
```html
<button class="btn btn-primary">Ação Principal</button>
```

**Estados:**
- Default: Fundo roxo (#6A0DAD), texto branco
- Hover: Fundo roxo escuro (#4A0A7A)
- Active: Fundo roxo mais escuro
- Disabled: Opacidade 0.5, cursor not-allowed

#### Botão Secundário
```html
<button class="btn btn-secondary">Ação Secundária</button>
```

#### Botão Outline
```html
<button class="btn btn-outline-primary">Ação Outline</button>
```

### Cards

```html
<div class="dashboard-card">
    <h2>Título do Card</h2>
    <div class="card-content">
        Conteúdo do card
    </div>
</div>
```

**Características:**
- Fundo branco (modo claro) / #16213e (modo escuro)
- Sombra sutil: `box-shadow: 0 2px 8px rgba(0,0,0,0.1)`
- Border-radius: 8px
- Padding: 1.5rem
- Transição suave em hover

### Tabelas

```html
<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th>Coluna 1</th>
            <th>Coluna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dado 1</td>
            <td>Dado 2</td>
        </tr>
    </tbody>
</table>
```

**Características:**
- Linhas alternadas (zebra)
- Hover em linhas
- Cabeçalho destacado
- Bordas sutis

### Formulários

#### Input
```html
<input type="text" class="form-control" placeholder="Digite...">
```

#### Select
```html
<select class="form-control">
    <option>Opção 1</option>
</select>
```

**Estados:**
- Default: Borda cinza clara
- Focus: Borda roxa, sombra sutil
- Error: Borda vermelha
- Disabled: Fundo cinza claro, cursor not-allowed

### Badges

```html
<span class="badge bg-success">Sucesso</span>
<span class="badge bg-danger">Erro</span>
<span class="badge bg-warning">Aviso</span>
<span class="badge bg-info">Info</span>
```

### Loading Spinners

```html
<div class="spinner-border text-primary" role="status">
    <span class="visually-hidden">Carregando...</span>
</div>
```

## 🎭 Animações e Transições

### Durações Padrão

```css
--transition-fast: 150ms;
--transition-base: 250ms;
--transition-slow: 350ms;
--transition-slower: 500ms;
```

### Easing Functions

```css
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
```

### Animações Comuns

#### Fade In
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

#### Slide In
```css
@keyframes slideIn {
    from { transform: translateY(-10px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
```

#### Pulse
```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
```

## 🎯 Ícones

**Biblioteca:** Font Awesome 6 (Free)

**Uso:**
- Dashboard: `fa-chart-line`
- Finanças: `fa-dollar-sign`
- Estoque: `fa-box`
- Público-Alvo: `fa-users`
- Fornecedores: `fa-truck`
- RH: `fa-user-tie`

## 📱 Responsividade

### Mobile First

- Base: Mobile (< 576px)
- SM: Mobile grande (≥ 576px)
- MD: Tablet (≥ 768px)
- LG: Desktop (≥ 992px)
- XL: Desktop grande (≥ 1200px)

### Estratégias

- **Mobile:** Coluna única, menu hamburger, gráficos empilhados
- **Tablet:** 2 colunas, sidebar colapsável
- **Desktop:** Múltiplas colunas, sidebar sempre visível

## ♿ Acessibilidade

### Contraste

- Texto normal: Mínimo 4.5:1 (WCAG AA)
- Texto grande: Mínimo 3:1 (WCAG AA)
- Componentes interativos: Mínimo 3:1 (WCAG AA)

### Tamanhos Mínimos

- Texto: 16px mínimo
- Botões: 44x44px mínimo (touch target)
- Links: Área clicável adequada

### Navegação por Teclado

- Tab: Navegar entre elementos
- Enter/Space: Ativar botões
- Esc: Fechar modais
- Setas: Navegar em menus

## 🚀 Performance Visual

### Otimizações

- Uso de `transform` e `opacity` para animações (GPU)
- `will-change` apenas quando necessário
- Debounce em scroll e resize
- Lazy loading de imagens
- CSS crítico inline

### Métricas Alvo

- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- 60fps em animações
- Lighthouse Score: > 90

---

**Última atualização:** Fase 5 - Interface e UX

