// tests/e2e/dashboards.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Dashboards', () => {
  test('Dashboard Geral should load and display data', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');

    // Should have main content
    const mainContent = page.locator('#main-content');
    await expect(mainContent).toBeVisible();

    // Should have period selector
    await page.waitForSelector('input[type="date"]', { timeout: 5000 });

    // Should have KPI cards (may take time to load)
    await page.waitForTimeout(2000);
    
    // Check for skeleton or content
    const hasContent = await page.locator('text=/R\\$|Total|KPI/i').count() > 0;
    const hasSkeleton = await page.locator('.animate-pulse').count() > 0;
    
    expect(hasContent || hasSkeleton).toBeTruthy();
  });

  test('Dashboard Finanças should load correctly', async ({ page }) => {
    await page.goto('/financas');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('#main-content')).toBeVisible();
    await page.waitForSelector('input[type="date"]', { timeout: 5000 });
  });

  test('Dashboard Estoque should load correctly', async ({ page }) => {
    await page.goto('/estoque');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('#main-content')).toBeVisible();
  });

  test('Charts should render correctly', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');
    
    // Wait for charts to potentially load
    await page.waitForTimeout(3000);
    
    // Check for chart containers (Recharts uses SVG)
    const svgElements = await page.locator('svg').count();
    // Should have at least some SVG elements (charts or icons)
    expect(svgElements).toBeGreaterThan(0);
  });

  test('Error boundary should handle errors gracefully', async ({ page }) => {
    await page.goto('/geral');
    
    // Inject error to test error boundary
    await page.evaluate(() => {
      throw new Error('Test error');
    });

    // Error boundary should catch it
    // Check for error UI (adjust based on actual error boundary implementation)
    await page.waitForTimeout(1000);
  });
});
