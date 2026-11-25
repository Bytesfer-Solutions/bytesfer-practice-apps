const { test, expect } = require("@playwright/test");

async function login(request, username, password) {
  const response = await request.post("/login", { data: { username, password } });
  expect(response.status()).toBe(200);
  return { Authorization: "Bearer " + (await response.json()).token };
}

test("the last seat goes to the first learner, then the batch is full", async ({ request }) => {
  await request.post("/reset");
  const meera = await login(request, "meera", "learn-123");
  const arjun = await login(request, "arjun", "learn-456");
  const first = await request.post("/enrolments", { data: { course_id: 2 }, headers: meera });
  expect(first.status()).toBe(201);
  const second = await request.post("/enrolments", { data: { course_id: 2 }, headers: arjun });
  expect(second.status()).toBe(422);
  expect((await second.json()).error).toBe("This batch is full.");
});
