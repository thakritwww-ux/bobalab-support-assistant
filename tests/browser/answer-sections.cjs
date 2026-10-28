/* Local fixture verification only. No real model, customer data or provider key. */
const { chromium } = require("playwright");
const assert = require("assert"),
  fs = require("fs");
let browser;
(async () => {
  browser = await chromium.launch({ channel: "chrome", headless: true });
  const ctx = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
    }),
    p = await ctx.newPage();
  const checks = [],
    audits = [],
    errors = [],
    responses = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", async (r) => {
    if (r.url().endsWith("/ui/chat")) responses.push(await r.json());
  });
  async function send(text) {
    const n = await p.locator(".message-assistant").count();
    await p.locator("#message-input").fill(text);
    await p.locator("#send-button").click();
    await p.waitForFunction(
      (n) => document.querySelectorAll(".message-assistant").length === n,
      n + 1,
    );
    await p.waitForFunction(
      () => !document.querySelector("#message-input").readOnly,
    );
  }
  async function audit(name) {
    await p.evaluate(
      fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8"),
    );
    const r = await p.evaluate(() =>
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
  await p.goto("http://127.0.0.1:8003", { waitUntil: "networkidle" });
  await p.locator("#access-code").fill("preview-demo-code");
  await p.locator("#access-submit").click();
  await p.locator("#chat-view").waitFor({ state: "visible" });
  await p.locator('[data-action="history-settings"]').click();
  await p.locator("#remember-history").check();
  await p.waitForFunction(() => BobalabHistoryStore.enabled());
  await p.locator('[data-close="history-dialog"]').click();
  await send("__test_sections__");
  assert.equal(await p.locator(".message-body ul li").count(), 2);
  assert.equal(await p.locator(".message-body ol li").count(), 2);
  assert.equal(await p.locator(".message-body table").count(), 1);
  checks.push(
    "validated typed sections render as native bullets steps and comparison table",
  );
  assert.equal(
    await p.locator(".message-body tbody tr").first().locator("td").count(),
    4,
  );
  assert(
    (await p.locator(".message-body tbody tr").first().textContent()).includes(
      "Option A | literal pipe",
    ),
  );
  checks.push("literal pipe in an option cannot change table columns");
  assert(
    (await p.locator(".message-body").textContent()).includes("Not specified"),
  );
  assert(
    (await p.locator(".answer-caveat").first().textContent()).includes(
      "collection is limited",
    ),
  );
  checks.push("unknown cells and point-specific uncertainty remain visible");
  await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
  await p.locator(".copy-button").click();
  assert.equal(
    await p.evaluate(() => navigator.clipboard.readText()),
    responses[0].aiReply,
  );
  checks.push("copy retains canonical aiReply and reviewed source footer");
  await p.waitForFunction(
    async () => (await BobalabHistoryStore.list()).length === 1,
  );
  const saved = await p.evaluate(() => BobalabHistoryStore.list());
  assert.equal(saved[0].messages[1].data.replyFormat, "sections-v1");
  assert(saved[0].messages[1].data.formatHash);
  checks.push("device history records typed content and versioned format hash");
  await audit("desktop typed answer");
  await p.locator("#conversation-scroll").evaluate((e) => (e.scrollTop = 0));
  await p.screenshot({ path: "work/sections-desktop-fixture.png" });
  await p.reload({ waitUntil: "networkidle" });
  await p.locator("#sidebar-history-list .history-open").click();
  await p.locator(".message-body table").waitFor();
  assert.equal(await p.locator(".message-body ol li").count(), 2);
  checks.push("reopened history preserves typed structure");
  const download = p.waitForEvent("download");
  await p.locator('[data-action="history"]').first().click();
  await p.locator("#history-export-json").click();
  const file = await download;
  const record = JSON.parse(fs.readFileSync(await file.path(), "utf8"));
  assert.deepEqual(
    record.conversation.messages[1].data.answer,
    saved[0].messages[1].data.answer,
  );
  checks.push("JSON export preserves exact typed answer and metadata");
  await p.locator('[data-close="history-dialog"]').click();
  for (const [width, height] of [
    [360, 740],
    [390, 844],
    [768, 1024],
    [1280, 800],
  ]) {
    await p.setViewportSize({ width, height });
    await p.waitForTimeout(100);
    assert(
      !(await p.evaluate(
        () => document.documentElement.scrollWidth > innerWidth,
      )),
    );
    assert((await p.locator("#send-button").boundingBox()).y < height);
  }
  checks.push("typed comparison stays contained at four viewport sizes");
  await p.setViewportSize({ width: 390, height: 844 });
  await p.locator("#conversation-scroll").evaluate((e) => (e.scrollTop = 0));
  await p.screenshot({ path: "work/sections-mobile-fixture.png" });
  await audit("mobile typed answer");
  await send("ฉันควรเริ่มอย่างไร");
  assert.equal(
    await p.locator(".message-body").last().locator("ol li").count(),
    2,
  );
  assert(
    (await p.locator(".message-body").last().textContent()).includes(
      "ขั้นตอนถัดไป",
    ),
  );
  checks.push("Thai typed steps and caveats render with localized labels");
  await send("__test_html__");
  assert.equal(await p.locator(".message-body img").count(), 0);
  assert(!(await p.evaluate(() => window.injected)));
  checks.push("structured HTML-looking text stays inert");
  const safe = await p.evaluate(() => {
    const corrupt = {
      direct_answer: "Safe",
      sections: [
        { kind: "comparison", items: [], options: [{ label: "bad" }] },
      ],
    };
    return BobalabFormat.renderAnswer(corrupt) === null;
  });
  assert(safe);
  checks.push(
    "malformed stored structures fall back to canonical text instead of crashing",
  );
  await send("A simple concern.");
  assert.equal(
    await p.locator(".message-body").last().locator("h3,ul,ol,table").count(),
    0,
  );
  checks.push("simple answer has no forced empty sections");
  // A pre-sections saved record can still be displayed without a new model call.
  await p.evaluate(() =>
    window.dispatchEvent(
      new CustomEvent("bobalab:open-thread", {
        detail: {
          messages: [
            {
              role: "client",
              message: "Old saved question",
              at: new Date().toISOString(),
            },
            {
              role: "consultant",
              message: "Old saved reply.",
              at: new Date().toISOString(),
              data: {
                aiReply: "Old saved reply.",
                messageText: "Old saved reply.",
                sources: [],
              },
            },
          ],
        },
      }),
    ),
  );
  assert(
    (await p.locator(".message-body").textContent()).includes(
      "Old saved reply",
    ),
  );
  checks.push("older saved conversations remain readable");
  assert.equal(errors.length, 0);
  const report = {
    kind: "local section-based presentation checks with explicitly simulated LLM responses",
    checks,
    browser_errors: errors,
    accessibility_audits: audits,
  };
  fs.writeFileSync(
    "work/answer-sections-browser.json",
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
