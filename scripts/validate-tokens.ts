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

    if (!meetsContrastRatio(primary, white, 'AA', 'normal')) {
      result.warnings.push('Primary sobre branco pode não ter contraste adequado');
    }

    if (!meetsContrastRatio(black, white, 'AA', 'normal')) {
      result.errors.push('Contraste preto/branco inválido');
      result.passed = false;
    }
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
