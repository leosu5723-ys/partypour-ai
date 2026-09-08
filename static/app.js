// PartyPour AI — 前端逻辑 / frontend logic
// 只负责展示：所有真正的解析/校验/检索/计算/推荐/解释逻辑都在后端 app.py -> Assignment.py
// This file only renders. Every real parse/validate/retrieve/calculate/
// recommend/explain decision happens server-side in Assignment.py.

let SUPPORTED_MENU = [];
let manualRowCount = 0;

// ---------------------------------------------------------------------------
// bilingual violation-code translator — known prefixes get a friendly
// bilingual label; anything unrecognised still shows the raw string so
// nothing is silently hidden.
// ---------------------------------------------------------------------------
const VIOLATION_LABELS = [
  { prefix: "UNSUPPORTED_DRINK_NOT_FLAGGED", zh: "解析器漏标了一个不支持的酒品", en: "Parser failed to flag an unsupported drink" },
  { prefix: "MISSING_SERVINGS_NOT_FLAGGED", zh: "缺少杯数但没有被标记", en: "Missing serving count was not flagged" },
  { prefix: "MISSING_PARTY_SIZE_NOT_FLAGGED", zh: "缺少人数但没有被标记", en: "Missing party size was not flagged" },
  { prefix: "OVER_BUDGET", zh: "超出预算", en: "Over budget" },
];

function translateViolation(v) {
  const hit = VIOLATION_LABELS.find(l => v.startsWith(l.prefix));
  if (!hit) return { zh: v, en: v };
  return { zh: `${hit.zh}：${v}`, en: `${hit.en}: ${v}` };
}

// ---------------------------------------------------------------------------
// init
// ---------------------------------------------------------------------------
async function init() {
  bindTabs();
  bindSettingsDrawer();
  bindInputModeToggle();
  document.getElementById("runPlanBtn").addEventListener("click", runPlan);
  document.getElementById("addDrinkRowBtn").addEventListener("click", () => addManualDrinkRow());
  document.getElementById("saveConfigBtn").addEventListener("click", saveConfig);

  const info = await fetchJSON("/api/init");
  SUPPORTED_MENU = info.supported_menu;

  renderMenuChips(info);
  document.getElementById("baseUrlInput").value = info.base_url || "";
  document.getElementById("modelInput").value = info.model || "";
  setConfigStatus(info.api_key_configured);

  addManualDrinkRow(); // start manual mode with one row

  await loadTestCases();
}

function fetchJSON(url, opts) {
  return fetch(url, opts).then(r => r.json().then(body => ({ ok: r.ok, body })))
    .then(({ ok, body }) => {
      if (!ok) { const e = new Error(body.error || "request_failed"); e.body = body; throw e; }
      return body;
    });
}

// ---------------------------------------------------------------------------
// tabs
// ---------------------------------------------------------------------------
function bindTabs() {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    });
  });
}

// ---------------------------------------------------------------------------
// settings drawer
// ---------------------------------------------------------------------------
function bindSettingsDrawer() {
  const drawer = document.getElementById("settingsDrawer");
  document.getElementById("settingsToggle").addEventListener("click", () => {
    drawer.classList.toggle("hidden");
  });
}

function setConfigStatus(configured) {
  const el = document.getElementById("configStatus");
  if (configured) {
    el.textContent = "✅ 已配置 Key configured";
    el.className = "status-pill status-ok";
  } else {
    el.textContent = "⚠️ 未配置 No key yet";
    el.className = "status-pill status-missing";
  }
}

async function saveConfig() {
  const api_key = document.getElementById("apiKeyInput").value.trim();
  const base_url = document.getElementById("baseUrlInput").value.trim();
  const model = document.getElementById("modelInput").value.trim();
  const res = await fetchJSON("/api/config", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key, base_url, model }),
  });
  document.getElementById("apiKeyInput").value = ""; // never keep it visible in the field
  setConfigStatus(res.api_key_configured);
}

// ---------------------------------------------------------------------------
// menu chips
// ---------------------------------------------------------------------------
function renderMenuChips(info) {
  const el = document.getElementById("menuChips");
  el.innerHTML = "";
  info.supported_menu.forEach(name => {
    const chip = document.createElement("span");
    chip.className = "menu-chip";
    chip.textContent = name;
    el.appendChild(chip);
  });
  const countChip = document.createElement("span");
  countChip.className = "menu-chip";
  countChip.style.opacity = ".7";
  countChip.textContent = `${info.sku_count} SKUs · ${info.kb_chunk_count} RAG chunks`;
  el.appendChild(countChip);
}

