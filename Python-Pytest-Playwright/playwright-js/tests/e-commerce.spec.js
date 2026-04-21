import { test, expect } from '@playwright/test'

test('check cart icon', async ({ page }) => {
    await page.goto('https://ecommerce-playground.lambdatest.io/')
    await page.locator('span.title', {hasText: ' Mega Menu'}).hover()
    await page.locator('a[title="Desktop"]').click();
    let t1 = page.locator('div.carousel-item.active > img[title="Palm Treo Pro"]')
    
    await t1.scrollIntoViewIfNeeded()
    await t1.hover()
    await page.waitForTimeout(1000)

    let t2 = page.locator('button[title="Add to Cart"]').nth(1)
    await expect(t2).toBeVisible()    
})