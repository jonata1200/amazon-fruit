// tests/e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('should have no accessibility violations on dashboard geral', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should have visible focus indicators', async ({ page }) => {
    await page.goto('/geral');
    
    // Tab through interactive elements
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');

    // Check if focused element has visible outline
    const focusedElement = page.locator(':focus');
    if (await focusedElement.count() > 0) {
      const outline = await focusedElement.evaluate((el) => {
        const styles = window.getComputedStyle(el);
        return styles.outline || styles.boxShadow;
      });
      
      expect(outline).not.toBe('none');
      expect(outline).not.toBe('');
    }
  });

  test('should have proper ARIA labels on icon-only buttons', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');

    // Find icon-only buttons
    const iconButtons = page.locator('button:has(svg):not(:has-text()))');
    const count = await iconButtons.count();

    if (count > 0) {
      // Check first icon button has aria-label
      const firstButton = iconButtons.first();
      const ariaLabel = await firstButton.getAttribute('aria-label');
      expect(ariaLabel).toBeTruthy();
    }
  });

  test('should have proper heading hierarchy', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');

    // Check for main heading (h1 or h2)
    const h1 = page.locator('h1');
    const h2 = page.locator('h2');
    
    const hasHeading = (await h1.count() > 0) || (await h2.count() > 0);
    expect(hasHeading).toBeTruthy();
  });

  test('should have accessible form inputs', async ({ page }) => {
    await page.goto('/geral');
    await page.waitForLoadState('networkidle');

    // Check date inputs have labels
    const dateInputs = page.locator('input[type="date"]');
    const inputCount = await dateInputs.count();

    if (inputCount > 0) {
      const firstInput = dateInputs.first();
      const id = await firstInput.getAttribute('id');
      
      if (id) {
        const label = page.locator(`label[for="${id}"]`);
        await expect(label).toBeVisible();
      }
    }
  });
});
