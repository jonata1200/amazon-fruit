/**
 * Script de Validação de Design Tokens
 * Valida que todos os tokens estão corretos e consistentes
 */

import { tokens } from '../src/lib/design-tokens';
import { getColor, getSpacing, getTypography } from '../src/lib/utils/design-tokens';
import { meetsContrastRatio } from '../src/lib/utils/colors';

interface ValidationResult {
  passed: boolean;
  errors: string[];
  warnings: string[];
}

function validateTokens(): ValidationResult {
  const result: ValidationResult = {
    passed: true,
    errors: [],
    warnings: [],
  };

  // Validar cores
  try {
    const primaryColor = getColor('primary', 600);
    if (!primaryColor || !primaryColor.startsWith('#')) {
      result.errors.push('Cor primary.600 inválida');
      result.passed = false;
    }
  } catch (error) {
    result.errors.push(`Erro ao validar cores: ${error}`);
    result.passed = false;
  }

  // Validar espaçamento
  try {
    const spacing = getSpacing('md');
    if (!spacing || !spacing.includes('rem')) {
      result.errors.push('Espaçamento md inválido');
      result.passed = false;
    }
  } catch (error) {
    result.errors.push(`Erro ao validar espaçamento: ${error}`);
    result.passed = false;
  }

  // Validar tipografia
  try {
    const fontSize = getTypography('fontSize', 'base');
    if (!fontSize) {
      result.errors.push('Font size base inválido');
      result.passed = false;
    }
  } catch (error) {
    result.errors.push(`Erro ao validar tipografia: ${error}`);
    result.passed = false;
  }

  // Validar contraste de cores principais
  try {
    const primary = getColor('primary', 600);
    const white = '#ffffff';
    const black = '#000000';

    // Validar contraste básico
    if (!meetsContrastRatio(black, white, 'AA', 'normal')) {
      result.errors.push('Contraste preto/branco inválido');
      result.passed = false;
    }

    // Validar contraste de cores semânticas sobre branco
    const semanticColors: Array<{ name: string; color: string }> = [
      { name: 'primary', color: primary },
      { name: 'success', color: getColor('success', 600) },
      { name: 'error', color: getColor('error', 600) },
      { name: 'warning', color: getColor('warning', 600) },
      { name: 'info', color: getColor('info', 600) },
    ];

    semanticColors.forEach(({ name, color }) => {
      // Validar contraste para texto normal (AA)
      if (!meetsContrastRatio(color, white, 'AA', 'normal')) {
        result.warnings.push(
          `${name} sobre branco não atende WCAG AA para texto normal (mínimo 4.5:1)`
        );
      }

      // Validar contraste para texto grande (AA)
      if (!meetsContrastRatio(color, white, 'AA', 'large')) {
        result.warnings.push(
          `${name} sobre branco não atende WCAG AA para texto grande (mínimo 3:1)`
        );
      }

      // Validar contraste AAA (opcional, mas recomendado)
      if (!meetsContrastRatio(color, white, 'AAA', 'normal')) {
        result.warnings.push(
          `${name} sobre branco não atende WCAG AAA (recomendado 7:1 para texto normal)`
        );
      }
    });

    // Validar contraste de cores sobre fundos escuros (dark mode)
    const darkBackground = '#1a1a1a'; // Cor de fundo escuro típica
    semanticColors.forEach(({ name, color }) => {
      // Em dark mode, geralmente usamos cores mais claras
      const lightColor = getColor(name as any, 400);
      if (!meetsContrastRatio(lightColor, darkBackground, 'AA', 'normal')) {
        result.warnings.push(
          `${name} claro sobre fundo escuro não atende WCAG AA`
        );
      }
    });
  } catch (error) {
    result.warnings.push(`Não foi possível validar contraste: ${error}`);
  }

  return result;
}

// Executar validação
if (require.main === module) {
  const result = validateTokens();

  console.log('\n🔍 Validação de Design Tokens\n');

  if (result.errors.length > 0) {
    console.error('❌ Erros encontrados:');
    result.errors.forEach((error) => console.error(`  - ${error}`));
  }

  if (result.warnings.length > 0) {
    console.warn('⚠️  Avisos:');
    result.warnings.forEach((warning) => console.warn(`  - ${warning}`));
  }

  if (result.passed && result.errors.length === 0) {
    console.log('✅ Todos os tokens estão válidos!\n');
    process.exit(0);
  } else {
    console.error('\n❌ Validação falhou\n');
    process.exit(1);
  }
}

export { validateTokens };
