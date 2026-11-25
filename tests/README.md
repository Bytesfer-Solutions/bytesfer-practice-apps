# Demo Playwright suite

UI tests for `apps/demo-shop`, a small demo shop: log in, add a course, pay (no real payment). API tests for `apps/practice-api`, the enrolment API from "API Testing with Python". All data is made up. The suite runs in GitHub Actions on every pull request and on every push to main.

`apps/demo-shop` is separate from `apps/course-shop`, the Course Shop used by "Test Design and QA Foundations"; this suite does not touch it.

## Run it on your computer
You need Node.js 22 and Python 3.12 or newer. From the repository root:
```
npm ci
npx playwright install chromium        (or use your installed Chrome: see below)
npx playwright test
npx playwright show-report             (opens the HTML report)
```
To use the Chrome already on your computer instead of downloading Chromium: `PW_CHANNEL=chrome npx playwright test`.

Playwright starts both practice servers itself (the API on port 8000, the demo shop on port 4321) and stops them when the run ends.

## The tests
| File | What it checks |
|---|---|
| `tests/ui/login.spec.js` | The right login shows "Welcome, Meera"; a wrong password shows the error |
| `tests/ui/checkout.spec.js` | Add a course; the checkout total is ₹999; the button reads "Pay now"; paying shows "Payment received" |
| `tests/api/courses.spec.js` | `GET /courses` returns 200 and 3 courses with the expected keys |
| `tests/api/enrol.spec.js` | The last seat in course 2 goes to meera (201); arjun then gets 422 "This batch is full." |

## Verified by real runs (25 Nov 2026; @playwright/test 1.65.0, local Chrome, macOS)
- `npm ci` from the lock file: 3 packages, Playwright 1.65.0.
- **Run 1, unchanged app:** 5 passed, exit code 0.
- **Run 2, the demo shop's button changed from "Pay now" to "Pay", with `CI=1`:**
  - `checkout.spec.js` failed on the run and on the retry with `Expected: "Pay now"` / `Received: "Pay"`.
  - The other 4 tests passed; the exit code was 1.
  - A screenshot was taken on failure, and a trace on the retry.
- **HTML report:** opened in Chrome. It shows All 5, Passed 4, Failed 1. The failed test shows Expected and Received and a screenshot; the Retry #1 tab has a Traces section.
- **Clean-up:** after each run nothing was listening on ports 8000 or 4321, and no server or browser process was left running.
- **Not run here:** the GitHub Actions workflow itself, which runs on the first push. Its YAML parses.
