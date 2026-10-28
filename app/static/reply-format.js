/* A deliberately small text-only Markdown renderer. Never parses model HTML. */
"use strict";
(() => {
  function inline(parent, text) {
    const pattern = /(\*\*([^*\n]+)\*\*|`([^`\n]+)`|\*([^*\n]+)\*)/g;
    let last = 0;
    for (const match of text.matchAll(pattern)) {
      parent.append(document.createTextNode(text.slice(last, match.index)));
      const tag = match[2] ? "strong" : match[3] ? "code" : "em";
      const element = document.createElement(tag);
      element.textContent = match[2] || match[3] || match[4];
      parent.append(element);
      last = match.index + match[0].length;
    }
    parent.append(document.createTextNode(text.slice(last)));
  }
  function cells(line) {
    return line
      .trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((s) => s.trim());
  }
  function tableAt(lines, i) {
    if (i + 1 >= lines.length || !lines[i].includes("|")) return false;
    const a = cells(lines[i]),
      b = cells(lines[i + 1]);
    return (
      a.length >= 2 &&
      a.length <= 8 &&
      a.length === b.length &&
      b.every((c) => /^:?-{3,}:?$/.test(c))
    );
  }
  function listItem(line) {
    return line.match(/^(\s*)([-+*]|\d+[.)])\s+(.+)$/);
  }
  function render(text) {
    const fragment = document.createDocumentFragment();
    const lines = String(text).replace(/\r\n?/g, "\n").split("\n");
    let i = 0;
    while (i < lines.length) {
      if (!lines[i].trim()) {
        i++;
        continue;
      }
      if (tableAt(lines, i)) {
        const headers = cells(lines[i]),
          rows = [];
        let next = i + 2;
        while (
          next < lines.length &&
          lines[next].trim() &&
          lines[next].includes("|")
        ) {
          const row = cells(lines[next]);
          if (row.length !== headers.length) break;
          rows.push(row);
          next++;
        }
        const wrap = document.createElement("div");
        wrap.className = "reply-table-scroll";
        wrap.tabIndex = 0;
        wrap.setAttribute("role", "region");
        wrap.setAttribute(
          "aria-label",
          "Comparison table; scroll horizontally if needed",
        );
        const table = document.createElement("table"),
          head = document.createElement("thead"),
          tr = document.createElement("tr"),
          body = document.createElement("tbody");
        for (const text of headers) {
          const th = document.createElement("th");
          th.scope = "col";
          inline(th, text);
          tr.append(th);
        }
        head.append(tr);
        for (const row of rows) {
          const tr = document.createElement("tr");
          for (const text of row) {
            const td = document.createElement("td");
            inline(td, text);
            tr.append(td);
          }
          body.append(tr);
        }
        table.append(head, body);
        wrap.append(table);
        fragment.append(wrap);
        i = next;
        continue;
      }
      const heading = lines[i].match(/^\s{0,3}#{1,6}\s+(.+)$/);
      if (heading) {
        const h = document.createElement("h3");
        inline(h, heading[1]);
        fragment.append(h);
        i++;
        continue;
      }
      const item = listItem(lines[i]);
      if (item) {
        const ordered = /^\d/.test(item[2]),
          list = document.createElement(ordered ? "ol" : "ul");
        if (ordered) list.start = parseInt(item[2], 10);
        while (i < lines.length) {
          const match = listItem(lines[i]);
          if (!match || /^\d/.test(match[2]) !== ordered) break;
          const li = document.createElement("li");
          // Preserve indentation as visible text rather than silently invent nesting.
          inline(li, match[1] + match[3]);
          list.append(li);
          i++;
        }
        fragment.append(list);
        continue;
      }
      const paragraph = [lines[i++]];
      while (
        i < lines.length &&
        lines[i].trim() &&
        !/^\s{0,3}#{1,6}\s+/.test(lines[i]) &&
        !listItem(lines[i]) &&
        !tableAt(lines, i)
      )
        paragraph.push(lines[i++]);
      const p = document.createElement("p");
      inline(p, paragraph.join("\n"));
      fragment.append(p);
    }
    return fragment;
  }
  window.BobalabFormat = Object.freeze({ render });
})();
