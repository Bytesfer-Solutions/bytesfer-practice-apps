const { test, expect } = require("@playwright/test");

test("a learner can add a course and pay at checkout", async ({ page }) => {
  await page.goto("/shop.html");
  await page.getByRole("button", { name: "Add API Testing with Python" }).click();
  await expect(page.locator("#cart-count")).toHaveText("1");
  await page.getByRole("button", { name: "Checkout" }).click();
  await expect(page.locator("#total")).toHaveText("999");
  const pay = page.locator("#pay");
  await expect(pay).toHaveText("Pay now");
  await pay.click();
  await expect(page.getByRole("status")).toHaveText("Payment received");
});
