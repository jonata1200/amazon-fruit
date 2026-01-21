/**
 * Tailwind CSS - Plugins Customizados
 * Plugins para design tokens, utilitários e componentes comuns
 */

// eslint-disable-next-line @typescript-eslint/no-require-imports
const plugin = require('tailwindcss/plugin') as typeof import('tailwindcss/plugin').default;

/**
 * Plugin para design tokens
 * Adiciona utilitários baseados nos design tokens
 */
export const designTokensPlugin = plugin(
  function ({ addUtilities, theme }) {
    // Utilitários para design tokens de espaçamento semântico
    addUtilities({
      '.spacing-xs': { gap: theme('spacing.1') },
      '.spacing-sm': { gap: theme('spacing.2') },
      '.spacing-md': { gap: theme('spacing.4') },
      '.spacing-lg': { gap: theme('spacing.6') },
      '.spacing-xl': { gap: theme('spacing.8') },
    });

    // Utilitários para elevação baseados em design tokens
    addUtilities({
      '.elevation-0': { boxShadow: theme('boxShadow.none') },
      '.elevation-1': { boxShadow: theme('boxShadow.sm') },
      '.elevation-2': { boxShadow: theme('boxShadow.base') },
      '.elevation-3': { boxShadow: theme('boxShadow.md') },
      '.elevation-4': { boxShadow: theme('boxShadow.lg') },
      '.elevation-5': { boxShadow: theme('boxShadow.xl') },
    });
  },
  {
    theme: {
      extend: {},
    },
  }
);

/**
 * Plugin para utilitários comuns
 * Utilitários reutilizáveis para layouts e componentes
 */
export const utilitiesPlugin = plugin(
  function ({ addUtilities, theme }) {
    addUtilities({
      // Container com max-width responsivo
      '.container-responsive': {
        width: '100%',
        marginLeft: 'auto',
        marginRight: 'auto',
        paddingLeft: theme('spacing.4'),
        paddingRight: theme('spacing.4'),
        '@screen sm': {
          maxWidth: theme('screens.sm'),
        },
        '@screen md': {
          maxWidth: theme('screens.md'),
        },
        '@screen lg': {
          maxWidth: theme('screens.lg'),
        },
        '@screen xl': {
          maxWidth: theme('screens.xl'),
        },
        '@screen 2xl': {
          maxWidth: theme('screens.2xl'),
        },
      },
      // Text balance (melhora legibilidade)
      '.text-balance': {
        textWrap: 'balance',
      },
      // Scrollbar styling
      '.scrollbar-thin': {
        scrollbarWidth: 'thin',
        '&::-webkit-scrollbar': {
          width: '8px',
          height: '8px',
        },
        '&::-webkit-scrollbar-track': {
          background: 'transparent',
        },
        '&::-webkit-scrollbar-thumb': {
          backgroundColor: theme('colors.muted.DEFAULT'),
          borderRadius: theme('borderRadius.full'),
        },
      },
      // Focus visible melhorado
      '.focus-ring': {
        '&:focus-visible': {
          outline: `2px solid ${theme('colors.ring')}`,
          outlineOffset: '2px',
        },
      },
      // Truncate com ellipsis
      '.truncate-2': {
        overflow: 'hidden',
        display: '-webkit-box',
        WebkitBoxOrient: 'vertical',
        WebkitLineClamp: '2',
      },
      '.truncate-3': {
        overflow: 'hidden',
        display: '-webkit-box',
        WebkitBoxOrient: 'vertical',
        WebkitLineClamp: '3',
      },
    });
  },
  {
    theme: {
      extend: {},
    },
  }
);

/**
 * Plugin para animações customizadas
 * Animações baseadas em design tokens
 */
export const animationsPlugin = plugin(
  function ({ addUtilities, theme }) {
    addUtilities({
      // Animações de fade
      '.animate-fade-in': {
        animation: `fade-in ${theme('transitionDuration.base')} ${theme('transitionTimingFunction.out')}`,
      },
      '.animate-fade-out': {
        animation: `fade-out ${theme('transitionDuration.base')} ${theme('transitionTimingFunction.in')}`,
      },
      // Animações de slide
      '.animate-slide-up': {
        animation: `slide-up ${theme('transitionDuration.base')} ${theme('transitionTimingFunction.out')}`,
      },
      '.animate-slide-down': {
        animation: `slide-down ${theme('transitionDuration.base')} ${theme('transitionTimingFunction.out')}`,
      },
      // Animações de scale
      '.animate-scale-in': {
        animation: `scale-in ${theme('transitionDuration.base')} ${theme('transitionTimingFunction.spring')}`,
      },
    });
  },
  {
    theme: {
      extend: {
        keyframes: {
          'fade-in': {
            '0%': { opacity: '0' },
            '100%': { opacity: '1' },
          },
          'fade-out': {
            '0%': { opacity: '1' },
            '100%': { opacity: '0' },
          },
          'slide-up': {
            '0%': { transform: 'translateY(10px)', opacity: '0' },
            '100%': { transform: 'translateY(0)', opacity: '1' },
          },
          'slide-down': {
            '0%': { transform: 'translateY(-10px)', opacity: '0' },
            '100%': { transform: 'translateY(0)', opacity: '1' },
          },
          'scale-in': {
            '0%': { transform: 'scale(0.95)', opacity: '0' },
            '100%': { transform: 'scale(1)', opacity: '1' },
          },
        },
      },
    },
  }
);

/**
 * Plugin consolidado - exporta todos os plugins
 */
export const customPlugins = [designTokensPlugin, utilitiesPlugin, animationsPlugin];
