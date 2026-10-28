/* Run against: python -m tests.browser.preview. Requires dev-only Playwright/axe-core. */
const { chromium } = require("playwright");
const fs = require("fs"),
  assert = require("assert");
let browser;
(async () => {
  const target = process.env.BROWSER_TEST_URL || "http://127.0.0.1:8002";
  if (!/^http:\/\/127\.0\.0\.1:/.test(target))
    throw Error("Fixture tests only run locally.");
  browser = await chromium.launch({ channel: "chrome", headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    acceptDownloads: true,
  });
  const page = await ctx.newPage(),
    errors = [],
    requests = [],
    checks = [],
    audits = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (r.url().endsWith("/ui/chat")) requests.push(JSON.parse(r.postData()));
  });
  async function check(name, fn) {
    await fn();
    checks.push(name);
  }
  async function history() {
    await page.locator('[data-action="history"]').first().click();
    await page.locator("#history-dialog").waitFor({ state: "visible" });
  }
  async function closeHistory() {
    await page.locator('[data-close="history-dialog"]').click();
  }
  async function send(text) {
    const count = await page.locator(".message-assistant").count();
    await page.locator("#message-input").fill(text);
    await page.locator("#send-button").click();
    await page.waitForFunction(
      (n) => document.querySelectorAll(".message-assistant").length === n,
      count + 1,
    );
    await page.waitForFunction(
      () => !document.querySelector("#message-input").readOnly,
    );
  }
  async function login(p) {
    await p.goto(target, { waitUntil: "networkidle" });
    await p.locator("#access-code").fill("preview-demo-code");
    await p.locator("#access-submit").click();
    await p.locator("#chat-view").waitFor({ state: "visible" });
  }
  async function audit(name) {
    await page.evaluate(
      fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8"),
    );
    const result = await page.evaluate(() =>
      axe.run(document, {
        runOnly: {
          type: "tag",
          values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"],
        },
      }),
    );
    audits.push({
      name,
      violations: result.violations.map((v) => ({
        id: v.id,
        nodes: v.nodes.map((n) => n.target),
      })),
    });
  }
  await login(page);
  await check(
    "long plain replies gain paragraph spacing without changing any text",
    async () => {
      const result = await page.evaluate(() => {
        const text =
          "The available information needs to be checked carefully before deciding, because the circumstances and terms can vary between customers and providers. ".repeat(
            5,
          );
        const node = document.createElement("div");
        node.append(BobalabFormat.render(text));
        return {
          same: node.textContent === text,
          count: node.querySelectorAll("p").length,
        };
      });
      assert(result.same);
      assert(result.count > 1);
    },
  );
  await check("saving is off by default and no thread is written", async () => {
    await send("A temporary question.");
    assert.equal(
      (await page.evaluate(() => BobalabHistoryStore.list())).length,
      0,
    );
  });
  await history();
  await page.locator("#remember-history").check();
  await page.waitForFunction(
    async () => (await BobalabHistoryStore.list()).length === 1,
  );
  await closeHistory();
  await check(
    "opting in saves the current completed conversation",
    async () => {
      assert.equal(
        (await page.evaluate(() => BobalabHistoryStore.list()))[0].messages
          .length,
        2,
      );
    },
  );
  await page.reload({ waitUntil: "networkidle" });
  await page.locator("#chat-view").waitFor({ state: "visible" });
  await history();
  await page.locator(".history-open").click();
  await page.locator(".message-assistant").waitFor();
  await check(
    "reload retains saved history and reopening restores exact messages",
    async () => {
      assert.equal(await page.locator(".message-assistant").count(), 1);
      assert(
        (await page.locator(".message-body").textContent()).includes(
          "uncertainty preserved",
        ),
      );
    },
  );
  await send("A follow-up in the reopened conversation.");
  await check("only the reopened thread is sent as context", async () => {
    assert.equal(requests.at(-1).chatHistory.length, 2);
    assert.equal(
      requests.at(-1).chatHistory[0].message,
      "A temporary question.",
    );
  });
  await history();
  await page.locator("#remember-history").uncheck();
  await page.waitForFunction(
    async () => !(await BobalabHistoryStore.enabled()),
  );
  await closeHistory();
  await send("Not saved while saving is off.");
  assert.equal(
    (await page.evaluate(() => BobalabHistoryStore.list()))[0].messages.length,
    4,
  );
  checks.push(
    "turning saving off retains old copies without saving new replies",
  );
  await history();
  await page.locator("#remember-history").check();
  await page.waitForFunction(
    async () => (await BobalabHistoryStore.list())[0].messages.length === 6,
  );
  checks.push(
    "re-enabling saving explicitly saves the current completed replies",
  );
  await page.locator(".history-action", { hasText: "Rename" }).click();
  await page.locator("#rename-title").fill("My planning notes");
  await page.locator('#rename-form button[type="submit"]').click();
  await page.locator("#rename-dialog").waitFor({ state: "hidden" });
  assert.equal(
    await page.locator(".history-open").textContent(),
    "My planning notes",
  );
  checks.push("rename persists");
  await page.locator("#history-search").fill("no matching question");
  assert(await page.locator("#history-empty").isVisible());
  await page.locator("#history-search").fill("follow-up");
  assert.equal(await page.locator(".history-row").count(), 1);
  checks.push("search includes message text");
  await page.locator("#history-search").fill("");
  const downloadPromise = page.waitForEvent("download");
  await page.locator("#history-export-json").click();
  const downloaded = await downloadPromise;
  const path = await downloaded.path();
  const exported = JSON.parse(fs.readFileSync(path, "utf8"));
  assert.equal(exported.conversation.messages.length, 6);
  assert(
    exported.conversation.messages[1].message.includes(
      "https://image.mfa.go.th",
    ),
  );
  assert(exported.conversation.messages[1].data.promptVersion);
  checks.push(
    "export retains original replies, sources, timestamps and prompt version",
  );
  await page.locator("#history-new").click();
  await page.locator("#confirm-reset").click();
  await page.locator("#message-input").fill("__test_structure__");
  await page.locator("#send-button").click();
  await page.locator(".message-body table").waitFor();
  await check(
    "structured text renders headings lists emphasis and comparison table",
    async () => {
      assert.equal(await page.locator(".message-body h3").count(), 3);
      assert.equal(await page.locator(".message-body table").count(), 1);
      assert.equal(await page.locator(".message-body ul li").count(), 2);
      assert.equal(await page.locator(".message-body ol li").count(), 2);
      assert.equal(await page.locator(".message-body strong").count(), 2);
    },
  );
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.locator(".copy-button").click();
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  assert(copied.includes("| Option | Benefit | Tradeoff |"));
  checks.push("copy preserves the original Markdown and source footer");
  await page.screenshot({ path: "work/history-structured-desktop.png" });
  await audit("desktop structured reply");
  for (const [width, height] of [
    [360, 740],
    [390, 844],
    [768, 1024],
    [1280, 800],
  ]) {
    await page.setViewportSize({ width, height });
    await page.waitForTimeout(100);
    assert(
      !(await page.evaluate(
        () => document.documentElement.scrollWidth > innerWidth,
      )),
    );
    const bottom = await page
      .locator("#send-button")
      .evaluate((e) => e.getBoundingClientRect().bottom);
    assert(bottom <= height);
  }
  checks.push(
    "four narrow/tablet/laptop sizes contain tables without page overflow",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: "work/history-structured-mobile.png" });
  await history();
  await page.waitForFunction(
    () => document.querySelectorAll(".history-row").length === 2,
  );
  await audit("mobile saved conversations");
  await page.screenshot({ path: "work/history-mobile-list.png" });
  await closeHistory();
  await send("__test_html__");
  assert.equal(
    await page.locator(".message-body img,.message-body script").count(),
    0,
  );
  assert(!(await page.evaluate(() => window.injected)));
  checks.push("untrusted HTML remains inert");
  await send("ฉันควรเริ่มอย่างไร");
  assert.equal(
    await page.locator(".message-body").last().getAttribute("lang"),
    "th",
  );
  assert.equal(
    await page.locator(".message-body").last().locator("ul li").count(),
    2,
  );
  checks.push("Thai structured replies render");
  // Reuse a second tab to verify atomic conflict detection without another login.
  await history();
  const rows = await page.evaluate(() => BobalabHistoryStore.list());
  const current = rows.find((r) =>
    r.messages.some((m) => m.message === "__test_structure__"),
  );
  await page.evaluate(async (id) => {
    await BobalabHistoryStore.rename(id, "Changed in another tab");
  }, current.id);
  await closeHistory();
  await send("Do not overwrite another tab.");
  await page.waitForFunction(() =>
    document
      .querySelector("#history-notice")
      .textContent.includes("changed in another tab"),
  );
  checks.push("concurrent version change is not overwritten");
  await history();
  const selected = page
    .locator(".history-row")
    .filter({ hasText: "Changed in another tab" });
  await selected.locator(".history-action", { hasText: "Delete" }).click();
  await page.locator("#history-confirm-yes").click();
  await page.waitForFunction(
    async () => (await BobalabHistoryStore.list()).length === 1,
  );
  assert(!(await page.locator("#remember-history").isChecked()));
  checks.push(
    "deleting the active saved copy turns off saving to prevent recreation",
  );
  await page.locator("#history-clear").click();
  await page.locator("#history-confirm-no").click();
  assert.equal(
    (await page.evaluate(() => BobalabHistoryStore.list())).length,
    1,
  );
  checks.push("delete all requires confirmation");
  await page.locator("#history-clear").click();
  await page.locator("#history-confirm-yes").click();
  await page.waitForFunction(
    async () => !(await BobalabHistoryStore.list()).length,
  );
  assert(!(await page.locator("#remember-history").isChecked()));
  checks.push("confirmed deletion clears records and disables saving");
  await closeHistory();
  const other = await browser.newContext();
  const p2 = await other.newPage();
  await login(p2);
  assert.equal((await p2.evaluate(() => BobalabHistoryStore.list())).length, 0);
  checks.push("separate browser profile has no saved conversations");
  await other.close();
  const failed = await browser.newContext();
  await failed.addInitScript(() => {
    Object.defineProperty(window, "indexedDB", {
      get() {
        throw new DOMException("Storage unavailable", "SecurityError");
      },
    });
  });
  const p3 = await failed.newPage();
  await login(p3);
  await p3.locator("#message-input").fill("Still usable without storage");
  await p3.locator("#send-button").click();
  await p3.locator(".message-assistant").waitFor();
  assert(
    (await p3.locator("#history-notice").textContent()).includes("storage"),
  );
  checks.push("storage unavailable does not prevent chatting");
  await failed.close();
  assert.equal(errors.length, 0);
  const report = {
    kind: "local browser checks using synthetic LLM fixtures; not model-quality evidence",
    checks,
    browser_errors: errors,
    accessibility_audits: audits,
  };
  fs.writeFileSync(
    "work/customer-history-browser-checks.json",
    JSON.stringify(report, null, 2),
  );
  console.log(JSON.stringify(report));
  await browser.close();
  if (audits.some((a) => a.violations.length)) process.exitCode = 2;
})().catch(async (error) => {
  console.error(error.stack);
  await browser?.close();
  process.exit(1);
});
