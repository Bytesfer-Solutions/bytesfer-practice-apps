// Demo suite for Bytesfer's public practice apps: UI tests for apps/demo-shop and API tests for apps/practice-api.
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "tests",
  workers: 1,                                  // the API tests share one practice server
  retries: process.env.CI ? 1 : 0,
  reporter: [["html", { open: "never" }], ["list"]],
  use: { trace: "on-first-retry", screenshot: "only-on-failure" },
  projects: [
    {
      name: "ui",
      testDir: "tests/ui",
      // On your computer you can use your installed Chrome: PW_CHANNEL=chrome npx playwright test
      use: { ...devices["Desktop Chrome"], baseURL: "http://127.0.0.1:4321", channel: process.env.PW_CHANNEL },
    },
    {
      name: "api",
      testDir: "tests/api",
      use: { baseURL: "http://127.0.0.1:8000" },
    },
  ],
  webServer: [
    {
      command: "python3 apps/practice-api/serve.py 8000",
      url: "http://127.0.0.1:8000/courses",
      reuseExistingServer: false,
    },
    {
      command: "python3 -m http.server 4321 --bind 127.0.0.1 --directory apps/demo-shop",
      url: "http://127.0.0.1:4321/login.html",
      reuseExistingServer: false,
    },
  ],
});
