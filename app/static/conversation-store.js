/* Optional device-local history. No network, model calls, credentials or raw HTML. */
"use strict";
(() => {
  const NAME = "bobalab-conversations",
    VERSION = 1,
    MAX_THREADS = 100;
  let connection;
  function open() {
    if (!connection)
      connection = new Promise((resolve, reject) => {
        if (!window.indexedDB) return reject(new Error("storage_unavailable"));
        const request = indexedDB.open(NAME, VERSION);
        request.onupgradeneeded = () => {
          const db = request.result;
          db.createObjectStore("threads", { keyPath: "id" });
          db.createObjectStore("settings");
        };
        request.onerror = () => {
          connection = null;
          reject(request.error || new Error("storage_unavailable"));
        };
        request.onblocked = () => {
          connection = null;
          reject(new Error("storage_blocked"));
        };
        request.onsuccess = () => {
          const db = request.result;
          db.onversionchange = () => {
            db.close();
            connection = null;
          };
          resolve(db);
        };
      });
    return connection;
  }
  async function transaction(stores, mode, run) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(stores, mode);
      let value, failure;
      tx.oncomplete = () => resolve(value);
      tx.onerror = () =>
        reject(failure || tx.error || new Error("storage_failed"));
      tx.onabort = () =>
        reject(failure || tx.error || new Error("storage_failed"));
      try {
        run(
          tx,
          (v) => {
            value = v;
          },
          (error) => {
            failure = error;
            tx.abort();
          },
        );
      } catch (error) {
        failure = error;
        tx.abort();
      }
    });
  }
  function valid(record) {
    return (
      record &&
      typeof record.id === "string" &&
      typeof record.title === "string" &&
      record.title.length <= 100 &&
      Number.isInteger(record.revision) &&
      typeof record.createdAt === "string" &&
      typeof record.updatedAt === "string" &&
      Array.isArray(record.messages) &&
      record.messages.length <= 200 &&
      record.messages.length % 2 === 0 &&
      record.messages.every(
        (m, i) =>
          m.role === (i % 2 ? "consultant" : "client") &&
          typeof m.message === "string" &&
          m.message.length <= 6000 &&
          typeof m.at === "string" &&
          (!i ||
            !m.data ||
            (typeof m.data.aiReply === "string" &&
              typeof m.data.messageText === "string" &&
              Array.isArray(m.data.sources) &&
              m.data.sources.every(
                (s) =>
                  s && typeof s.title === "string" && typeof s.url === "string",
              ))),
      )
    );
  }
  const api = {
    async enabled() {
      return transaction(["settings"], "readonly", (tx, done) => {
        const r = tx.objectStore("settings").get("remember");
        r.onsuccess = () => done(r.result === true);
      });
    },
    async setEnabled(enabled) {
      return transaction(["settings"], "readwrite", (tx) =>
        tx.objectStore("settings").put(Boolean(enabled), "remember"),
      );
    },
    async list() {
      return transaction(["threads"], "readonly", (tx, done) => {
        const r = tx.objectStore("threads").getAll();
        r.onsuccess = () =>
          done(
            r.result
              .filter(valid)
              .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)),
          );
      });
    },
    async save(record) {
      if (!valid(record)) throw new Error("invalid_history");
      return transaction(
        ["threads", "settings"],
        "readwrite",
        (tx, done, fail) => {
          const threads = tx.objectStore("threads"),
            setting = tx.objectStore("settings").get("remember");
          setting.onsuccess = () => {
            if (!setting.result) return fail(new Error("saving_disabled"));
            const request = threads.get(record.id);
            request.onsuccess = () => {
              const previous = request.result;
              if ((previous?.revision || 0) !== record.revision)
                return fail(new Error("history_conflict"));
              const write = () => {
                const next = { ...record, revision: record.revision + 1 };
                threads.put(next);
                done(next);
              };
              if (previous) write();
              else {
                const count = threads.count();
                count.onsuccess = () =>
                  count.result >= MAX_THREADS
                    ? fail(new Error("history_limit"))
                    : write();
              }
            };
          };
        },
      );
    },
    async rename(id, title) {
      return transaction(["threads"], "readwrite", (tx, done, fail) => {
        const store = tx.objectStore("threads"),
          r = store.get(id);
        r.onsuccess = () => {
          if (!valid(r.result)) return fail(new Error("history_missing"));
          const next = {
            ...r.result,
            title: title.trim().slice(0, 100),
            revision: r.result.revision + 1,
          };
          store.put(next);
          done(next);
        };
      });
    },
    async remove(id) {
      return transaction(["threads"], "readwrite", (tx) =>
        tx.objectStore("threads").delete(id),
      );
    },
    async clear() {
      return transaction(["threads", "settings"], "readwrite", (tx) => {
        tx.objectStore("threads").clear();
        tx.objectStore("settings").put(false, "remember");
      });
    },
  };
  window.BobalabHistoryStore = Object.freeze(api);
})();
