/**
 * Design Tokens - Sistema de Z-Index
 * Camadas bem definidas para evitar conflitos
 */

export const zIndex = {
  hide: -1,
  auto: 'auto',
  base: 0,
  docked: 10,
  dropdown: 1000,
  sticky: 1100,
  banner: 1200,
  overlay: 1300,
  modal: 1400,
  popover: 1500,
  skipLink: 1600,
  tooltip: 1700,
} as const;

// Z-index para componentes específicos
export const componentZIndex = {
  sidebar: zIndex.docked,
  header: zIndex.sticky,
  dropdown: zIndex.dropdown,
  tooltip: zIndex.tooltip,
  modal: zIndex.modal,
  popover: zIndex.popover,
  overlay: zIndex.overlay,
  banner: zIndex.banner,
  skipLink: zIndex.skipLink,
} as const;
