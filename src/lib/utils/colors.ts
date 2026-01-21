/**
 * Utilitários de Cores
 * Funções para manipulação e transformação de cores
 */

import { getColor } from './design-tokens';
import type { ColorName, ColorScale } from '@/lib/design-tokens/types';

/**
 * Adiciona opacidade a uma cor hex
 * @param hex - Cor em formato hex (#RRGGBB)
 * @param opacity - Opacidade (0-1)
 * @returns Cor com opacidade em formato rgba
 */
export function addOpacity(hex: string, opacity: number): string {
  const hexWithoutHash = hex.replace('#', '');
  const r = parseInt(hexWithoutHash.substring(0, 2), 16);
  const g = parseInt(hexWithoutHash.substring(2, 4), 16);
  const b = parseInt(hexWithoutHash.substring(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

/**
 * Obtém cor com opacidade do design system
 * @param name - Nome da cor
 * @param scale - Escala da cor
 * @param opacity - Opacidade (0-1)
 * @returns Cor com opacidade
 */
export function getColorWithOpacity(
  name: ColorName,
  scale: ColorScale = 600,
  opacity: number = 1
): string {
  const color = getColor(name, scale);
  return addOpacity(color, opacity);
}

/**
 * Calcula o contraste entre duas cores (WCAG)
 * @param color1 - Primeira cor (hex)
 * @param color2 - Segunda cor (hex)
 * @returns Razão de contraste
 */
export function getContrastRatio(color1: string, color2: string): number {
  const getLuminance = (hex: string): number => {
    const hexWithoutHash = hex.replace('#', '');
    const r = parseInt(hexWithoutHash.substring(0, 2), 16) / 255;
    const g = parseInt(hexWithoutHash.substring(2, 4), 16) / 255;
    const b = parseInt(hexWithoutHash.substring(4, 6), 16) / 255;

    const [rLinear, gLinear, bLinear] = [r, g, b].map((val) => {
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * rLinear + 0.7152 * gLinear + 0.0722 * bLinear;
  };

  const lum1 = getLuminance(color1);
  const lum2 = getLuminance(color2);

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Verifica se o contraste atende aos requisitos WCAG
 * @param foreground - Cor do texto
 * @param background - Cor do fundo
 * @param level - Nível WCAG ('AA' ou 'AAA')
 * @param size - Tamanho do texto ('normal' ou 'large')
 * @returns true se o contraste é adequado
 */
export function meetsContrastRatio(
  foreground: string,
  background: string,
  level: 'AA' | 'AAA' = 'AA',
  size: 'normal' | 'large' = 'normal'
): boolean {
  const ratio = getContrastRatio(foreground, background);
  
  if (level === 'AAA') {
    return size === 'large' ? ratio >= 4.5 : ratio >= 7;
  }
  
  return size === 'large' ? ratio >= 3 : ratio >= 4.5;
}

/**
 * Obtém cor de texto adequada baseada na cor de fundo
 * @param backgroundColor - Cor de fundo
 * @param lightText - Cor de texto para fundo escuro
 * @param darkText - Cor de texto para fundo claro
 * @returns Cor de texto adequada
 */
export function getTextColor(
  backgroundColor: string,
  lightText: string = '#ffffff',
  darkText: string = '#000000'
): string {
  const whiteContrast = getContrastRatio(lightText, backgroundColor);
  const blackContrast = getContrastRatio(darkText, backgroundColor);
  
  return whiteContrast > blackContrast ? lightText : darkText;
}

/**
 * Converte hex para RGB
 * @param hex - Cor em formato hex
 * @returns Objeto com valores RGB
 */
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

/**
 * Converte RGB para hex
 * @param r - Valor red (0-255)
 * @param g - Valor green (0-255)
 * @param b - Valor blue (0-255)
 * @returns Cor em formato hex
 */
export function rgbToHex(r: number, g: number, b: number): string {
  return `#${[r, g, b].map((x) => x.toString(16).padStart(2, '0')).join('')}`;
}

/**
 * Converte hex para HSL
 * @param hex - Cor em formato hex
 * @returns Objeto com valores HSL
 */
export function hexToHsl(hex: string): { h: number; s: number; l: number } | null {
  const rgb = hexToRgb(hex);
  if (!rgb) return null;

  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }
  }

  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100),
  };
}

/**
 * Gera uma paleta de cores baseada em uma cor primária
 * @param baseColor - Cor base em formato hex
 * @returns Objeto com paleta de cores (50-950)
 */
export function generateColorPalette(baseColor: string): Record<number, string> {
  const hsl = hexToHsl(baseColor);
  if (!hsl) {
    throw new Error('Cor inválida. Use formato hex (#RRGGBB)');
  }

  const { h, s } = hsl;
  const palette: Record<number, string> = {};

  // Escala de luminosidade para cada nível
  const lightnessMap: Record<number, number> = {
    50: 95,
    100: 90,
    200: 80,
    300: 70,
    400: 60,
    500: 50,
    600: 40,
    700: 30,
    800: 20,
    900: 15,
    950: 10,
  };

  // Ajustar saturação para tons mais claros e escuros
  const saturationMap: Record<number, number> = {
    50: Math.max(0, s - 20),
    100: Math.max(0, s - 15),
    200: Math.max(0, s - 10),
    300: Math.max(0, s - 5),
    400: s,
    500: s,
    600: Math.min(100, s + 5),
    700: Math.min(100, s + 10),
    800: Math.min(100, s + 15),
    900: Math.min(100, s + 20),
    950: Math.min(100, s + 25),
  };

  // Gerar cada nível da paleta
  for (const [level, lightness] of Object.entries(lightnessMap)) {
    const levelNum = parseInt(level);
    const saturation = saturationMap[levelNum];
    
    // Converter HSL para RGB e depois para hex
    const rgb = hslToRgb(h, saturation, lightness);
    palette[levelNum] = rgbToHex(rgb.r, rgb.g, rgb.b);
  }

  return palette;
}

/**
 * Converte HSL para RGB
 * @param h - Matiz (0-360)
 * @param s - Saturação (0-100)
 * @param l - Luminosidade (0-100)
 * @returns Objeto com valores RGB
 */
function hslToRgb(h: number, s: number, l: number): { r: number; g: number; b: number } {
  s /= 100;
  l /= 100;

  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;

  let r = 0;
  let g = 0;
  let b = 0;

  if (h >= 0 && h < 60) {
    r = c;
    g = x;
    b = 0;
  } else if (h >= 60 && h < 120) {
    r = x;
    g = c;
    b = 0;
  } else if (h >= 120 && h < 180) {
    r = 0;
    g = c;
    b = x;
  } else if (h >= 180 && h < 240) {
    r = 0;
    g = x;
    b = c;
  } else if (h >= 240 && h < 300) {
    r = x;
    g = 0;
    b = c;
  } else if (h >= 300 && h < 360) {
    r = c;
    g = 0;
    b = x;
  }

  return {
    r: Math.round((r + m) * 255),
    g: Math.round((g + m) * 255),
    b: Math.round((b + m) * 255),
  };
}
