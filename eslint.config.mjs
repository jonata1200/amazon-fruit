import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
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
