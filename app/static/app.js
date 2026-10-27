"use strict";

const $ = (id) => document.getElementById(id);
const state = {
  csrf: "",
  authenticated: false,
  history: [],
  pending: false,
  sequence: 0,
  controller: null,
  userBubble: null,
  resetAction: "reset",
};
const scroll = $("conversation-scroll");
const input = $("message-input");

function icon(name) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "icon");
  svg.setAttribute("aria-hidden", "true");
  const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
  use.setAttribute("href", "/static/icons/lucide.svg#" + name);
  svg.append(use);
  return svg;
}
function announce(text) {
  $("announcer").textContent = text;
}
function authenticated(value) {
  state.authenticated = value;
  $("boot-state").hidden = true;
  $("access-view").hidden = value;
  $("chat-view").hidden = !value;
  document.querySelectorAll(".auth-only").forEach((el) => {
    el.hidden = !value;
  });
}
function errorText(error) {
  const code = error.code;
  if (code === "invalid_demo_code")
    return "That code wasn’t recognized. Check the private demo code you received.";
  if (code === "ui_not_configured")
    return "Demo access isn’t configured yet. Please contact the demo owner.";
  if (code === "ui_session_expired")
    return "Your demo access has expired. Open the demo again to continue.";
  if (code === "csrf_failed")
    return "Your access needs refreshing. Try again after the demo reconnects.";
  if (code === "daily_call_limit")
    return "The demo has reached its shared daily allowance. Please try another Bangkok day.";
  if (code === "request_limit")
    return "A few requests arrived together. Please wait a minute before trying again.";
  if (code === "invalid_request" || error.status === 413)
    return "The message or conversation is too long. Shorten it, or start a new conversation.";
  if (error.status === 502)
    return "The assistant couldn’t safely prepare a reply. Your question is still here; you can try again.";
  if (error.name === "AbortError")
    return "No reply arrived in time. Your question is still here. The server may still be finishing the request.";
  return "The assistant couldn’t reply just now. Your question is still here; please try again later.";
}
async function request(path, payload, signal) {
  const controller = signal ? null : new AbortController();
  const timer = controller
    ? setTimeout(() => controller.abort(), 150000)
    : null;
  try {
    const response = await fetch(path, {
      method: payload === undefined ? "GET" : "POST",
      credentials: "same-origin",
      cache: "no-store",
      headers:
        payload === undefined
          ? {}
          : { "Content-Type": "application/json", "X-CSRF-Token": state.csrf },
      body: payload === undefined ? undefined : JSON.stringify(payload),
      signal: signal || controller.signal,
    });
    let data;
    try {
      data = await response.json();
    } catch (_) {
      throw { status: response.status, code: "invalid_response" };
    }
    if (!response.ok)
      throw {
        status: response.status,
        code: data.error?.code || "unavailable",
      };
    return data;
  } finally {
    if (timer) clearTimeout(timer);
  }
}
async function reconnect() {
  const data = await request("/ui/session");
  state.csrf = data.csrfToken;
  authenticated(Boolean(data.authenticated));
  if (!data.available) {
    $("access-error").textContent =
      "Demo access isn’t configured yet. Please contact the demo owner.";
    $("access-error").hidden = false;
    $("access-submit").disabled = true;
  }
  return data;
}
function updateComposer() {
  const count = Array.from(input.value).length;
  $("message-count").textContent = count.toLocaleString() + " / 6,000";
  $("message-count").hidden = count < 5000;
  $("message-count").classList.toggle("over-limit", count > 6000);
  input.setAttribute("aria-invalid", count > 6000 ? "true" : "false");
  input.readOnly = state.pending;
  $("send-button").disabled =
    state.pending || !input.value.trim() || count > 6000;
}
function atBottom() {
  return scroll.scrollHeight - scroll.scrollTop - scroll.clientHeight < 100;
}
function toBottom() {
  scroll.scrollTo({ top: scroll.scrollHeight, behavior: "instant" });
  $("new-reply").hidden = true;
}
function showError(text, retry = true) {
  $("chat-error-text").textContent = text;
  $("chat-error").hidden = false;
  $("retry-button").hidden = !retry;
}
function language(text) {
  return /[\u0E00-\u0E7F]/.test(text) ? "th" : "en";
}
function sourceLink(source) {
  if (typeof source.url !== "string" || typeof source.title !== "string")
    return null;
  let url;
  try {
    url = new URL(source.url);
  } catch (_) {
    return null;
  }
  if (
    url.protocol !== "https:" ||
    !/\.(go\.th|thaiembassy\.org)$/i.test(url.hostname)
  )
    return null;
  const link = document.createElement("a");
  link.className = "source-link";
  link.href = url.href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.append(icon("arrow-up-right"));
  const content = document.createElement("span");
  content.className = "source-content";
  const title = document.createElement("span");
  title.className = "source-title";
  title.textContent = source.title;
  const detail = document.createElement("span");
  detail.className = "source-detail";
  detail.textContent =
    url.hostname +
    (source.reviewedAt ? " · Reviewed " + source.reviewedAt : "") +
    (source.scope ? " · Scope: " + source.scope : "");
  content.append(title, detail);
  link.append(content);
  return link;
}
function addAssistant(data) {
  const article = document.createElement("article");
  article.className = "message message-assistant";
  const label = document.createElement("div");
  label.className = "assistant-label";
  label.append(icon("message-circle"), document.createTextNode("BOBALAB"));
  const body = document.createElement("div");
  body.className = "message-body";
  body.lang = language(data.messageText);
  body.textContent = data.messageText;
  article.append(label, body);
  if (Array.isArray(data.sources) && data.sources.length) {
    const sources = document.createElement("div");
    sources.className = "sources";
    const heading = document.createElement("p");
    heading.className = "sources-heading";
    heading.textContent = "Sources mentioned";
    const links = data.sources.map(sourceLink).filter(Boolean);
    if (links.length) {
      sources.append(heading, ...links);
      article.append(sources);
    }
  }
  const tools = document.createElement("div");
  tools.className = "message-tools";
  const copy = document.createElement("button");
  copy.type = "button";
  copy.className = "text-button copy-button";
  copy.append(icon("copy"), document.createTextNode("Copy reply"));
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(data.aiReply);
      announce("Reply copied, including its sources.");
      copy.lastChild.textContent = "Copied";
      setTimeout(() => {
        copy.lastChild.textContent = "Copy reply";
      }, 1800);
    } catch (_) {
      announce(
        "The reply couldn’t be copied. You can select the text directly.",
      );
    }
  });
  tools.append(copy);
  article.append(tools);
  $("messages").append(article);
}
async function sendMessage(event) {
  if (event) event.preventDefault();
  const question = input.value.trim();
  if (state.pending || !question || !state.authenticated) return;
  const length = Array.from(question).length;
  const total =
    length +
    state.history.reduce((n, turn) => n + Array.from(turn.message).length, 0);
  const payload = { clientSequence: question, chatHistory: state.history };
  if (
    length > 6000 ||
    total > 24000 ||
    state.history.length > 100 ||
    state.history.some((t) => Array.from(t.message).length > 6000) ||
    new TextEncoder().encode(JSON.stringify(payload)).length > 65536
  ) {
    showError(
      "The message or conversation has reached the demo limit. Shorten your question, or start a new conversation.",
      false,
    );
    return;
  }
  const sequence = ++state.sequence;
  state.pending = true;
  updateComposer();
  $("chat-error").hidden = true;
  $("empty-state").hidden = true;
  if (state.userBubble) state.userBubble.remove();
  const user = document.createElement("div");
  user.className = "message message-user";
  user.lang = language(question);
  user.textContent = question;
  state.userBubble = user;
  $("messages").append(user);
  const waiting = document.createElement("div");
  waiting.className = "pending-message";
  const spinner = document.createElement("span");
  spinner.className = "spinner";
  spinner.setAttribute("aria-hidden", "true");
  const waitingText = document.createElement("span");
  waitingText.textContent = "Preparing a reply…";
  waiting.append(spinner, waitingText);
  $("messages").append(waiting);
  toBottom();
  announce("Preparing a reply.");
  const slow = setTimeout(() => {
    waitingText.textContent = "This may take a little longer on free hosting…";
  }, 12000);
  const controller = new AbortController();
  state.controller = controller;
  const timeout = setTimeout(() => controller.abort(), 150000);
  try {
    const data = await request("/ui/chat", payload, controller.signal);
    if (sequence !== state.sequence) return;
    if (
      typeof data.aiReply !== "string" ||
      !data.aiReply.trim() ||
      typeof data.messageText !== "string"
    )
      throw { code: "invalid_response" };
    const follow = atBottom();
    waiting.remove();
    addAssistant(data);
    state.history.push(
      { role: "client", message: question },
      { role: "consultant", message: data.aiReply },
    );
    state.userBubble = null;
    input.value = "";
    if (follow) toBottom();
    else $("new-reply").hidden = false;
    announce("Reply received.");
  } catch (error) {
    if (sequence !== state.sequence) return;
    waiting.remove();
    if (error.code === "ui_session_expired" || error.code === "csrf_failed") {
      try {
        await reconnect();
      } catch (_) {
        authenticated(false);
      }
      if (!state.authenticated) {
        $("access-error").textContent =
          "Open demo access again to continue. Your draft is still in this tab.";
        $("access-error").hidden = false;
      }
    }
    showError(
      errorText(error),
      !["daily_call_limit", "invalid_request", "request_limit"].includes(
        error.code,
      ),
    );
  } finally {
    clearTimeout(slow);
    clearTimeout(timeout);
    if (sequence === state.sequence) {
      state.pending = false;
      state.controller = null;
      updateComposer();
    }
  }
}
function clearConversation() {
  state.sequence++;
  state.controller?.abort();
  state.controller = null;
  state.pending = false;
  state.history = [];
  state.userBubble = null;
  $("messages").replaceChildren();
  input.value = "";
  $("chat-error").hidden = true;
  $("new-reply").hidden = true;
  $("empty-state").hidden = false;
  updateComposer();
  scroll.scrollTop = 0;
}
async function resetOrLock() {
  $("reset-dialog").close();
  if (state.resetAction === "logout") {
    try {
      const data = await request("/ui/logout", {});
      state.csrf = data.csrfToken;
      clearConversation();
      authenticated(false);
      $("access-code").focus();
    } catch (error) {
      showError("The demo couldn’t be locked. Please try again.", false);
    }
  } else {
    clearConversation();
    if (state.authenticated) input.focus();
  }
}
function confirmReset(action) {
  if (!state.authenticated) {
    $("access-code").focus();
    return;
  }
  state.resetAction = action;
  if (
    !state.history.length &&
    !state.pending &&
    !input.value.trim() &&
    action === "reset"
  ) {
    clearConversation();
    input.focus();
    return;
  }
  $("reset-heading").textContent =
    action === "logout" ? "Lock this demo?" : "A fresh conversation?";
  $("confirm-reset").firstChild.textContent =
    action === "logout" ? "Lock demo " : "Start fresh ";
  $("reset-description").textContent =
    "This clears the chat and draft in this tab. It does not erase messages already sent to the model provider.";
  $("reset-pending-note").hidden = !state.pending;
  $("reset-dialog").showModal();
  $("cancel-reset").focus();
}

