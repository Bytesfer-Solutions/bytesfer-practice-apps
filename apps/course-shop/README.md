# Course Shop (practice app)

A small practice web shop for testing. It has 7 courses, a cart with a coupon box, a checkout with a test payment
("Pay: Success" / "Pay: Fail"), a login page and "My orders". No real server, no real money.

## Open it

Serve this folder over HTTP and open `index.html` (a service worker needs `http://localhost` or https; `file://` does not work):

    python3 -m http.server 8080 --bind 127.0.0.1

Then open http://127.0.0.1:8080/apps/course-shop/ . The first load installs the shop's server (a service worker);
the page starts by itself. Its data lives in your browser (IndexedDB).

## Test logins

- asha@example.com / Shop@1234 (mobile 9000000001): has the preset orders
- ravi@example.com / Shop@1234 (mobile 9000000002): a second learner, for the "not your order" (403) case
- finance@example.com / Shop@1234: the finance login. It sees the "Finance: mark refunded" list on My orders and can mark a Refund requested order as Refunded. Learners cannot.

## Reset shop

The footer has a **Reset shop** button. It restores the shop clock and all data to the starting state: the two learners,
their past orders (paid on 2, 3 and 4 Nov 2026, one Payment pending, one Payment failed), an empty cart.

## Shop clock

"Today" is fixed at **9 Nov 2026, 10:00 IST**. It does not tick. The footer shows it, with **+15 min** and **+1 day** buttons.
Reset shop sets it back.

## Server (API)

The shop's server answers `/api/...` inside the browser, with real status codes and JSON (see the Network tab):
`/api/cart`, `/api/coupon`, `/api/checkout`, `/api/login`, `/api/orders`, `/api/orders/{id}`.
Order ids look like CS-1042. Requests that need a login send `Authorization: Bearer <token>` (the token is returned by `POST /api/login`).

Practice controls (not part of the shop rules): `GET /api/courses` lists the catalogue, `GET /api/clock` and `POST /api/clock` read and move the shop clock, `POST /api/reset` is what the Reset shop button calls.

## Licence

MIT (see LICENSE).
