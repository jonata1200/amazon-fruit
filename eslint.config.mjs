import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
// eslint-disable-next-line @typescript-eslint/no-require-imports
const tailwindcss = require("eslint-plugin-tailwindcss");

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Plugin Tailwind CSS
  {
    plugins: {
      tailwindcss,
    },
    rules: {
      // Regras do Tailwind CSS
      "tailwindcss/classnames-order": "warn",
      "tailwindcss/enforces-negative-arbitrary-values": "warn",
      "tailwindcss/enforces-shorthand": "warn",
      "tailwindcss/migration-from-tailwind-2": "warn",
      "tailwindcss/no-arbitrary-value": "off", // Permitir valores arbitrários quando necessário
      "tailwindcss/no-custom-classname": "off", // Permitir classes customizadas
      "tailwindcss/no-contradicting-classname": "error", // Erro para classes contraditórias
    },
  },
  // Regras específicas para design system
  {
    files: ["src/components/**/*.tsx", "src/lib/**/*.ts"],
    rules: {
      // Encorajar uso de design tokens
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],
    },
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Config files that use require()
    "jest.config.js",
    "jest.setup.js",
    "tailwind.config.ts",
    "next.config.ts",
    "postcss.config.mjs",
  ]),
]);

export default eslintConfig;
