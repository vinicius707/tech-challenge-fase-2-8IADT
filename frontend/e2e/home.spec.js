const { test, expect } = require('@playwright/test')

test.describe('home page', () => {
  test('renders and has links to create and jobs', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: /Bem-vindo ao Sistema de Distribuição/ })).toBeVisible()
    await expect(page.getByText(/Nova Rota/)).toBeVisible()
    await expect(page.getByText(/Ver Histórico/)).toBeVisible()
  })
})
