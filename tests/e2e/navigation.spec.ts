// tests/e2e/navigation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should navigate between dashboards via sidebar', async ({ page }) => {
    // Wait for sidebar to be visible
    await page.waitForSelector('aside nav', { timeout: 5000 });

    // Click on Finanças dashboard
    await page.click('text=Finanças');
    await expect(page).toHaveURL(/.*\/financas/);
    await expect(page.locator('h1, h2')).toContainText(/finanças/i);

    // Click on Estoque dashboard
    await page.click('text=Estoque');
    await expect(page).toHaveURL(/.*\/estoque/);
    await expect(page.locator('h1, h2')).toContainText(/estoque/i);

    // Click on Público-Alvo dashboard
    await page.click('text=Público-Alvo');
    await expect(page).toHaveURL(/.*\/publico-alvo/);

    // Click on Geral dashboard
    await page.click('text=Visão Geral');
    await expect(page).toHaveURL(/.*\/geral/);
  });

  test('should navigate via keyboard', async ({ page }) => {
    await page.waitForSelector('aside nav', { timeout: 5000 });

    // Skip to main content
    await page.keyboard.press('Tab');
    const skipLink = page.locator('a[href="#main-content"]');
    if (await skipLink.isVisible()) {
      await skipLink.press('Enter');
    }

    // Use keyboard to navigate sidebar
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Navigate through menu items
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/.*\/geral/);
  });

  test('should have accessible skip link', async ({ page }) => {
    // Skip link should be hidden but focusable
    const skipLink = page.locator('a[href="#main-content"]');
    await expect(skipLink).toHaveClass(/sr-only/);
    
    // Tab to make it visible
    await page.keyboard.press('Tab');
    await expect(skipLink).toBeVisible();
    
    // Should navigate to main content
    await skipLink.press('Enter');
    const mainContent = page.locator('#main-content');
    await expect(mainContent).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Sidebar should be hidden on mobile
    const sidebar = page.locator('aside');
    const sidebarClasses = await sidebar.getAttribute('class');
    expect(sidebarClasses).toContain('-translate-x-full');
  });
});
