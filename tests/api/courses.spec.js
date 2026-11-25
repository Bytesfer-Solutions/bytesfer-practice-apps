const { test, expect } = require("@playwright/test");

test("GET /courses lists the 3 practice courses", async ({ request }) => {
  await request.post("/reset");
  const response = await request.get("/courses");
  expect(response.status()).toBe(200);
  const courses = await response.json();
  expect(courses).toHaveLength(3);
  for (const course of courses) {
    expect(Object.keys(course).sort()).toEqual(["fee", "id", "seats_left", "title"]);
  }
});
