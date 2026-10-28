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
  function paragraphs(parent, text) {
    let chunks = [text];
    // Add whitespace at sentence boundaries only. Never infer labels or rewrite advice.
    if (
      text.length > 480 &&
      !/[*`]/.test(text) &&
      typeof Intl.Segmenter === "function"
    ) {
      const sentences = [
        ...new Intl.Segmenter(undefined, { granularity: "sentence" }).segment(
          text,
        ),
      ].map((s) => s.segment);
      if (sentences.length >= 3) {
        chunks = [];
        let chunk = "";
        for (const sentence of sentences) {
          chunk += sentence;
          if (chunk.length >= 260) {
            chunks.push(chunk);
            chunk = "";
          }
        }
        if (chunk) chunks.push(chunk);
      }
    }
    for (const chunk of chunks) {
      const p = document.createElement("p");
      inline(p, chunk);
      parent.append(p);
    }
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
      paragraphs(fragment, paragraph.join("\n"));
    }
    return fragment;
  }
  function renderAnswer(answer) {
    const atom = (text, max = 800) =>
      typeof text === "string" &&
      text.length > 0 &&
      text.length <= max &&
      !/[\r\n]/.test(text);
    const optional = (text, max = 800) => text == null || atom(text, max);
    if (
      !answer ||
      !atom(answer.direct_answer, 500) ||
      !optional(answer.caveat, 350) ||
      !optional(answer.next_step, 350) ||
      !Array.isArray(answer.sections) ||
      answer.sections.length > 4
    )
      return null;
    for (const section of answer.sections) {
      if (
        !section ||
        !optional(section.heading, 80) ||
        !optional(section.caveat, 350) ||
        !Array.isArray(section.items) ||
        !Array.isArray(section.options)
      )
        return null;
      if (section.kind === "paragraph") {
        if (
          !atom(section.text) ||
          section.items.length ||
          section.options.length
        )
          return null;
      } else if (section.kind === "bullets" || section.kind === "steps") {
        if (
          section.text != null ||
          section.options.length ||
          !section.items.length ||
          section.items.length > 6 ||
          !section.items.every(
            (i) => i && atom(i.text, 350) && optional(i.caveat, 350),
          )
        )
          return null;
      } else if (section.kind === "comparison") {
        if (
          section.text != null ||
          section.items.length ||
          section.options.length < 2 ||
          section.options.length > 4 ||
          !section.options.every(
            (o) =>
              o &&
              atom(o.label, 80) &&
              optional(o.benefit, 350) &&
              optional(o.drawback, 350) &&
              optional(o.uncertainty, 350) &&
              (o.benefit || o.drawback || o.uncertainty),
          )
        )
          return null;
      } else return null;
    }
    const thai = /[\u0E00-\u0E7F]/.test(answer.direct_answer);
    const names = thai
      ? {
          bullets: "สิ่งที่ควรตรวจสอบ",
          steps: "ขั้นตอนถัดไป",
          comparison: "ทางเลือก",
          next: "ขั้นตอนถัดไป",
          unknown: "ยังไม่ระบุ",
          columns: ["ทางเลือก", "ข้อดี", "ข้อจำกัด", "สิ่งที่ควรตรวจสอบ"],
        }
      : {
          bullets: "What to check",
          steps: "Next steps",
          comparison: "Options",
          next: "Next step",
          unknown: "Not specified",
          columns: ["Option", "Benefit", "Drawback", "What to check"],
        };
    const root = document.createDocumentFragment();
    const node = (tag, text, cls) => {
      const n = document.createElement(tag);
      n.textContent = text;
      if (cls) n.className = cls;
      return n;
    };
    const caveat = (parent, text) => {
      if (text) parent.append(node("p", text, "answer-caveat"));
    };
    root.append(node("p", answer.direct_answer));
    caveat(root, answer.caveat);
    for (const section of answer.sections) {
      const container = document.createElement("section");
      container.className = "answer-section";
      const heading = section.heading || names[section.kind];
      if (heading) container.append(node("h3", heading));
      if (section.kind === "paragraph")
        container.append(node("p", section.text));
      else if (section.kind === "bullets" || section.kind === "steps") {
        const list = document.createElement(
          section.kind === "steps" ? "ol" : "ul",
        );
        for (const item of section.items) {
          const li = document.createElement("li");
          li.append(node("span", item.text));
          caveat(li, item.caveat);
          list.append(li);
        }
        container.append(list);
      } else {
        const wrap = document.createElement("div");
        wrap.className = "reply-table-scroll";
        wrap.tabIndex = 0;
        wrap.setAttribute("role", "region");
        wrap.setAttribute("aria-label", heading || names.comparison);
        const table = document.createElement("table"),
          thead = document.createElement("thead"),
          row = document.createElement("tr"),
          tbody = document.createElement("tbody");
        for (const title of names.columns) {
          const th = node("th", title);
          th.scope = "col";
          row.append(th);
        }
        thead.append(row);
        for (const option of section.options) {
          const tr = document.createElement("tr");
          for (const value of [
            option.label,
            option.benefit,
            option.drawback,
            option.uncertainty,
          ])
            tr.append(node("td", value || names.unknown));
          tbody.append(tr);
        }
        table.append(thead, tbody);
        wrap.append(table);
        container.append(wrap);
      }
      caveat(container, section.caveat);
      root.append(container);
    }
    if (answer.next_step) {
      const next = document.createElement("section");
      next.className = "answer-section answer-next-step";
      next.append(node("h3", names.next), node("p", answer.next_step));
      root.append(next);
    }
    return root;
  }
  window.BobalabFormat = Object.freeze({ render, renderAnswer });
})();
