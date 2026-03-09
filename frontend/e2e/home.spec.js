const { test, expect } = require('@playwright/test')

test.describe('home page', () => {
  test('renders and has links to create and jobs', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: /Otimização de Rotas Médicas/ })).toBeVisible()
    await expect(page.getByRole('link', { name: /Criar novo job/ })).toBeVisible()
    await expect(page.getByRole('link', { name: /Ver jobs/ })).toBeVisible()
  })
})
