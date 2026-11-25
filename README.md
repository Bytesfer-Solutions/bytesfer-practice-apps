# Bytesfer practice apps

Small practice applications that Bytesfer learners test, by hand and with automation (UI, API and AI testing).
Each app lives in its own folder under `apps/` and runs in the browser, with no real server and no real payments.

## Apps

- `apps/course-shop/` (available): the Course Shop, a small course store with a cart, coupons, a test checkout,
  login and "My orders". Used by the Bytesfer course Test Design and QA Foundations.
- `apps/practice-api/` (available): a small local API for the API Testing with Python course.
- `apps/demo-shop/` (available): a tiny made-up shop (login and checkout) with a Playwright demo suite in `tests/`
  that runs in GitHub Actions on every pull request. See `tests/README.md`. It is separate from the Course Shop.

## Using an app

Each app's README will say how to open it and how to start from a clean state ("Reset shop").
Test only the practice apps in this repository, not third-party sites.

## Licence

MIT (see LICENSE).