// ---------------------------------------------------------------------------
// input mode toggle (free text vs manual)
// ---------------------------------------------------------------------------
function bindInputModeToggle() {
  const freeBtn = document.getElementById("modeFreeTextBtn");
  const manualBtn = document.getElementById("modeManualBtn");
  freeBtn.addEventListener("click", () => {
    freeBtn.classList.add("active"); manualBtn.classList.remove("active");
    document.getElementById("freeTextMode").classList.remove("hidden");
    document.getElementById("manualMode").classList.add("hidden");
  });
  manualBtn.addEventListener("click", () => {
    manualBtn.classList.add("active"); freeBtn.classList.remove("active");
    document.getElementById("manualMode").classList.remove("hidden");
    document.getElementById("freeTextMode").classList.add("hidden");
  });
}

function addManualDrinkRow() {
  manualRowCount += 1;
  const wrap = document.getElementById("manualDrinkRows");
  const row = document.createElement("div");
  row.className = "manual-drink-row";
  const select = document.createElement("select");
  SUPPORTED_MENU.forEach(name => {
    const opt = document.createElement("option");
    opt.value = name; opt.textContent = name;
    select.appendChild(opt);
  });
  const servings = document.createElement("input");
  servings.type = "number"; servings.min = "1"; servings.value = "4";
  servings.placeholder = "杯数 servings";
  const removeBtn = document.createElement("button");
  removeBtn.className = "remove-row"; removeBtn.textContent = "✕";
  removeBtn.addEventListener("click", () => row.remove());
  row.appendChild(select); row.appendChild(servings); row.appendChild(removeBtn);
  wrap.appendChild(row);
}

function buildManualOrder() {
  const party_size = parseInt(document.getElementById("manualPartySize").value, 10) || null;
  const budget = parseFloat(document.getElementById("manualBudget").value) || null;
  const drinks = Array.from(document.querySelectorAll("#manualDrinkRows .manual-drink-row")).map(row => {
    const [select, servingsInput] = row.querySelectorAll("select, input");
    return { name: select.value, servings: parseInt(servingsInput.value, 10) || null };
  });
  return {
    party_size, budget, drinks,
    non_alcoholic_need: false, restrictions: [], missing_fields: [], unsupported_drinks: [],
  };
}

// ---------------------------------------------------------------------------
// run plan
// ---------------------------------------------------------------------------
async function runPlan() {
  const errorBox = document.getElementById("planError");
  errorBox.classList.add("hidden");
  document.getElementById("resultPanels").classList.add("hidden");

  const isManual = !document.getElementById("manualMode").classList.contains("hidden");
  const budget_mode = document.getElementById("budgetModeSelect").value;
  const payload = { budget_mode };

  if (isManual) {
    payload.manual_order = buildManualOrder();
    payload.message = "(manual order)";
  } else {
    payload.message = document.getElementById("messageInput").value.trim();
  }

  const btn = document.getElementById("runPlanBtn");
  btn.disabled = true; btn.textContent = "…";

  try {
    const result = await fetchJSON("/api/plan", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    renderResult(result, budget_mode);
    document.getElementById("resultPanels").classList.remove("hidden");
  } catch (e) {
    const body = e.body || {};
    errorBox.innerHTML = `<span class="zh">${body.error_zh || "请求失败"}</span><span class="en">${body.error_en || e.message}</span>`;
    errorBox.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.innerHTML = '▶ <span class="zh">生成方案</span><span class="en">Run</span>';
  }
}

// ---------------------------------------------------------------------------
// render result panels
// ---------------------------------------------------------------------------
function renderResult(result, chosenTier) {
  renderParsed(result.parsed_request);
  renderValidation(result.parse_violations, result.budget_violations);
  renderRetrieval(result.retrieved_knowledge);
  renderTiers(result.calculation_by_tier, result.chosen_tier);
  renderPlan(result.calculation_by_tier[result.chosen_tier], result.chosen_tier);
  renderBilingual("panelRecommend", result.recommendation_bilingual);
  renderBilingual("panelExplain", result.explanation_bilingual);
}

function renderParsed(p) {
  const el = document.getElementById("panelParsed");
  el.innerHTML = "";
  el.appendChild(kvRow("人数 / Party size", p.party_size ?? "—"));
  el.appendChild(kvRow("预算 / Budget", p.budget != null ? `S$${p.budget}` : "—"));
  el.appendChild(kvRow("需要无酒精 / Non-alcoholic need", p.non_alcoholic_need ? "是 Yes" : "否 No"));

  const drinksWrap = document.createElement("div");
  drinksWrap.className = "chip-row";
  (p.drinks || []).forEach(d => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = `${d.name} × ${d.servings ?? "?"}`;
    drinksWrap.appendChild(chip);
  });
  el.appendChild(labeledBlock("酒品 / Drinks", drinksWrap));

  if ((p.unsupported_drinks || []).length) {
    const wrap = document.createElement("div"); wrap.className = "chip-row";
    p.unsupported_drinks.forEach(name => {
      const chip = document.createElement("span"); chip.className = "chip warn";
      chip.textContent = `🚫 ${name}`; wrap.appendChild(chip);
    });
    el.appendChild(labeledBlock("不支持的酒品 / Unsupported drinks", wrap));
  }
  if ((p.missing_fields || []).length) {
    const wrap = document.createElement("div"); wrap.className = "chip-row";
    p.missing_fields.forEach(f => {
      const chip = document.createElement("span"); chip.className = "chip warn";
      chip.textContent = `❓ ${f}`; wrap.appendChild(chip);
    });
    el.appendChild(labeledBlock("缺少信息 / Missing fields", wrap));
  }
  if ((p.restrictions || []).length) {
    const wrap = document.createElement("div"); wrap.className = "chip-row";
    p.restrictions.forEach(r => {
      const chip = document.createElement("span"); chip.className = "chip";
      chip.textContent = r; wrap.appendChild(chip);
    });
    el.appendChild(labeledBlock("限制条件 / Restrictions", wrap));
  }
}

