import { test, expect } from "@playwright/test"

test("check the msg", async ({ page }) => {
    await page.goto("https://www.lambdatest.com/selenium-playground/simple-form-demo")
    let userMsg = page.getByPlaceholder("Please enter your Message")
    await userMsg.fill("Jafar Loka")
    console.log("The user msg: ", await userMsg.textContent())
    let showInput = page.locator("#showInput")
    await showInput.click()
    await page.waitForTimeout(1000)
    await showInput.click()
    console.log("Message is: ", await page.locator("#message").textContent())
    // expect(await page.locator("#message")).toHaveText("Jafar Loka")

    // await page.click("#sum1")
    let sum1Btn = page.locator("#sum1")
    await sum1Btn.fill('1')
    // await page.getByRole('textbox', { name: 'Please enter second value' }).click()
    let sum2Btn = page.locator('#sum2')
    await sum2Btn.fill('2')
    let resultBtn = page.getByRole('button', { name: 'Get Sum' })
    await resultBtn.click()
    console.log("The add msg is: ", await page.locator("#addmessage").textContent())
})

// test("Check sum", async ({ page }) => {
//     // await page.goto("https://www.lambdatest.com/selenium-playground/simple-form-demo")
// })