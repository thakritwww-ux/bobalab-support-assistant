"use strict";
(() => {
  const $ = (id) => document.getElementById(id),
    store = window.BobalabHistoryStore;
  let active,
    records = [],
    remember = false,
    ready = false,
    callback;
  let sequence = Promise.resolve();
  const uid = () => crypto.randomUUID();
  function fresh() {
    return {
      id: uid(),
      title: "New conversation",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      revision: 0,
      messages: [],
    };
  }
  active = fresh();
  function notify(text) {
    $("history-notice").textContent = text;
    $("history-notice").hidden = !text;
    $("announcer").textContent = text;
  }
  function status() {
    $("remember-history").checked = remember;
    $("history-storage-status").textContent = remember
      ? "New replies save on this device."
      : "New replies are not being saved.";
    $("history-current-status").textContent = remember
      ? "Saving on this device"
      : "This conversation stays in this tab";
    $("sidebar-storage-status").textContent = remember
      ? "Saving on this device"
      : "Saving is off · Device history only";
    $("history-current-status").title =
      "Open Conversations to manage device storage.";
  }
  function failure(error) {
    const messages = {
      history_conflict:
        "This conversation changed in another tab. Your current reply is still here. Export it before reopening the saved version.",
      history_limit:
        "This device has reached the limit of 100 saved conversations. Export or delete older ones before saving more.",
      saving_disabled:
        "Saving was turned off in another tab. Your current conversation is still here.",
      storage_blocked:
        "Close other BOBALAB tabs and reopen Conversations to try device storage again.",
    };
    notify(
      messages[error.message] ||
        "Device storage is unavailable or full. Your conversation is still in this tab; export it before leaving.",
    );
    $("history-storage-status").textContent =
      "The latest change could not be saved. Export the current conversation.";
    $("history-current-status").textContent = "Latest change not saved";
    $("sidebar-storage-status").textContent = "Latest change not saved";
  }
  function enqueue(fn) {
    const task = sequence.then(fn);
    sequence = task.catch(() => {});
    return task;
  }
  async function refresh() {
    records = await store.list();
    render();
  }
  function action(text, fn) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "text-button history-action";
    b.textContent = text;
    b.addEventListener("click", fn);
    return b;
  }
  function confirm(title, description, label, fn) {
    $("history-confirm-heading").textContent = title;
    $("history-confirm-description").textContent = description;
    $("history-confirm-yes").textContent = label;
    callback = fn;
    $("history-confirm-dialog").showModal();
    $("history-confirm-no").focus();
  }
  function filtered(query) {
    query = query.trim().toLocaleLowerCase();
    return records.filter((record) =>
      (record.title + " " + record.messages.map((m) => m.message).join(" "))
        .toLocaleLowerCase()
        .includes(query),
    );
  }
  function render() {
    const matches = filtered($("history-search").value);
    $("history-empty").hidden = matches.length > 0;
    $("history-empty").textContent = records.length
      ? "No conversations match your search."
      : "No saved conversations yet. Turn on saving to keep completed replies here.";
    $("history-count").textContent = records.length + " saved on this device";
    renderRows($("history-list"), matches);
    const sidebar = filtered($("sidebar-history-search").value);
    $("sidebar-history-count").textContent = String(records.length);
    $("sidebar-history-empty").hidden = sidebar.length > 0;
    $("sidebar-history-empty").textContent = records.length
      ? "No matching conversations."
      : "No saved conversations yet. Open history settings to enable saving.";
    renderRows($("sidebar-history-list"), sidebar);
  }
  function renderRows(container, matches) {
    container.replaceChildren();
    for (const record of matches) {
      const row = document.createElement("li");
      row.className = "history-row";
      const open = action(record.title, () => openRecord(record));
      open.className = "history-open";
      if (record.id === active.id) {
        row.classList.add("is-active");
        open.setAttribute("aria-current", "true");
      }
      open.title = record.title;
      const meta = document.createElement("p");
      meta.className = "history-meta";
      meta.textContent =
        (container.id === "sidebar-history-list"
          ? new Date(record.updatedAt).toLocaleDateString(undefined, {
              month: "short",
              day: "numeric",
            })
          : new Date(record.updatedAt).toLocaleString()) +
        " · " +
        record.messages.length / 2 +
        (record.messages.length === 2 ? " reply" : " replies") +
        (record.id === active.id && container.id !== "sidebar-history-list"
          ? " · Open now"
          : "");
      const controls = document.createElement("div");
      controls.className = "history-row-actions";
      controls.append(
        action("Rename", () => rename(record)),
        action("Delete", () =>
          confirm(
            "Delete this conversation?",
            "This removes the saved copy from this browser. Export it first if you need a backup. An open copy in another tab is not erased.",
            "Delete conversation",
            async () => {
              await sequence;
              await store.remove(record.id);
              if (active.id === record.id) {
                active = { ...active, id: uid(), revision: 0 };
                remember = false;
                await store.setEnabled(false);
                status();
              }
              await refresh();
              notify("Saved conversation deleted from this device.");
            },
          ),
        ),
      );
      row.append(open, meta, controls);
      container.append(row);
    }
  }
  async function openRecord(record) {
    const go = async () => {
      await sequence;
      const latest = (await store.list()).find((r) => r.id === record.id);
      if (!latest) throw new Error("history_missing");
      if ($("history-dialog").open) $("history-dialog").close();
      active = structuredClone(latest);
      window.dispatchEvent(
        new CustomEvent("bobalab:open-thread", {
          detail: structuredClone(latest),
        }),
      );
      notify(
        "Saved conversation opened. Continuing sends this conversation's messages to the model.",
      );
      render();
    };
    const state = window.BobalabConversationState();
    const saved = records.find((r) => r.id === active.id);
    const unsaved =
      active.messages.length &&
      (!saved ||
        JSON.stringify(saved.messages) !== JSON.stringify(active.messages));
    if (state.pending || state.draft || unsaved)
      confirm(
        "Open another conversation?",
        "Your unsaved draft will be cleared. Export the current conversation first if it has not been saved. A request already sent may still finish on the server.",
        "Open conversation",
        go,
      );
    else
      try {
        await go();
      } catch (e) {
        failure(e);
      }
  }
  function rename(record) {
    $("rename-title").value = record.title;
    $("rename-dialog").dataset.threadId = record.id;
    $("rename-dialog").showModal();
    $("rename-title").focus();
  }
  async function initialize() {
    if (ready) return;
    try {
      remember = await store.enabled();
      await refresh();
      ready = true;
      status();
    } catch (error) {
      failure(error);
    }
  }
  function filename(record, ext) {
    return "BOBALAB-" + record.id + "." + ext;
  }
  function download(ext) {
    const record = structuredClone(active);
    if (!record.messages.length) {
      notify("There are no completed replies to export yet.");
      return;
    }
    let content;
    if (ext === "json")
      content = JSON.stringify(
        {
          format: "bobalab-conversation",
          schemaVersion: 1,
          exportedAt: new Date().toISOString(),
          conversation: record,
        },
        null,
        2,
      );
    else
      content =
        "BOBALAB conversation\n" +
        record.title +
        "\nSaved on this device only; reply time differs from source review dates.\n\n" +
        record.messages
          .map(
            (m) =>
              (m.role === "client" ? "Customer" : "BOBALAB") +
              " — " +
              m.at +
              (m.data?.promptVersion
                ? "\nPrompt version: " + m.data.promptVersion
                : "") +
              "\n" +
              m.message,
          )
          .join("\n\n");
    const url = URL.createObjectURL(
      new Blob([content], {
        type:
          ext === "json"
            ? "application/json;charset=utf-8"
            : "text/plain;charset=utf-8",
      }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = filename(record, ext);
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    notify(
      "Transcript downloaded, including original replies and source references.",
    );
  }
  window.BobalabConversationHistory = Object.freeze({
    async authenticated() {
      await initialize();
    },
    newThread() {
      active = fresh();
      render();
      notify("");
    },
    async completed(question, data, askedAt) {
      const record = active;
      record.messages.push(
        { role: "client", message: question, at: askedAt },
        {
          role: "consultant",
          message: data.aiReply,
          at: new Date().toISOString(),
          data: structuredClone(data),
        },
      );
      if (record.messages.length === 2 && record.title === "New conversation")
        record.title = Array.from(question).slice(0, 65).join("");
      record.updatedAt = new Date().toISOString();
      await initialize();
      if (!remember) return;
      return enqueue(async () => {
        try {
          const saved = await store.save(structuredClone(record));
          record.revision = saved.revision;
          if (active.id === record.id) status();
          await refresh();
        } catch (error) {
          failure(error);
        }
      });
    },
  });
  document
    .querySelectorAll(
      '[data-action="history"], [data-action="history-settings"]',
    )
    .forEach((b) =>
      b.addEventListener("click", async () => {
        if (!window.BobalabConversationState().authenticated) return;
        $("history-dialog").showModal();
        await initialize();
        try {
          await refresh();
        } catch (e) {
          failure(e);
        }
      }),
    );
  $("history-search").addEventListener("input", render);
  $("sidebar-history-search").addEventListener("input", render);
  $("remember-history").addEventListener("change", async () => {
    const enabled = $("remember-history").checked;
    $("remember-history").disabled = true;
    try {
      await sequence;
      await store.setEnabled(enabled);
      remember = enabled;
      ready = true;
      status();
      if (enabled && active.messages.length) {
        const record = active;
        const saved = await store.save(structuredClone(record));
        record.revision = saved.revision;
      }
      await refresh();
      notify(
        enabled
          ? "Saving enabled on this device. Completed replies will be kept here."
          : "Saving turned off. Existing saved copies remain until you delete them.",
      );
    } catch (error) {
      failure(error);
    } finally {
      $("remember-history").disabled = false;
    }
  });
  $("history-new").addEventListener("click", () => {
    $("history-dialog").close();
    document.querySelector('[data-action="new-chat"]').click();
  });
  $("history-export-text").addEventListener("click", () => download("txt"));
  $("history-export-json").addEventListener("click", () => download("json"));
  $("history-clear").addEventListener("click", () =>
    confirm(
      "Delete all saved conversations?",
      "This permanently removes all saved conversations in this browser and turns off saving. Download any transcripts you want to keep first. Other devices and open tab copies are not erased.",
      "Delete all saved",
      async () => {
        await sequence;
        await store.clear();
        remember = false;
        active = { ...active, id: uid(), revision: 0 };
        status();
        await refresh();
        notify("Saved conversations deleted. New replies will not be saved.");
      },
    ),
  );
  $("history-confirm-no").addEventListener("click", () =>
    $("history-confirm-dialog").close(),
  );
  $("history-confirm-yes").addEventListener("click", async () => {
    const action = callback;
    callback = null;
    $("history-confirm-dialog").close();
    try {
      await action?.();
    } catch (e) {
      failure(e);
    }
  });
  $("rename-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = $("rename-title").value.trim();
    if (!title) return;
    const id = $("rename-dialog").dataset.threadId;
    try {
      await sequence;
      const saved = await store.rename(id, title);
      if (active.id === id) {
        active.title = saved.title;
        if (JSON.stringify(active.messages) === JSON.stringify(saved.messages))
          active.revision = saved.revision;
      }
      $("rename-dialog").close();
      await refresh();
      notify("Conversation renamed.");
    } catch (error) {
      failure(error);
    }
  });
  status();
})();