function renderValidation(parseViolations, budgetViolations) {
  const el = document.getElementById("panelValidation");
  el.innerHTML = "";
  const all = [...(parseViolations || []), ...(budgetViolations || [])];
  if (all.length === 0) {
    const ok = document.createElement("div");
    ok.className = "ok-box";
    ok.innerHTML = '✅ <span class="zh">未发现规则违反</span> <span class="en">/ No rule violations found</span>';
    el.appendChild(ok);
    return;
  }
  all.forEach(v => {
    const t = translateViolation(v);
    const box = document.createElement("div");
    box.className = "violation-item";
    box.innerHTML = `<span class="zh-tag">⚠️ ${t.zh}</span><br><span class="en">${t.en}</span>`;
    el.appendChild(box);
  });
}

function renderRetrieval(chunkIds) {
  const el = document.getElementById("panelRetrieval");
  el.innerHTML = "";
  const note = document.createElement("p");
  note.className = "muted";
  note.innerHTML = '<span class="zh">按本次请求的酒品从17条知识库里检索出的相关片段（关键词检索，非全量注入）：</span>' +
    '<span class="en">Chunks retrieved for this specific order from the 17-chunk knowledge base (keyword retrieval, not full-context stuffing):</span>';
  el.appendChild(note);
  const wrap = document.createElement("div");
  wrap.className = "chip-row";
  (chunkIds || []).forEach(id => {
    const chip = document.createElement("span"); chip.className = "chip";
    chip.textContent = `📄 ${id}`; wrap.appendChild(chip);
  });
  el.appendChild(wrap);
}

function renderTiers(calcByTier, chosenTier) {
  const el = document.getElementById("panelTiers");
  el.innerHTML = "";
  const grid = document.createElement("div");
  grid.className = "tier-cards";
  const zhNames = { Economy: "经济档", Balanced: "均衡档", Quality: "品质档" };
  ["Economy", "Balanced", "Quality"].forEach(tier => {
    const c = calcByTier[tier];
    const card = document.createElement("div");
    card.className = "tier-card" + (tier === chosenTier ? " chosen" : "");
    card.innerHTML = `
      <div class="tier-name">${tier} ${zhNames[tier]}${tier === chosenTier ? " ✓" : ""}</div>
      <div class="tier-price">S$${c.total_cost_sgd.toFixed(2)}</div>
      <div class="tier-range">S$${c.total_cost_min_sgd.toFixed(2)} – S$${c.total_cost_max_sgd.toFixed(2)}</div>
    `;
    grid.appendChild(card);
  });
  el.appendChild(grid);
}

