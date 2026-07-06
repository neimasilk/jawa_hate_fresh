const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

// ---- tabs -------------------------------------------------------------

$$(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    $$(".tab-btn").forEach((b) => b.classList.remove("active"));
    $$(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    $("#tab-" + btn.dataset.tab).classList.add("active");
    if (btn.dataset.tab === "dashboard") loadDashboard();
  });
});

// ---- taxonomy + form population ---------------------------------------

let TAXONOMY = null;

async function loadTaxonomy() {
  const res = await fetch("/api/taxonomy");
  TAXONOMY = await res.json();

  // niche cards (tab 1)
  const cards = $("#niche-cards");
  cards.innerHTML = "";
  TAXONOMY.niches.forEach((n) => {
    const el = document.createElement("div");
    el.className = "niche-card";
    el.innerHTML = `<h4>${n.label}</h4><p>${n.guidance}</p>`;
    cards.appendChild(el);
  });

  // target chips (tab 1)
  const chips = $("#target-chips");
  chips.innerHTML = "";
  TAXONOMY.targets.forEach((t) => {
    const el = document.createElement("span");
    el.className = "chip";
    el.textContent = t;
    chips.appendChild(el);
  });

  // generator selects
  const nicheSel = $("#gen-niche");
  nicheSel.innerHTML = TAXONOMY.niches
    .map((n) => `<option value="${n.key}">${n.label}</option>`)
    .join("");
  nicheSel.addEventListener("change", updateNicheGuidance);
  updateNicheGuidance();

  const targetSel = $("#gen-target");
  targetSel.innerHTML = TAXONOMY.targets.map((t) => `<option value="${t}">${t}</option>`).join("");

  const modelSel = $("#gen-model");
  modelSel.innerHTML = TAXONOMY.gen_models
    .map((m) => `<option value="${m}">${m}${m === "deepseek" ? " (cloud, paling otentik)" : " (lokal, gratis)"}</option>`)
    .join("");

  // detector checkboxes
  const detWrap = $("#det-checks");
  detWrap.innerHTML = "";
  const all = [...TAXONOMY.detectors.cloud, ...TAXONOMY.detectors.local];
  all.forEach((d) => {
    const isCloud = TAXONOMY.detectors.cloud.includes(d);
    const id = "det-" + d.replace(/[^a-z0-9]/gi, "");
    const wrap = document.createElement("label");
    wrap.className = "checkbox-item";
    wrap.innerHTML = `<input type="checkbox" id="${id}" value="${d}" ${["deepseek", "grok", "qwen3:14b"].includes(d) ? "checked" : ""}> ${d} <span class="hint">(${isCloud ? "cloud" : "lokal"})</span>`;
    detWrap.appendChild(wrap);
  });
}

function updateNicheGuidance() {
  const key = $("#gen-niche").value;
  const n = TAXONOMY.niches.find((x) => x.key === key);
  $("#gen-niche-guidance").textContent = n ? n.guidance : "";
}

// ---- generator ----------------------------------------------------------

$("#gen-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const niche = $("#gen-niche").value;
  const target = $("#gen-target").value;
  const model = $("#gen-model").value;

  $("#gen-btn").disabled = true;
  $("#gen-loading").classList.remove("hidden");
  $("#gen-error").classList.add("hidden");
  $("#gen-result").classList.add("hidden");

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ niche, target, model }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "generate failed");

    $("#gen-model-badge").textContent = data.model;
    $("#gen-register-badge").textContent = data.register;
    $("#gen-severity-badge").textContent = data.severity;
    $("#gen-form-badge").textContent = data.form;
    $("#gen-latency").textContent = `${data.latency_ms} ms`;
    $("#gen-text").textContent = data.text;
    $("#gen-mekanisme").textContent = data.mekanisme || "-";
    $("#gen-result").classList.remove("hidden");
  } catch (err) {
    $("#gen-error").textContent = "Gagal generate: " + err.message;
    $("#gen-error").classList.remove("hidden");
  } finally {
    $("#gen-btn").disabled = false;
    $("#gen-loading").classList.add("hidden");
  }
});

$("#gen-to-detector").addEventListener("click", () => {
  $("#det-text").value = $("#gen-text").textContent;
  $$(".tab-btn").forEach((b) => b.classList.remove("active"));
  $$(".tab-panel").forEach((p) => p.classList.remove("active"));
  $('.tab-btn[data-tab="detector"]').classList.add("active");
  $("#tab-detector").classList.add("active");
});

// ---- detector -------------------------------------------------------------

