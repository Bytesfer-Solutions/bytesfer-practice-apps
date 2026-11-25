const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("/login.html");
});

test("the right email and password show the welcome heading", async ({ page }) => {
  await page.getByLabel("Email").fill("meera@example.com");
  await page.getByLabel("Password").fill("learn-123");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page.getByRole("heading", { name: "Welcome, Meera" })).toBeVisible();
});

test("a wrong password shows an error", async ({ page }) => {
  await page.getByLabel("Email").fill("meera@example.com");
  await page.getByLabel("Password").fill("wrong");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page.getByRole("alert")).toHaveText("Wrong email or password.");
});