function renderPlan(calc, tierName) {
  document.getElementById("chosenTierLabel").textContent = tierName;
  const el = document.getElementById("panelPlan");
  el.innerHTML = "";
  const table = document.createElement("table");
  table.className = "plan-table";
  table.innerHTML = `<thead><tr>
      <th>原料 / Ingredient</th><th>采购 / Buy</th><th>费用 / Cost</th>
    </tr></thead>`;
  const tbody = document.createElement("tbody");
  (calc.lines || []).forEach(line => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${line.ingredient}</td><td>${line.buy}</td><td>S$${line.cost_sgd.toFixed(2)}</td>`;
    tbody.appendChild(tr);
  });
  const totalTr = document.createElement("tr");
  totalTr.className = "total-row";
  totalTr.innerHTML = `<td>合计 / Total</td><td></td><td>S$${calc.total_cost_sgd.toFixed(2)}
      <span class="muted">(S$${calc.total_cost_min_sgd.toFixed(2)}–S$${calc.total_cost_max_sgd.toFixed(2)})</span></td>`;
  tbody.appendChild(totalTr);
  table.appendChild(tbody);
  el.appendChild(table);
}

function renderBilingual(elId, obj) {
  const el = document.getElementById(elId);
  el.innerHTML = "";
  if (!obj) { el.textContent = "—"; return; }
  const zh = document.createElement("div");
  zh.className = "lang-block lang-zh";
  zh.innerHTML = '<span class="lang-label">中文</span>' + escapeHtml(obj.zh || "");
  const en = document.createElement("div");
  en.className = "lang-block lang-en";
  en.innerHTML = '<span class="lang-label">English</span>' + escapeHtml(obj.en || "");
  el.appendChild(zh); el.appendChild(en);
}

// ---------------------------------------------------------------------------
// small DOM helpers
// ---------------------------------------------------------------------------
function kvRow(label, value) {
  const row = document.createElement("div");
  row.className = "kv-row";
  row.innerHTML = `<span class="kv-key">${label}</span><span>${value}</span>`;
  return row;
}

function labeledBlock(label, contentEl) {
  const wrap = document.createElement("div");
  wrap.style.marginTop = "8px";
  const lbl = document.createElement("div");
  lbl.className = "kv-key"; lbl.style.fontSize = "12px"; lbl.style.marginBottom = "3px";
  lbl.textContent = label;
  wrap.appendChild(lbl); wrap.appendChild(contentEl);
  return wrap;
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ---------------------------------------------------------------------------
// evaluation tab
// ---------------------------------------------------------------------------
async function loadTestCases() {
  const cases = await fetchJSON("/api/testcases");
  const el = document.getElementById("testCaseList");
  el.innerHTML = "";
  cases.forEach(tc => {
    const btn = document.createElement("button");
    btn.className = "testcase-btn";
    btn.innerHTML = `<span class="tc-id">${tc.id}</span><span class="tc-cat">${tc.category}</span><span class="tc-msg">${tc.message}</span>`;
    btn.addEventListener("click", () => runEvaluation(tc.id, btn));
    el.appendChild(btn);
  });
}

async function runEvaluation(caseId, btn) {
  document.querySelectorAll(".testcase-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  const resultEl = document.getElementById("evalResult");
  resultEl.classList.remove("hidden");
  resultEl.innerHTML = '<p class="muted">…</p>';

  try {
    const r = await fetchJSON("/api/evaluate", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ case_id: caseId }),
    });
    renderEvaluation(r);
  } catch (e) {
    resultEl.innerHTML = `<p class="error-box">${e.message}</p>`;
  }
}

function renderEvaluation(r) {
  const el = document.getElementById("evalResult");
  el.innerHTML = "";

  const header = document.createElement("p");
  header.innerHTML = `<strong>${r.id}</strong> [${r.category}] — ${r.message}`;
  el.appendChild(header);

  const grid = document.createElement("div");
  grid.className = "variant-grid";

  const aCard = document.createElement("div");
  aCard.className = "variant-card";
  aCard.innerHTML = '<h4>A. 裸 LLM <span class="en">Minimal LLM</span></h4>' +
    `<pre>${r.variant_a ? escapeHtml(r.variant_a) : "(未配置 API key / no API key configured)"}</pre>`;
  grid.appendChild(aCard);

  const bCard = document.createElement("div");
  bCard.className = "variant-card";
  bCard.innerHTML = '<h4>B. 简化系统 <span class="en">Simplified system</span></h4>' +
    `<pre>${escapeHtml(JSON.stringify(r.variant_b, null, 1))}</pre>`;
  grid.appendChild(bCard);

  const cCard = document.createElement("div");
  cCard.className = "variant-card";
  const c = r.variant_c;
  cCard.innerHTML = '<h4>C. 完整系统 <span class="en">Full system</span></h4>' +
    `<div class="kv-row"><span class="kv-key">Balanced 总价</span><span>S$${c.balanced_total.toFixed(2)} (S$${c.balanced_min.toFixed(2)}–S$${c.balanced_max.toFixed(2)})</span></div>` +
    `<div class="kv-row"><span class="kv-key">解析违规</span><span>${c.parse_violations.length}</span></div>` +
    `<div class="kv-row"><span class="kv-key">预算违规</span><span>${c.budget_violations.length}</span></div>`;
  grid.appendChild(cCard);

  el.appendChild(grid);

  if (r.substitution_check) {
    const s = r.substitution_check;
    const box = document.createElement("div");
    box.className = s.allowed ? "ok-box" : "violation-item";
    box.style.marginTop = "12px";
    box.innerHTML = `<strong>替代规则检查 / Substitution check:</strong> ${s.from} → ${s.to} — ` +
      `${s.allowed ? "✅ 允许 Allowed" : "🚫 拒绝 Rejected"} ` +
      `(${s.needs_confirmation ? "需用户确认 needs confirmation" : "无需确认"})<br>` +
      `<span class="muted">${s.rationale}</span>`;
    el.appendChild(box);
  }
}

init();