$("#det-btn").addEventListener("click", async () => {
  const text = $("#det-text").value.trim();
  const detectors = $$("#det-checks input:checked").map((i) => i.value);
  $("#det-error").classList.add("hidden");
  $("#det-summary").classList.add("hidden");
  $("#det-results").innerHTML = "";

  if (!text) {
    $("#det-error").textContent = "Isi teks dulu (atau kirim dari tab Generator).";
    $("#det-error").classList.remove("hidden");
    return;
  }
  if (!detectors.length) {
    $("#det-error").textContent = "Pilih minimal 1 detector.";
    $("#det-error").classList.remove("hidden");
    return;
  }

  $("#det-btn").disabled = true;
  $("#det-loading").classList.remove("hidden");

  try {
    const res = await fetch("/api/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, detectors }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "detect failed");

    const grid = $("#det-results");
    let caught = 0, valid = 0;
    data.results.forEach((r) => {
      const verdictClass = r.error ? "verdict-unknown" : r.hate === true ? "verdict-hate" : r.hate === false ? "verdict-safe" : "verdict-unknown";
      const verdictLabel = r.error ? "ERROR" : r.hate === true ? "HATE" : r.hate === false ? "AMAN (bukan hate)" : "TIDAK JELAS";
      if (r.hate !== null && !r.error) {
        valid++;
        if (r.hate) caught++;
      }
      const card = document.createElement("div");
      card.className = "det-card " + verdictClass;
      card.innerHTML = `
        <div class="det-name">${r.detector}</div>
        <div class="det-verdict ${verdictClass}">${verdictLabel}</div>
        ${r.target_group ? `<div class="det-meta">target: ${Array.isArray(r.target_group) ? r.target_group.join(", ") : r.target_group}</div>` : ""}
        ${r.severity ? `<div class="det-meta">severity: ${r.severity}</div>` : ""}
        <div class="det-meta">${r.latency_ms} ms</div>
        ${r.reasoning ? `<div class="det-reasoning">${r.reasoning}</div>` : ""}
        ${r.error ? `<div class="det-reasoning">${r.error}</div>` : ""}
      `;
      grid.appendChild(card);
    });

    const summary = $("#det-summary");
    if (valid > 0) {
      const rate = caught / valid;
      summary.textContent = `${caught}/${valid} detector menandai HATE` + (rate <= 0.34 ? "  ->  teks ini LOLOS mayoritas detektor (blind-spot)" : rate >= 0.66 ? "  ->  tertangkap mayoritas detektor" : "  ->  detektor terbelah");
      summary.className = rate <= 0.34 ? "evasive" : "caught";
      summary.classList.remove("hidden");
    }
  } catch (err) {
    $("#det-error").textContent = "Gagal menjalankan detector: " + err.message;
    $("#det-error").classList.remove("hidden");
  } finally {
    $("#det-btn").disabled = false;
    $("#det-loading").classList.add("hidden");
  }
});

// ---- dashboard -------------------------------------------------------------

let dashboardLoaded = false;

async function loadDashboard() {
  if (dashboardLoaded) return;
  const res = await fetch("/api/dashboard");
  const data = await res.json();
  dashboardLoaded = true;

  if (data.overall) {
    $("#dash-overall").innerHTML = `Validasi native: <strong>${data.overall.authentic}/${data.overall.total} = ${data.overall.pct}%</strong> teks generated dinilai otentik ujaran kebencian Jawa oleh pakar native.`;
  }

  renderHeatmap($("#dash-heatmap"), data.detection_by_niche);
  renderBarList($("#dash-auth-niche"), data.authenticity_by_niche);
  renderBarList($("#dash-auth-model"), data.authenticity_by_model);
  renderTable($("#dash-evasion"), data.evasion_cross_tab);
}

function pctFromCell(cell) {
  const m = /\((\d+)%\)/.exec(cell) || /^(\d+)%$/.exec(cell);
  return m ? parseInt(m[1], 10) : null;
}

function heatColor(pct) {
  if (pct === null) return "#f2efe8";
  // sequential blue scale: low detection rate (blind-spot) = pale, high = deep blue
  const t = pct / 100;
  const r = Math.round(230 - t * 150);
  const g = Math.round(238 - t * 140);
  const b = Math.round(245 - t * 60);
  return `rgb(${r},${g},${b})`;
}

function renderHeatmap(el, rows) {
  if (!rows || !rows.length) { el.innerHTML = "<p class='hint'>Belum ada data (jalankan detect_probe.py).</p>"; return; }
  const header = rows[0];
  const body = rows.slice(1);
  let html = "<table><thead><tr>" + header.map((h) => `<th>${h}</th>`).join("") + "</tr></thead><tbody>";
  body.forEach((row) => {
    html += "<tr>" + row.map((cell, i) => {
      if (i === 0) return `<td>${cell}</td>`;
      const pct = pctFromCell(cell);
      return `<td class="heat-cell" style="background:${heatColor(pct)}">${cell}</td>`;
    }).join("") + "</tr>";
  });
  html += "</tbody></table>";
  el.innerHTML = html;
}

function renderBarList(el, rows) {
  if (!rows || rows.length < 2) { el.innerHTML = "<p class='hint'>Belum ada data.</p>"; return; }
  el.innerHTML = "";
  rows.slice(1).forEach((row) => {
    const [label, frac, ratePct] = row;
    const pct = pctFromCell(ratePct) ?? 0;
    const div = document.createElement("div");
    div.className = "bar-row";
    div.innerHTML = `
      <span>${label}</span>
      <span class="bar-track"><span class="bar-fill" style="width:${pct}%"></span></span>
      <span class="bar-rate">${ratePct} (${frac})</span>
    `;
    el.appendChild(div);
  });
}

function renderTable(el, rows) {
  if (!rows || !rows.length) { el.innerHTML = "<p class='hint'>Belum ada data.</p>"; return; }
  const header = rows[0];
  const body = rows.slice(1);
  let html = "<table><thead><tr>" + header.map((h) => `<th>${h}</th>`).join("") + "</tr></thead><tbody>";
  body.forEach((row) => {
    html += "<tr>" + row.map((c) => `<td>${c}</td>`).join("") + "</tr>";
  });
  html += "</tbody></table>";
  el.innerHTML = html;
}

loadTaxonomy();