$("access-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("access-submit");
  if (button.disabled) return;
  button.disabled = true;
  $("access-error").hidden = true;
  try {
    const data = await request("/ui/session", {
      accessCode: $("access-code").value.trim(),
    });
    state.csrf = data.csrfToken;
    authenticated(Boolean(data.authenticated));
    $("access-code").value = "";
    input.focus();
  } catch (error) {
    $("access-error").textContent = errorText(error);
    $("access-error").hidden = false;
    if (error.code === "csrf_failed") {
      try {
        await reconnect();
      } catch (_) {}
    }
  } finally {
    button.disabled = false;
  }
});
$("reveal-code").addEventListener("click", () => {
  const show = $("access-code").type === "password";
  $("access-code").type = show ? "text" : "password";
  $("reveal-code").setAttribute(
    "aria-label",
    show ? "Hide access code" : "Show access code",
  );
  $("reveal-code").setAttribute("aria-pressed", String(show));
});
$("chat-form").addEventListener("submit", sendMessage);
input.addEventListener("input", updateComposer);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    sendMessage();
  }
});
$("retry-button").addEventListener("click", sendMessage);
$("new-reply").addEventListener("click", toBottom);
scroll.addEventListener(
  "scroll",
  () => {
    if (atBottom()) $("new-reply").hidden = true;
  },
  { passive: true },
);
document.querySelectorAll(".starter").forEach((button) =>
  button.addEventListener("click", () => {
    input.value = button.dataset.question;
    updateComposer();
    input.focus();
  }),
);
document
  .querySelectorAll('[data-action="new-chat"]')
  .forEach((button) =>
    button.addEventListener("click", () => confirmReset("reset")),
  );
document
  .querySelectorAll('[data-action="logout"]')
  .forEach((button) =>
    button.addEventListener("click", () => confirmReset("logout")),
  );
document
  .querySelectorAll('[data-action="about"]')
  .forEach((button) =>
    button.addEventListener("click", () => $("about-dialog").showModal()),
  );
document.querySelectorAll(".wordmark").forEach((link) =>
  link.addEventListener("click", (event) => {
    if (state.authenticated) {
      event.preventDefault();
      confirmReset("reset");
    }
  }),
);
document
  .querySelectorAll("[data-close]")
  .forEach((button) =>
    button.addEventListener("click", () => $(button.dataset.close).close()),
  );
$("cancel-reset").addEventListener("click", () => $("reset-dialog").close());
$("confirm-reset").addEventListener("click", resetOrLock);
reconnect().catch(() => {
  authenticated(false);
  $("access-error").textContent =
    "The demo couldn’t connect. Please refresh this page to try again.";
  $("access-error").hidden = false;
  $("access-submit").disabled = true;
});
