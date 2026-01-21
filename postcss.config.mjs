const config = {
  plugins: {
    "@tailwindcss/postcss": {
      // Otimizações para produção
      ...(process.env.NODE_ENV === 'production' && {
        // Minificação já é feita automaticamente pelo Next.js
      }),
    },
  },
};

export default config;
