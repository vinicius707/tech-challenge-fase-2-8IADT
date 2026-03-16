const { test, expect } = require('@playwright/test')

test.describe('navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should navigate to Planejar Rota', async ({ page }) => {
    await page.getByRole('button', { name: 'Planejar Rota' }).click()
    await expect(page).toHaveURL(/\/create/)
    await expect(page.getByRole('heading', { name: /Planejar rota de distribuição/i })).toBeVisible()
  })

  test('should navigate to Histórico', async ({ page }) => {
    await page.getByRole('button', { name: 'Histórico' }).click()
    await expect(page).toHaveURL(/\/jobs/)
    await expect(page.getByRole('heading', { name: /Planejamentos de rotas/i })).toBeVisible()
  })

  test('should navigate to Endereços', async ({ page }) => {
    await page.getByRole('button', { name: 'Endereços' }).click()
    await expect(page).toHaveURL(/\/locations/)
    await expect(page.getByRole('heading', { name: /Endereços \/ Hospitais/i })).toBeVisible()
  })

  test('should navigate to Veículos', async ({ page }) => {
    await page.getByRole('button', { name: 'Veículos' }).click()
    await expect(page).toHaveURL(/\/vehicles/)
    await expect(page.getByRole('heading', { name: /Veículos Cadastrados/i })).toBeVisible()
  })
})
