const { chromium } = require("playwright");
const fs = require("fs"),
  assert = require("assert");
let browser;
(async () => {
  browser = await chromium.launch({ channel: "chrome", headless: true });
  const ctx = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
    }),
    page = await ctx.newPage();
  const checks = [],
    errors = [],
    calls = [],
    audits = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (r.url().endsWith("/ui/chat")) calls.push(JSON.parse(r.postData()));
  });
  async function send(q) {
    const n = await page.locator(".message-assistant").count();
    await page.locator("#message-input").fill(q);
    await page.locator("#send-button").click();
    await page.waitForFunction(
      (n) => document.querySelectorAll(".message-assistant").length === n,
      n + 1,
    );
    await page.waitForFunction(
      () => !document.querySelector("#message-input").readOnly,
    );
  }
  async function settled(n) {
    await page.waitForFunction(
      (n) =>
        document.querySelectorAll("#sidebar-history-list .history-row")
          .length === n,
      n,
    );
  }
  async function audit(name) {
    await page.evaluate(
      fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8"),
    );
    const r = await page.evaluate(() =>
      axe.run(document, {
        runOnly: {
          type: "tag",
          values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"],
        },
      }),
    );
    audits.push({
      name,
      violations: r.violations.map((v) => ({
        id: v.id,
        nodes: v.nodes.map((n) => n.target),
      })),
    });
  }
  await page.goto("http://127.0.0.1:8002", { waitUntil: "networkidle" });
  assert(!(await page.locator(".sidebar-history").isVisible()));
  checks.push("saved conversations stay hidden before demo access");
  await page.locator("#access-code").fill("preview-demo-code");
  await page.locator("#access-submit").click();
  await page.locator("#chat-view").waitFor({ state: "visible" });
  assert(await page.locator(".sidebar-history").isVisible());
  assert(await page.locator("#sidebar-history-empty").isVisible());
  checks.push(
    "desktop exposes sidebar history and truthful empty/storage state",
  );
  await page.locator('[data-action="history-settings"]').click();
  await page.locator("#remember-history").check();
  await page.waitForFunction(() => BobalabHistoryStore.enabled());
  await page.locator('[data-close="history-dialog"]').click();
  await send("First planning question.");
  await settled(1);
  assert.equal(
    await page.locator('#sidebar-history-list [aria-current="true"]').count(),
    1,
  );
  checks.push(
    "completed saved reply appears with active conversation highlight",
  );
  await page.locator(".sidebar-new").click();
  await page.locator("#confirm-reset").click();
  await send("Second planning question.");
  await settled(2);
  await page
    .locator("#sidebar-history-list .history-open", {
      hasText: "First planning question.",
    })
    .click();
  await page.waitForFunction(
    () =>
      document.querySelector(".message-user")?.textContent ===
      "First planning question.",
  );
  await send("First plan follow-up.");
  assert.equal(calls.at(-1).chatHistory.length, 2);
  assert.equal(calls.at(-1).chatHistory[0].message, "First planning question.");
  checks.push(
    "sidebar reopens selected conversation and only its context is sent",
  );
  await page.locator("#sidebar-history-search").fill("First plan follow-up");
  await settled(1);
  assert(
    (
      await page.locator("#sidebar-history-list .history-open").textContent()
    ).includes("First"),
  );
  await page.locator("#sidebar-history-search").fill("");
  await settled(2);
  checks.push("sidebar search matches stored message text");
  await page.locator("#message-input").fill("Keep this draft.");
  await page
    .locator("#sidebar-history-list .history-open", {
      hasText: "Second planning question.",
    })
    .click();
  await page.locator("#history-confirm-no").click();
  assert.equal(
    await page.locator("#message-input").inputValue(),
    "Keep this draft.",
  );
  checks.push(
    "switching from an unsaved draft requires confirmation and cancel preserves it",
  );
  await page.locator("#message-input").fill("");
  const first = page
    .locator("#sidebar-history-list .history-row")
    .filter({ hasText: "First planning question." });
  await first.locator(".history-action", { hasText: "Rename" }).click();
  await page.locator("#rename-title").fill("First plan reviewed");
  await page.locator('#rename-form button[type="submit"]').click();
  await page.locator("#rename-dialog").waitFor({ state: "hidden" });
  assert.equal(
    await page
      .locator("#sidebar-history-list .history-open", {
        hasText: "First plan reviewed",
      })
      .count(),
    1,
  );
  checks.push("sidebar rename updates the shared saved record");
  await audit("desktop active sidebar");
  await page.screenshot({ path: "work/sidebar-desktop.png" });
  for (const [w, h] of [
    [1280, 800],
    [1024, 768],
    [768, 1024],
    [390, 844],
    [360, 740],
  ]) {
    await page.setViewportSize({ width: w, height: h });
    await page.waitForTimeout(100);
    assert(
      !(await page.evaluate(
        () => document.documentElement.scrollWidth > innerWidth,
      )),
    );
    assert((await page.locator("#send-button").boundingBox()).y < h);
  }
  checks.push(
    "desktop tablet and mobile layouts fit without horizontal page overflow",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.locator('[data-action="history"]').first().click();
  const box = await page.locator("#history-dialog").boundingBox();
  assert(box.x < 1 && box.width < 390);
  await audit("mobile conversation drawer");
  await page.screenshot({ path: "work/sidebar-mobile-drawer.png" });
  await page.keyboard.press("Escape");
  assert(!(await page.locator("#history-dialog").isVisible()));
  checks.push("mobile uses a left drawer with keyboard dismissal");
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.evaluate(async () => {
    const r = (await BobalabHistoryStore.list()).find(
      (r) => r.title === "First plan reviewed",
    );
    r.messages.push(
      {
        role: "client",
        message: "Other tab only.",
        at: new Date().toISOString(),
      },
      {
        role: "consultant",
        message: "Other tab reply.",
        at: new Date().toISOString(),
        data: {
          aiReply: "Other tab reply.",
          messageText: "Other tab reply.",
          sources: [],
        },
      },
    );
    r.updatedAt = new Date().toISOString();
    await BobalabHistoryStore.save(r);
  });
  await page
    .locator("#sidebar-history-list .history-row")
    .filter({ hasText: "First plan reviewed" })
    .locator(".history-action", { hasText: "Rename" })
    .click();
  await page.locator("#rename-title").fill("First plan renamed safely");
  await page.locator('#rename-form button[type="submit"]').click();
  await page.locator("#rename-dialog").waitFor({ state: "hidden" });
  await send("A stale-tab reply must stay local.");
  await page.waitForFunction(() =>
    document
      .querySelector("#history-notice")
      .textContent.includes("changed in another tab"),
  );
  const saved = await page.evaluate(() => BobalabHistoryStore.list());
  const current = saved.find((r) => r.title === "First plan renamed safely");
  assert(current.messages.some((m) => m.message === "Other tab only."));
  assert(
    !current.messages.some(
      (m) => m.message === "A stale-tab reply must stay local.",
    ),
  );
  checks.push(
    "renaming a stale open thread does not allow overwriting another tab",
  );
  await page
    .locator("#sidebar-history-list .history-open", {
      hasText: "Second planning question.",
    })
    .click();
  await page.locator("#history-confirm-dialog").waitFor({ state: "visible" });
  await page.locator("#history-confirm-no").click();
  assert(
    (await page.locator(".message-user").last().textContent()).includes(
      "stale-tab",
    ),
  );
  checks.push(
    "unsaved reply after a failed save requires confirmation before switching",
  );
  const second = page
    .locator("#sidebar-history-list .history-row")
    .filter({ hasText: "Second planning question." });
  await second.locator(".history-action", { hasText: "Delete" }).click();
  await page.locator("#history-confirm-no").click();
  await settled(2);
  await second.locator(".history-action", { hasText: "Delete" }).click();
  await page.locator("#history-confirm-yes").click();
  await settled(1);
  checks.push("sidebar deletion is confirmed and updates the visible list");
  assert.equal(errors.length, 0);
  const report = {
    kind: "local sidebar and drawer checks with synthetic model fixtures; no live calls",
    checks,
    browser_errors: errors,
    accessibility_audits: audits,
  };
  fs.writeFileSync(
    "work/sidebar-browser-checks.json",
    JSON.stringify(report, null, 2),
  );
  console.log(JSON.stringify(report));
  await browser.close();
  if (audits.some((a) => a.violations.length)) process.exitCode = 2;
})().catch(async (e) => {
  console.error(e.stack);
  await browser?.close();
  process.exit(1);
});
