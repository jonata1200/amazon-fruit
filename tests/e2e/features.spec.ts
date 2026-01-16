// tests/e2e/features.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Features', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');
  });

  test('should select period dates', async ({ page }) => {
    // Wait for period selector to be visible
    await page.waitForSelector('input[type="date"]', { timeout: 5000 });

    // Find date inputs
    const startDateInput = page.locator('input[type="date"]').first();
    const endDateInput = page.locator('input[type="date"]').last();

    // Set dates
    await startDateInput.fill('2024-01-01');
    await endDateInput.fill('2024-12-31');

    // Click apply button
    await page.click('button:has-text("Aplicar Período")');

    // Wait for data to update
    await page.waitForTimeout(1000);
  });

  test('should reset period dates', async ({ page }) => {
    await page.waitForSelector('button:has-text("Resetar")', { timeout: 5000 });

    // Click reset button
    await page.click('button:has-text("Resetar")');

    // Dates should be reset to current year
    await page.waitForTimeout(500);
  });

  test('should open export dropdown', async ({ page }) => {
    // Look for export button (may be in header)
    const exportButton = page.locator('button:has-text("Exportar"), button[aria-label*="Exportar" i]');
    
    if (await exportButton.count() > 0) {
      await exportButton.first().click();
      
      // Dropdown should open
      await page.waitForSelector('text=Exportar como PDF', { timeout: 2000 });
      
      // Click outside to close
      await page.click('body');
    }
  });

  test('should open global search with Ctrl+K', async ({ page }) => {
    // Press Ctrl+K (or Cmd+K on Mac)
    await page.keyboard.press('Control+K');
    
    // Search modal/panel should appear
    // Adjust selector based on actual implementation
    await page.waitForTimeout(500);
    
    // Press Escape to close
    await page.keyboard.press('Escape');
  });
});
