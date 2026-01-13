// src/lib/constants/index.ts

export const DASHBOARDS = [
  { id: 'geral', name: 'Visão Geral', icon: 'LineChart', path: '/geral' },
  { id: 'financas', name: 'Finanças', icon: 'DollarSign', path: '/financas' },
  { id: 'estoque', name: 'Estoque', icon: 'Package', path: '/estoque' },
  { id: 'publico-alvo', name: 'Público-Alvo', icon: 'Users', path: '/publico-alvo' },
  { id: 'fornecedores', name: 'Fornecedores', icon: 'Truck', path: '/fornecedores' },
  {
    id: 'recursos-humanos',
    name: 'Recursos Humanos',
    icon: 'UserTie',
    path: '/recursos-humanos',
  },
] as const;

export const ALERT_TYPES = {
  warning: { color: 'yellow', icon: 'AlertTriangle' },
  danger: { color: 'red', icon: 'XCircle' },
  info: { color: 'blue', icon: 'Info' },
  success: { color: 'green', icon: 'CheckCircle' },
} as const;

export const KEYBOARD_SHORTCUTS = {
  SEARCH: 'ctrl+f',
  THEME: 'ctrl+t',
  REPORT: 'ctrl+r',
  HELP: 'ctrl+?',
} as const;

export const API_CACHE_TIME = {
  SHORT: 60 * 1000, // 1 minuto
  MEDIUM: 5 * 60 * 1000, // 5 minutos
  LONG: 30 * 60 * 1000, // 30 minutos
  INFINITE: Infinity,
} as const;
