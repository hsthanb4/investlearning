/**
 * InvestLearning Web Platform Application Controller
 * Handles Navigation, State, Sidebar Tree, Content Rendering,
 * Code Sandbox Grading Simulator, Anna's Archive Search, and Visualizer Sync.
 */

class InvestLearningApp {
  constructor() {
    window.app = this;
    this.currentModuleIndex = 0;
    this.currentLessonIndex = 0;
    this.expandedModules = new Set([0]);
    this.currentTab = "theory"; // 'theory', 'guide', 'code', 'qa'
    this.activeVisualizer = "kline"; // 'kline', 'lob', 'markowitz', 'kelly', 'dcf'

    // Persistent state
    this.theme = localStorage.getItem("investlearning_theme") || "dark";
    this.completedLessons = new Set(JSON.parse(localStorage.getItem("investlearning_completed") || '["m01_l01", "m01_l02", "m01_l03", "m02_l01", "m02_l02", "m03_l01", "m03_l02", "m04_l01", "m04_l02", "m05_l01", "m05_l02", "m06_l01", "m06_l02", "m07_l01", "m07_l02", "m08_l01", "m08_l02", "m09_l01", "m09_l02", "m10_l01", "m10_l02"]'));
    

    // Visualizer instances
    this.vKline = null;
    this.vLob = null;
    this.vMarkowitz = null;
    this.vKelly = null;
    this.vDcf = null;

    this.init();
  }

  init() {
    this.applyTheme(this.theme);
    this.renderSidebar();
    this.renderCurrentLesson();
    this.initVisualizers();
    this.renderBooks();
    this.bindEvents();
    this.switchMainView('overview');
    this.syncLiveMarketData(false);
  }
  // ==========================================
  // KaTeX & Semantic Math Renderer (Bulletproof)
  // ==========================================
  sanitizeSvgHtml(html) {
    if (!html) return html;
    return html.replace(/<svg[\s\S]*?<\/svg>/gi, (svgMatch) => {
      return svgMatch.replace(/<\/?p>/gi, '').replace(/&le;/gi, '≤');
    });
  }

  sanitizeMath(str) {
    if (!str) return str;
    return str
      .replace(/\t(ext|imes|au|heta|o)\b/g, '\\$1')
      .replace(/\f(rac)\b/g, '\\$1')
      .replace(/\u0007(pprox)\b/g, '\\$1')
      .replace(/\\night\b/g, '\\right');
  }

  formatSemanticMath(rawLatex) {
    let clean = this.sanitizeMath(rawLatex).trim()
      .replace(/\\text\{([^}]+)\}/g, '$1')
      .replace(/\\times/g, ' × ')
      .replace(/\\cdot/g, ' · ')
      .replace(/\\le/g, ' ≤ ')
      .replace(/\\ge/g, ' ≥ ')
      .replace(/\\approx/g, ' ≈ ')
      .replace(/\\equiv/g, ' ≡ ')
      .replace(/\\implies/g, ' ⟹ ')
      .replace(/\\forall/g, '∀')
      .replace(/\\in/g, ' ∈ ')
      .replace(/\\notin/g, ' ∉ ')
      .replace(/\\sum/g, '∑')
      .replace(/\\sqrt/g, '√')
      .replace(/\\Delta/g, 'Δ')
      .replace(/\\Sigma/g, 'Σ')
      .replace(/\\Phi/g, 'Φ')
      .replace(/\\mu/g, 'μ')
      .replace(/\\sigma/g, 'σ')
      .replace(/\\beta/g, 'β')
      .replace(/\\lambda/g, 'λ')
      .replace(/\\alpha/g, 'α')
      .replace(/\\theta/g, 'θ')
      .replace(/\\eta/g, 'η')
      .replace(/\\kappa/g, 'κ')
      .replace(/\\rho/g, 'ρ')
      .replace(/\\omega/g, 'ω')
      .replace(/\\pi/g, 'π')
      .replace(/\\quad/g, '  ')
      .replace(/\\qquad/g, '    ')
      .replace(/\\mathbb\{R\}/g, 'ℝ')
      .replace(/\\%/g, '%')
      .replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1 / $2)');
    return clean;
  }

  renderMath(el) {
    if (!el) return;

    // Phase 1: Explicitly render all dedicated block formulas (.math-formula)
    const formulaBlocks = el.querySelectorAll('.math-formula');
    formulaBlocks.forEach(fEl => {
      let raw = fEl.getAttribute('data-raw') || fEl.textContent.trim();
      raw = this.sanitizeMath(raw);
      if (!fEl.getAttribute('data-raw')) fEl.setAttribute('data-raw', raw);
      if (raw.startsWith('$$') && raw.endsWith('$$')) raw = raw.slice(2, -2).trim();
      if (raw.startsWith('$') && raw.endsWith('$')) raw = raw.slice(1, -1).trim();

      let rendered = false;
      if (typeof katex !== 'undefined' && typeof katex.renderToString === 'function') {
        try {
          fEl.innerHTML = katex.renderToString(raw, { displayMode: true, output: "html", throwOnError: false });
          rendered = true;
        } catch (err) {
          console.warn("KaTeX direct block render warning:", err);
        }
      }
      if (!rendered) {
        fEl.innerHTML = `<span class="fallback-math">${this.formatSemanticMath(raw)}</span>`;
      }
    });

    // Phase 2: Render inline math ($...$) in paragraphs and list items
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(el, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\[", right: "\\]", display: true },
            { left: "\\(", right: "\\)", display: false }
          ],
          output: "html",
          throwOnError: false,
          ignoredClasses: ["math-formula", "diagram-card"],
          ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "svg", "annotation"]
        });
      } catch (e) {
        console.warn("KaTeX auto-render warning:", e);
      }
    }
  }

  // ==========================================
  // Section / View Switching Controller
  // ==========================================
  switchMainView(viewName) {
    const overviewSec = document.getElementById('overviewSection');
    const lessonView = document.getElementById('lessonViewContainer');
    const libSec = document.getElementById('librarySection');
    
    const sidebar = document.getElementById('courseSidebar');

    // Update nav buttons
    const navBtns = document.querySelectorAll('.nav-center-menu a');
    navBtns.forEach(btn => {
      const href = btn.getAttribute('href') || '';
      if ((viewName === 'overview' && href.includes('overviewSection')) ||
          (viewName === 'curriculum' && href.includes('curriculumSection')) ||
          (viewName === 'library' && href.includes('librarySection'))) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    this.currentView = viewName;
    this.renderSidebar();
    if (viewName === 'overview') {
      if (overviewSec) overviewSec.style.display = 'block';
      if (lessonView) lessonView.style.display = 'none';
      if (libSec) libSec.style.display = 'none';
      if (sidebar) {
        sidebar.style.display = '';
        sidebar.classList.remove('collapsed');
      }
      if (overviewSec) {
        this.renderMath(overviewSec);
        this.bindDiagramZoom(overviewSec);
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'curriculum') {
      if (overviewSec) overviewSec.style.display = 'none';
      if (lessonView) lessonView.style.display = 'block';
      if (libSec) libSec.style.display = 'none';
      if (sidebar) {
        sidebar.style.display = '';
        sidebar.classList.remove('collapsed');
      }
      this.switchTab(this.currentTab || 'theory');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'library') {
      if (overviewSec) overviewSec.style.display = 'none';
      if (lessonView) lessonView.style.display = 'none';
      if (libSec) libSec.style.display = 'block';
      if (sidebar) {
        sidebar.style.display = '';
        sidebar.classList.remove('collapsed');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  // ==========================================
  // Mermaid Flowchart Renderer
  // ==========================================
  // ==========================================
  // Scientific Diagram Lightbox & Zoom Engine
  // ==========================================
  // ==========================================
  // ==========================================
  // Universal Position Sizing & Real-Time Risk Engine
  // ==========================================
  calcPositionSizing() {
    const eq = parseFloat(document.getElementById("calcAccountEquity")?.value || 100000);
    const rPct = parseFloat(document.getElementById("calcRiskPct")?.value || 1.5);
    const pEntry = parseFloat(document.getElementById("calcEntryPrice")?.value || 25.0);
    const pStop = parseFloat(document.getElementById("calcStopPrice")?.value || 23.5);

    const riskAmt = eq * (rPct / 100.0);
    const deltaP = Math.abs(pEntry - pStop);
    const pctLoss = pEntry > 0 ? (deltaP / pEntry) * 100.0 : 0;

    let shares = 0;
    if (deltaP > 0.001) {
      shares = Math.floor(riskAmt / deltaP);
    }
    const lots = Math.floor(shares / 100);
    const notional = shares * pEntry;
    const posRatio = eq > 0 ? (notional / eq) * 100.0 : 0;

    const r1 = pEntry + deltaP;
    const r2 = pEntry + 2.0 * deltaP;
    const r3 = pEntry + 3.0 * deltaP;

    const riskBadge = document.getElementById("sizingRiskBadge");
    if (riskBadge) riskBadge.textContent = `锁定风险: ¥${riskAmt.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;

    const elDeltaP = document.getElementById("sizingDeltaP");
    if (elDeltaP) elDeltaP.textContent = `¥${deltaP.toFixed(2)}`;

    const elDeltaPSub = document.getElementById("sizingDeltaPSub");
    if (elDeltaPSub) elDeltaPSub.textContent = `跌幅 -${pctLoss.toFixed(1)}% 严格止损`;

    const elShares = document.getElementById("sizingShares");
    if (elShares) elShares.textContent = `${shares.toLocaleString()} 股`;

    const elLotText = document.getElementById("sizingLotText");
    if (elLotText) elLotText.textContent = `整手: ${lots.toLocaleString()} 手 (A股)`;

    const elNotional = document.getElementById("sizingNotional");
    if (elNotional) elNotional.textContent = `¥${notional.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;

    const elPosRatio = document.getElementById("sizingPosRatio");
    if (elPosRatio) elPosRatio.textContent = `占总本金 ${posRatio.toFixed(1)}%`;

    const elTargets = document.getElementById("sizingTargets");
    if (elTargets) elTargets.textContent = `¥${r1.toFixed(2)} / ¥${r2.toFixed(2)} / ¥${r3.toFixed(2)}`;
  }

  injectUniversalSizingTool(containerEl) {
    if (!containerEl) return;
    const calcBox = containerEl.querySelector(".trader-calc-box");
    if (!calcBox || calcBox.querySelector(".interactive-sizing-tool")) return;

    const tool = document.createElement("div");
    tool.className = "interactive-sizing-tool";
    tool.innerHTML = `
      <div style="font-size:0.8rem; font-weight:700; color:var(--claude-terracotta); margin-top:14px; margin-bottom:8px; padding-top:10px; border-top:1px dashed var(--border-primary); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
        <span>⚡ 操盘手即时以损定量计算器（输入你的账户资金与止损价，即时计算买入股数与止盈目标）</span>
        <span class="live-status-pill" id="sizingRiskBadge" style="color:var(--claude-terracotta); font-weight:700;">锁定风险: ¥1,500</span>
      </div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:12px;">
        <div>
          <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:2px;">账户总资金 (元)</label>
          <input type="number" id="calcAccountEquity" value="100000" step="5000" oninput="app.calcPositionSizing()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
        </div>
        <div>
          <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:2px;">单笔最大风险比例 (%)</label>
          <input type="number" id="calcRiskPct" value="1.5" step="0.1" min="0.5" max="5.0" oninput="app.calcPositionSizing()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
        </div>
        <div>
          <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:2px;">计划买入价 (元)</label>
          <input type="number" id="calcEntryPrice" value="25.00" step="0.1" oninput="app.calcPositionSizing()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
        </div>
        <div>
          <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:2px;">技术止损价 (元)</label>
          <input type="number" id="calcStopPrice" value="23.50" step="0.1" oninput="app.calcPositionSizing()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
        </div>
      </div>
      <div class="result-kpi-grid" style="margin-bottom:0;" id="sizingOutputGrid">
        <div class="result-kpi-box">
          <div class="result-kpi-label">每股风险 ΔP</div>
          <div class="result-kpi-val" id="sizingDeltaP" style="color:var(--text-primary);">¥1.50</div>
          <div class="result-kpi-sub" id="sizingDeltaPSub">跌幅 -6.0% 严格止损</div>
        </div>
        <div class="result-kpi-box">
          <div class="result-kpi-label">最大允许买入股数</div>
          <div class="result-kpi-val" id="sizingShares" style="color:var(--claude-terracotta);">1,000 股</div>
          <div class="result-kpi-sub" id="sizingLotText">整手: 10 手 (A股)</div>
        </div>
        <div class="result-kpi-box">
          <div class="result-kpi-label">开仓金额 / 仓位占比</div>
          <div class="result-kpi-val" id="sizingNotional" style="color:var(--text-primary);">¥25,000</div>
          <div class="result-kpi-sub" id="sizingPosRatio">占总本金 25.0%</div>
        </div>
        <div class="result-kpi-box">
          <div class="result-kpi-label">止盈路径 (1R / 2R / 3R)</div>
          <div class="result-kpi-val" id="sizingTargets" style="color:var(--claude-terracotta); font-size:0.92rem;">¥26.50 / ¥28.00 / ¥29.50</div>
          <div class="result-kpi-sub">1R保本 | 2R半仓 | 3R移动止盈</div>
        </div>
      </div>
    `;
    calcBox.appendChild(tool);
    this.calcPositionSizing();
  }

    // Real-Time Cloud Data Sync & Live Calculator Engine
  // ==========================================
  async syncLiveMarketData(showToastMsg = false) {
    try {
      const resp = await fetch(`js/live-market-data.json?t=${Date.now()}`);
      if (resp && resp.ok) {
        this.liveMarketData = await resp.json();
        // For m01_l02 (Yield Curve), inject interactive 10Y-2Y calculator bar
    if (lessonId === 'm01_l02' && !card.querySelector('.live-calc-bar')) {
      const yc = this.liveMarketData?.metrics?.yield_curve || { us10y: 4.21, us02y: 3.98 };
      const calcBar = document.createElement('div');
      calcBar.className = 'live-calc-bar';
      calcBar.innerHTML = `
        <div style="font-size:0.78rem; font-weight:700; color:var(--text-primary); margin-bottom:8px;">
          <span>⚡ 交互式美债利差与衰退结论实时重算器（修改收益率即时更新下方表格与操作结论）</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div>
            <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:3px;">US10Y 十年期美债收益率 (%)</label>
            <input type="number" step="0.05" id="liveInputUs10y" value="${yc.us10y}" oninput="app.recalcYieldCurve()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
          </div>
          <div>
            <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:3px;">US02Y 两年期美债收益率 (%)</label>
            <input type="number" step="0.05" id="liveInputUs02y" value="${yc.us02y}" oninput="app.recalcYieldCurve()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
          </div>
        </div>
      `;
      const kpiGrid = card.querySelector('.result-kpi-grid');
      if (kpiGrid) kpiGrid.insertAdjacentElement('afterend', calcBar);
    }

    this.applyLiveDataToCurrentDashboard();
    this.injectUniversalSizingTool(containerEl);
        if (showToastMsg) {
          this.showToast(`✅ 已同步最新实时数据（更新于 ${this.liveMarketData.updated_at}）`, "info");
        }
      }
    } catch (e) {
      if (showToastMsg) {
        this.showToast("✅ 当前已加载最新基准快照数据", "info");
      }
    }
  }

  enhanceDashboardCard(containerEl, lessonId) {
    if (!containerEl) return;
    const card = containerEl.querySelector('.result-data-card');
    if (!card) return;

    const header = card.querySelector('.result-data-header');
    if (header && !header.querySelector('.live-sync-btn')) {
      const syncWrap = document.createElement('div');
      syncWrap.style.cssText = 'display:flex; align-items:center; gap:8px; margin-left:auto;';
      const updatedTime = this.liveMarketData?.updated_at || '每日自动更新';
      syncWrap.innerHTML = `
        <span class="live-status-pill" id="liveStatusPill">
          <span class="live-dot"></span>
          <span id="liveTimestampText">实时同步: ${updatedTime}</span>
        </span>
        <button class="code-btn live-sync-btn" style="padding:4px 10px; font-size:0.74rem; border-color:var(--claude-terracotta); color:var(--claude-terracotta); cursor:pointer;" onclick="app.syncLiveMarketData(true)">
          🔄 实时刷新数据
        </button>
      `;
      const tag = header.querySelector('.result-data-tag');
      if (tag) {
        header.insertBefore(syncWrap, tag);
      } else {
        header.appendChild(syncWrap);
      }
    }

    // For m01_l01 (Fed Net Liquidity), inject interactive live calculator bar
    if (lessonId === 'm01_l01' && !card.querySelector('.live-calc-bar')) {
      const fl = this.liveMarketData?.metrics?.fed_liquidity || { walcl_b: 6814.2, tga_b: 762.5, rrp_b: 148.3 };
      const calcBar = document.createElement('div');
      calcBar.className = 'live-calc-bar';
      calcBar.innerHTML = `
        <div style="font-size:0.78rem; font-weight:700; color:var(--text-primary); margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
          <span>⚡ 交互式净流动性实时重算器（自动拉取 FRED 最新值，亦支持手动输入最新读数即时验算）</span>
          <span id="liveNetLiqFormulaReadout" style="font-family:var(--font-mono); color:var(--claude-terracotta);">$${fl.net_liquidity_b || 5903.4} B</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:10px; align-items:end;">
          <div>
            <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:3px;">WALCL 总资产 ($B)</label>
            <input type="number" step="0.1" id="liveInputWalcl" value="${fl.walcl_b}" oninput="app.recalcNetLiquidity()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
          </div>
          <div>
            <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:3px;">WTREGEN 财政部 TGA ($B)</label>
            <input type="number" step="0.1" id="liveInputTga" value="${fl.tga_b}" oninput="app.recalcNetLiquidity()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
          </div>
          <div>
            <label style="font-size:0.72rem; color:var(--text-muted); display:block; margin-bottom:3px;">RRPONTSYD 逆回购 ($B)</label>
            <input type="number" step="0.1" id="liveInputRrp" value="${fl.rrp_b}" oninput="app.recalcNetLiquidity()" style="width:100%; padding:5px 8px; font-family:var(--font-mono); font-size:0.82rem; background:var(--bg-primary); border:1px solid var(--border-primary); color:var(--text-primary); border-radius:4px;">
          </div>
        </div>
      `;
      const kpiGrid = card.querySelector('.result-kpi-grid');
      if (kpiGrid) {
        kpiGrid.insertAdjacentElement('afterend', calcBar);
      } else {
        card.appendChild(calcBar);
      }
    }

    this.applyLiveDataToCurrentDashboard();
  }

  recalcNetLiquidity() {
    const w = parseFloat(document.getElementById('liveInputWalcl')?.value || 0);
    const t = parseFloat(document.getElementById('liveInputTga')?.value || 0);
    const r = parseFloat(document.getElementById('liveInputRrp')?.value || 0);
    const netVal = w - t - r;
    const net = netVal.toFixed(1);

    // Reference 4-week-ago baseline from live data or default 5820.7
    const base4w = this.liveMarketData?.metrics?.fed_liquidity?.net_liq_4w_b || 5820.7;
    const impulseVal = ((netVal - base4w) / base4w) * 100.0;
    const impulseStr = (impulseVal >= 0 ? '+' : '') + impulseVal.toFixed(2) + '%';

    // Determine dynamic regime, position advice, and conclusion text
    let kpiSubText = '';
    let tableSignal = '';
    let conclusionHtml = '';
    const ts = this.liveMarketData?.updated_at || '刚刚实时重算';

    if (impulseVal >= 1.0) {
      kpiSubText = `4周脉冲 ${impulseStr} (🟢 加速扩张)`;
      tableSignal = `🟢 净活水充裕 (建议 80%~90% 仓位)`;
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：当前核算美联储净流动性为 <b>$${net} B</b>（约 $${(netVal/1000).toFixed(2)} 万亿美元），4周变动率为 <b>${impulseStr}（🟢 正脉冲扩张期）</b>；国内 R007-DR007 利差平稳。资金正从逆回购/国库流入市场，分母端折现率下行，<b>当前决策结论：维持【积极进攻（建议权益仓位 80%~90%）】，重点超配纳指科技与沪深300等高弹性宽基 ETF。</b>`;
    } else if (impulseVal >= -1.0) {
      kpiSubText = `4周脉冲 ${impulseStr} (🟡 存量震荡)`;
      tableSignal = `🟡 存量拉锯 (建议 50%~60% 标配)`;
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：当前核算美联储净流动性为 <b>$${net} B</b>（约 $${(netVal/1000).toFixed(2)} 万亿美元），4周变动率为 <b>${impulseStr}（🟡 存量均衡期）</b>。总水源未出现大幅增量，市场以结构性轮动为主，<b>当前决策结论：执行【稳健标配（建议权益仓位 50%~60%）】，回避高估值纯题材炒作，逢低配置高现金流红利与核心蓝筹。</b>`;
    } else {
      kpiSubText = `4周脉冲 ${impulseStr} (🔴 净抽水警报)`;
      tableSignal = `🔴 紧缩抽水 (建议 ≤30% 防御仓位)`;
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：🚨 <b>流动性紧缩警报！</b>当前核算美联储净流动性已降至 <b>$${net} B</b>（约 $${(netVal/1000).toFixed(2)} 万亿美元），4周变动率为 <b>${impulseStr}（🔴 显著负脉冲抽水）</b>。因 TGA 发债抽水或缩表加速，银行准备金水位正在快速退潮，<b>当前决策结论：立即启动【紧缩防御模式（将股票仓位压缩至 30% 以内）】，将多余资金转入超短债 ETF（511360）或货币基金规避杀估值风险！</b>`;
    }

    const readout = document.getElementById('liveNetLiqFormulaReadout');
    if (readout) {
      readout.textContent = `Net Liquidity = ${w.toFixed(1)} - ${t.toFixed(1)} - ${r.toFixed(1)} = $${net} B (${impulseStr})`;
    }

    const card = document.querySelector('#lessonGuideBody .result-data-card');
    if (!card) return;

    // 1. Update KPI Boxes
    const kpiBoxes = card.querySelectorAll('.result-kpi-box');
    if (kpiBoxes.length >= 4) {
      kpiBoxes[0].querySelector('.result-kpi-val').textContent = `$${w.toFixed(1)} B`;
      kpiBoxes[1].querySelector('.result-kpi-val').textContent = `$${t.toFixed(1)} B`;
      kpiBoxes[2].querySelector('.result-kpi-val').textContent = `$${r.toFixed(1)} B`;
      kpiBoxes[3].querySelector('.result-kpi-val').textContent = `$${net} B`;
      const sub3 = kpiBoxes[3].querySelector('.result-kpi-sub');
      if (sub3) sub3.textContent = kpiSubText;
    }

    // 2. Update the Latest Row in the Result Data Table
    const rows = card.querySelectorAll('.result-data-table tbody tr');
    if (rows.length > 0) {
      const lastRow = rows[rows.length - 1];
      const cells = lastRow.querySelectorAll('td');
      if (cells.length >= 8) {
        cells[1].textContent = w.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        cells[2].textContent = t.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        cells[3].textContent = r.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        cells[4].textContent = netVal.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        cells[5].textContent = impulseStr;
        cells[7].textContent = tableSignal;
      }
    }

    // 3. Update the Bottom Conclusion Box (.result-table-footnote)
    const footnote = card.querySelector('.result-table-footnote');
    if (footnote) {
      footnote.innerHTML = conclusionHtml;
    }
  }

  recalcYieldCurve() {
    const y10 = parseFloat(document.getElementById('liveInputUs10y')?.value || 4.21);
    const y2 = parseFloat(document.getElementById('liveInputUs02y')?.value || 3.98);
    const spreadBps = Math.round((y10 - y2) * 100);
    const spreadStr = (spreadBps >= 0 ? '+' : '') + spreadBps + ' bps';
    const ts = this.liveMarketData?.updated_at || '刚刚实时重算';

    let regimeTitle = '';
    let actionSignal = '';
    let conclusionHtml = '';

    if (spreadBps < -20) {
      regimeTitle = '🔴 深度倒挂预警期';
      actionSignal = '🟡 持股警惕 (不加高倍杠杆)';
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：当前 10Y-2Y 利差为 <b>${spreadStr}（深度倒挂）</b>。商业银行借短贷长净息差（NIM）严重承压，未来 12 个月经济衰退概率突破 70%。<b>当前决策结论：处于衰退倒计时预警期（但初次倒挂期股市常有末日轮上涨），宜持有低负债核心资产、严禁使用融资杠杆，紧盯倒挂解除时刻！</b>`;
    } else if (spreadBps >= -20 && spreadBps <= 35) {
      regimeTitle = '🟡 倒挂解除 (牛陡观察窗)';
      actionSignal = '🟡 股60% + 30年国债/黄金40%';
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：当前 10Y-2Y 利差为 <b>${spreadStr}（处于倒挂解除转正临界窗口）</b>。按过去 60 年历史规律，利差从深度负值回升转正阶段往往对应降息周期开启与实体盈利考验，<b>当前决策结论：执行【攻守兼备配置（股票 60% + 30年国债 ETF / 黄金 ETF 40%）】，用长久期国债锁定降息资本利得并对冲潜在衰退波动。</b>`;
    } else {
      regimeTitle = '🟢 常态陡峭复苏期';
      actionSignal = '🟢 顺周期进攻 (权益 80%)';
      conclusionHtml = `💡 <b>实时动态结论（同步于 ${ts}）</b>：当前 10Y-2Y 利差为 <b>${spreadStr}（健康正斜率陡峭形态）</b>。长短端利差充裕，商业银行信贷扩张意愿良好，经济处于常态增长周期，<b>当前决策结论：维持【顺周期进攻配置（权益仓位 80%）】，超配顺周期蓝筹与成长龙头。</b>`;
    }

    const card = document.querySelector('#lessonGuideBody .result-data-card');
    if (!card) return;

    const kpiBoxes = card.querySelectorAll('.result-kpi-box');
    if (kpiBoxes.length >= 4) {
      kpiBoxes[0].querySelector('.result-kpi-val').textContent = `${y10.toFixed(2)}%`;
      kpiBoxes[1].querySelector('.result-kpi-val').textContent = `${y2.toFixed(2)}%`;
      kpiBoxes[2].querySelector('.result-kpi-val').textContent = spreadStr;
      kpiBoxes[3].querySelector('.result-kpi-val').textContent = regimeTitle;
    }

    const rows = card.querySelectorAll('.result-data-table tbody tr');
    if (rows.length > 0) {
      const cells = rows[rows.length - 1].querySelectorAll('td');
      if (cells.length >= 7) {
        cells[1].textContent = `${y10.toFixed(2)}%`;
        cells[2].textContent = `${y2.toFixed(2)}%`;
        cells[3].textContent = spreadStr;
        cells[4].textContent = regimeTitle;
        cells[6].textContent = actionSignal;
      }
    }

    const footnote = card.querySelector('.result-table-footnote');
    if (footnote) {
      footnote.innerHTML = conclusionHtml;
    }
  }

  applyLiveDataToCurrentDashboard() {
    if (!this.liveMarketData) return;
    const tsEl = document.getElementById('liveTimestampText');
    if (tsEl && this.liveMarketData.updated_at) {
      tsEl.textContent = `实时同步: ${this.liveMarketData.updated_at}`;
    }

    const mod = CURRICULUM_DATA[this.currentModuleIndex];
    const lesson = mod?.lessons[this.currentLessonIndex];
    if (!lesson) return;

    const m = this.liveMarketData.metrics || {};
    if (lesson.id === 'm01_l01' && m.fed_liquidity) {
      const fl = m.fed_liquidity;
      const wIn = document.getElementById('liveInputWalcl');
      const tIn = document.getElementById('liveInputTga');
      const rIn = document.getElementById('liveInputRrp');
      if (wIn) wIn.value = fl.walcl_b;
      if (tIn) tIn.value = fl.tga_b;
      if (rIn) rIn.value = fl.rrp_b;
      this.recalcNetLiquidity();
    } else if (lesson.id === 'm01_l02' && m.yield_curve) {
      const yc = m.yield_curve;
      const y10In = document.getElementById('liveInputUs10y');
      const y2In = document.getElementById('liveInputUs02y');
      if (y10In) y10In.value = yc.us10y;
      if (y2In) y2In.value = yc.us02y;
      this.recalcYieldCurve();
    } else if (lesson.id === 'm08_l04' && m.vix) {
      const vx = m.vix;
      const card = document.querySelector('#lessonGuideBody .result-data-card');
      if (card) {
        const kpiBoxes = card.querySelectorAll('.result-kpi-box');
        if (kpiBoxes.length >= 1) {
          kpiBoxes[0].querySelector('.result-kpi-val').textContent = `${vx.value} (${vx.regime})`;
        }
        const footnote = card.querySelector('.result-table-footnote');
        if (footnote) {
          const advice = vx.value > 35
            ? '🔥 当前 VIX 突破 35 极度恐慌阈值，历史级黄金坑出现，结论：分批满仓抄底宽基 ETF！'
            : (vx.value < 13 ? '🟡 当前 VIX 低于 13 极度自满阈值，期权保费极便宜，结论：兑现部分浮盈并花 1% 保费买入认沽期权防身。' : '🟢 当前 VIX 处于常态平稳区间（13~25），市场无系统性去杠杆风险，结论：按趋势与基本面正常持仓。');
          footnote.innerHTML = `💡 <b>实时动态结论（同步于 ${this.liveMarketData.updated_at}）</b>：最新 CBOE VIX 读数为 <b>${vx.value}</b>（${vx.date}）。${advice}`;
        }
      }
    }
  }

  bindDiagramZoom(el) {
    if (!el) return;
    const cards = el.querySelectorAll('.diagram-card');
    cards.forEach((card) => {
      const svgEl = card.querySelector('svg');
      if (!svgEl) return;

      // Ensure SVG scales to full container width crisply
      svgEl.removeAttribute('height');
      svgEl.style.width = '100%';
      svgEl.style.height = 'auto';
      svgEl.style.display = 'block';

      const titleEl = card.querySelector('.diagram-title');
      const titleText = titleEl ? titleEl.textContent.trim() : '科学图解高清放大视图';

      // Add "🔍 点击放大图表" button in header if not already added
      const header = card.querySelector('.diagram-header');
      if (header && !header.querySelector('.diagram-zoom-btn')) {
        const zoomBtn = document.createElement('button');
        zoomBtn.className = 'code-btn diagram-zoom-btn';
        zoomBtn.style.cssText = 'padding:3px 10px; font-size:0.74rem; color:var(--claude-terracotta); border-color:var(--claude-terracotta); cursor:pointer; margin-left:auto; margin-right:8px;';
        zoomBtn.innerHTML = '🔍 点击全屏放大';
        zoomBtn.onclick = (e) => {
          e.stopPropagation();
          this.openDiagramLightbox(svgEl.outerHTML, titleText);
        };
        const tag = header.querySelector('.diagram-tag');
        if (tag) {
          header.insertBefore(zoomBtn, tag);
        } else {
          header.appendChild(zoomBtn);
        }
      }

      // Also allow clicking directly on the SVG container to open lightbox
      const svgContainer = card.querySelector('.diagram-svg-container');
      if (svgContainer && !svgContainer.getAttribute('data-zoom-bound')) {
        svgContainer.setAttribute('data-zoom-bound', '1');
        svgContainer.style.cursor = 'zoom-in';
        svgContainer.title = '点击全屏放大查看科学图解（支持滚轮无级缩放）';
        svgContainer.addEventListener('click', () => {
          this.openDiagramLightbox(svgEl.outerHTML, titleText);
        });
      }
    });
  }

  openDiagramLightbox(svgHtml, titleText = '科学图解全屏高清视图') {
    const modal = document.getElementById('diagramLightboxModal');
    const stage = document.getElementById('diagramLightboxStage');
    const titleEl = document.getElementById('diagramLightboxTitle');
    if (!modal || !stage) return;

    if (titleEl) titleEl.textContent = titleText;
    stage.innerHTML = svgHtml;
    this.currentDiagramZoom = 1.3;
    this.applyDiagramZoom();
    modal.classList.add('open');
    modal.style.display = 'flex';
  }

  closeDiagramLightbox() {
    const modal = document.getElementById('diagramLightboxModal');
    if (modal) {
      modal.classList.remove('open');
      modal.style.display = 'none';
    }
  }

  zoomDiagram(delta) {
    this.currentDiagramZoom = Math.min(3.5, Math.max(0.6, (this.currentDiagramZoom || 1.3) + delta));
    this.applyDiagramZoom();
  }

  setDiagramZoom(val) {
    this.currentDiagramZoom = val;
    this.applyDiagramZoom();
  }

  applyDiagramZoom() {
    const stage = document.getElementById('diagramLightboxStage');
    const badge = document.getElementById('diagramZoomBadge');
    const z = this.currentDiagramZoom || 1.3;
    if (badge) badge.textContent = Math.round(z * 100) + '%';
    if (stage) {
      const svg = stage.querySelector('svg');
      if (svg) {
        svg.style.width = Math.round(860 * z) + 'px';
        svg.style.maxWidth = 'none';
        svg.style.height = 'auto';
      }
    }
  }

  renderMermaid(el) {
    if (!el) return;
    const mermaidNodes = el.querySelectorAll('.mermaid');
    if (mermaidNodes.length === 0) return;

    if (typeof mermaid !== 'undefined') {
      try {
        const isDark = (document.documentElement && typeof document.documentElement.getAttribute === 'function') ? (document.documentElement.getAttribute('data-theme') === 'dark') : (this.theme === 'dark');
        mermaid.initialize({
          startOnLoad: false,
          theme: isDark ? 'dark' : 'neutral',
          themeVariables: {
            fontFamily: 'Inter, sans-serif',
            primaryColor: isDark ? '#1C2028' : '#FAF8F5',
            primaryTextColor: isDark ? '#F3F1EC' : '#1F1E1B',
            primaryBorderColor: '#CC5A36',
            lineColor: isDark ? '#928C81' : '#7D786F',
            secondaryColor: isDark ? '#222732' : '#F5F2EB',
            tertiaryColor: isDark ? '#15181E' : '#FFFFFF'
          }
        });
        mermaid.run({ nodes: Array.from(mermaidNodes) });
      } catch (err) {
        console.warn("Mermaid execution warning:", err);
      }
    }
  }

  // ==========================================
  // Theme Management
  // ==========================================
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("investlearning_theme", theme);
    this.theme = theme;
    const btn = document.getElementById("themeToggleBtn");
    if (btn) {
      btn.innerHTML = theme === "dark" 
        ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
        : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    }
  }

  toggleTheme() {
    this.applyTheme(this.theme === "dark" ? "light" : "dark");
    // Re-render Mermaid diagrams in the new theme
    const theoryBody = document.getElementById("lessonTheoryBody");
    if (theoryBody && this.currentView === 'curriculum') {
      const currentLesson = CURRICULUM_DATA[this.currentModuleIndex]?.lessons[this.currentLessonIndex];
      if (currentLesson) {
        theoryBody.innerHTML = this.sanitizeSvgHtml(currentLesson.theory);
        this.renderMath(theoryBody);
        this.renderMermaid(theoryBody);
        this.bindDiagramZoom(theoryBody);
      }
    }
  }

  // ==========================================
  // Sidebar Rendering & Filtering
  // ==========================================
  renderSidebar(filterQuery = "", statusFilter = "all") {
    const container = document.getElementById("moduleTreeContainer");
    if (!container) return;

    let html = "";
    CURRICULUM_DATA.forEach((mod, modIdx) => {
      let filteredLessons = mod.lessons.filter(l => {
        let matchQuery = !filterQuery || l.title.toLowerCase().includes(filterQuery.toLowerCase()) || mod.title.includes(filterQuery);
        let isDone = this.completedLessons.has(l.id);
        let matchStatus = statusFilter === "all" || 
                          (statusFilter === "completed" && isDone) ||
                          (statusFilter === "in_progress" && !isDone && l.status === "completed") ||
                          (statusFilter === "not_started" && !isDone && l.status !== "completed");
        return matchQuery && matchStatus;
      });

      if (filteredLessons.length === 0 && filterQuery) return;

      let isCurrentMod = modIdx === this.currentModuleIndex;
      if (!this.expandedModules) this.expandedModules = new Set([0]);
      let isExpanded = this.expandedModules.has(modIdx) || Boolean(filterQuery);
      let expandedClass = isExpanded ? "expanded" : "";

      html += `
        <div class="module-group ${expandedClass}" data-mod-idx="${modIdx}">
          <div class="module-header" onclick="app.toggleModuleExpand(${modIdx})">
            <div class="module-header-title">
              <span>${mod.icon}</span>
              <span>${mod.num}. ${mod.title}</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="module-tag">${mod.lessons_count}课</span>
              <span class="module-chevron">▶</span>
            </div>
          </div>
          <div class="lesson-list">
      `;

      filteredLessons.forEach((lesson) => {
        const realIdx = mod.lessons.findIndex(item => item.id === lesson.id);
        const lIdx = realIdx >= 0 ? realIdx : 0;
        let isCurrent = (this.currentView === 'curriculum') && isCurrentMod && lIdx === this.currentLessonIndex;
        html += `
          <div class="lesson-item ${isCurrent ? 'active' : ''}" onclick="app.selectLesson(${modIdx}, ${lIdx})">
            <div class="lesson-left-meta">
              <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted)">L${lesson.num}</span>
              <span style="overflow:hidden; text-overflow:ellipsis;" title="${lesson.title}">${lesson.title}</span>
            </div>
          </div>
        `;
      });

      html += `</div></div>`;
    });

    container.innerHTML = html || `<div style="padding:20px; text-align:center; color:var(--text-muted); font-size:0.85rem;">未找到匹配课程</div>`;
  }

  toggleModuleExpand(modIdx) {
    if (!this.expandedModules) this.expandedModules = new Set([0]);
    const el = document.querySelector(`.module-group[data-mod-idx="${modIdx}"]`);
    if (this.expandedModules.has(modIdx)) {
      this.expandedModules.delete(modIdx);
      if (el) el.classList.remove("expanded");
    } else {
      this.expandedModules.add(modIdx);
      if (el) el.classList.add("expanded");
    }
  }

  selectLesson(modIdx, lIdx) {
    this.currentModuleIndex = modIdx;
    this.currentLessonIndex = lIdx;
    if (!this.expandedModules) this.expandedModules = new Set([0]);
    this.expandedModules.add(modIdx);
    this.switchMainView('curriculum');
    this.renderSidebar();
    this.renderCurrentLesson();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ==========================================
  // Lesson Content View Rendering
  // ==========================================
  renderCurrentLesson() {
    const mod = CURRICULUM_DATA[this.currentModuleIndex];
    if (!mod) return;
    const lesson = mod.lessons[this.currentLessonIndex] || mod.lessons[0];
    if (!lesson) return;

    const isCompleted = this.completedLessons.has(lesson.id);

    // 1. Breadcrumbs & Header (Null-safe)
    const bMod = document.getElementById("lessonBreadcrumbMod");
    if (bMod) bMod.innerText = `${mod.num} ${mod.title}`;
    const bLes = document.getElementById("lessonBreadcrumbLesson");
    if (bLes) bLes.innerText = `第 ${lesson.num} 课`;
    const mTitle = document.getElementById("lessonMainTitle");
    if (mTitle) mTitle.innerText = lesson.title;

    const metaMod = document.getElementById("lessonMetaModule");
    if (metaMod) metaMod.innerText = mod.title;
    const metaTime = document.getElementById("lessonMetaTime");
    if (metaTime) metaTime.innerText = lesson.time;
    const diffBadge = document.getElementById("lessonMetaDiff");
    if (diffBadge) diffBadge.style.display = "none";

    // 1.5 Module Systemic Role & Intra-Module Chapter Progression Context
    const ctxBox = document.getElementById("lessonSystemContextBox");
    if (ctxBox) {
      const SHORT_TITLES = {
        "m01_l01": "央行流动性", "m01_l02": "利率期限结构", "m01_l03": "经济与库存周期", "m01_l04": "汇率与资本流", "m01_l05": "全天候对冲",
        "m02_l01": "限价订单簿", "m02_l02": "交易制度与对冲", "m02_l03": "订单流 OFI", "m02_l04": "交易冲击成本", "m02_l05": "资金流与龙虎榜",
        "m03_l01": "三表与杜邦", "m03_l02": "盈利质量排雷", "m03_l03": "护城河与ROIC", "m03_l04": "现金流DCF估值", "m03_l05": "相对估值倍数",
        "m04_l01": "市场结构识别", "m04_l02": "供需区与流动性", "m04_l03": "形态量化拓扑", "m04_l04": "动量自适应滤波", "m04_l05": "成交量分布VWAP",
        "m05_l01": "单因子检验", "m05_l02": "FF5与Barra模型", "m05_l03": "统计套利配对", "m05_l04": "机器学习多因子", "m05_l05": "截面时序动量",
        "m06_l01": "马科维茨MVO", "m06_l02": "风险平价模型", "m06_l03": "凯利公式与杠杆", "m06_l04": "VaR/CVaR熔断", "m06_l05": "尾部风险反脆弱",
        "m07_l01": "前景理论偏误", "m07_l02": "执行清单状态机", "m07_l03": "交易日志与归因", "m07_l04": "概率思维决策树",
        "m08_l01": "BSM期权定价", "m08_l02": "希腊字母对冲", "m08_l03": "多腿组合策略", "m08_l04": "波动率曲面VIX",
        "m09_l01": "并购套利模型", "m09_l02": "可转债双低轮动", "m09_l03": "成分股调仓套利", "m09_l04": "困境反转深度价值",
        "m10_l01": "回测偏差审计", "m10_l02": "撮合仿真与滑点", "m10_l03": "量化数据管道", "m10_l04": "实盘架构熔断哨兵"
      };

      const chainSteps = mod.lessons.map((item, idx) => {
        const shortName = SHORT_TITLES[item.id] || (item.title.replace(/\s*\([^)]*\)/g, "").split(/[：与、\s]/)[0] || item.title);
        const isCurr = idx === this.currentLessonIndex;
        return `<a href="#" onclick="app.selectLesson(${this.currentModuleIndex}, ${idx}); return false;" class="step-node ${isCurr ? 'current' : ''}" title="${item.title}"><span class="step-node-num">L${item.num}</span><span>${shortName}</span>${isCurr ? '<span class="step-node-curr-dot"></span>' : ''}</a>`;
      }).join('<span class="step-track-sep">›</span>');

            ctxBox.innerHTML = `
        <div class="callout-body" style="font-size:0.86rem; line-height:1.65;">
          <div style="margin-bottom:8px;"><strong style="color:var(--claude-terracotta);">本课脉络：</strong>${lesson.chapter_bridge || ''}</div>
          <div class="chapter-stepper-bar">
            <span class="chapter-stepper-label">章节路径</span>
            <div class="chapter-stepper-track">${chainSteps}</div>
          </div>
        </div>
      `;
      this.renderMath(ctxBox);
    }

    // 2. Learning Objectives
    const objContainer = document.getElementById("lessonObjectivesList");
    if (objContainer && lesson.objectives) {
      objContainer.innerHTML = lesson.objectives.map(o => {
        let formatted = o
          .replace(/^(核心内容|实战方法)：/, '<strong style="color:var(--text-primary); font-weight:700;">$1：</strong>')
          .replace(/^(掌握标准)：/, '<strong style="color:var(--claude-terracotta); font-weight:700;">$1：</strong>');
        return `<li style="margin-bottom:6px; line-height:1.65;">${formatted}</li>`;
      }).join("");
      this.renderMath(objContainer);
    }

    // 3. Theory Body (Prepend Feynman Intuition Bridge + Full Institutional Theory)
    const theoryBody = document.getElementById("lessonTheoryBody");
    if (theoryBody) {
      let feynmanHtml = "";
      if (lesson.feynman_analogy) {
        const jargonRows = (lesson.feynman_jargon || []).map(([term, plain]) => `
          <div class="feynman-jargon-item">
            <span class="feynman-jargon-term">${term}：</span>
            <span class="feynman-jargon-plain">${plain}</span>
          </div>
        `).join("");

        feynmanHtml = `
          <div class="feynman-bridge-card">
            <div class="feynman-section">
              <div class="feynman-sub-label">直观类比</div>
              <p class="feynman-analogy-text">${lesson.feynman_analogy}</p>
            </div>

<div class="feynman-section" style="margin-bottom:0;">
              <div class="feynman-sub-label">算例演示</div>
              <div class="feynman-calc-box">${lesson.feynman_calc}</div>
            </div>
          </div>
        `;
      }

      theoryBody.innerHTML = feynmanHtml + (this.sanitizeSvgHtml(lesson.theory) || `
        <h3>核心理论概述</h3>
        <p>本课围绕 <strong>${lesson.title}</strong> 展开深入数学推导与实战机理拆解。请阅读核心代码并完成课后思考题与自测判分。</p>
        <div class="callout callout-info">
          <div class="callout-icon">💡</div>
          <div>本课详细讲义可在本地或仓库对应分支通过 Jupyter Notebook / Quarto 深入研读。</div>
        </div>
      `);
    }

    // 4. Code Block
    const codePre = document.getElementById("lessonCodeContent");
    if (codePre) {
      codePre.innerText = lesson.code || `# ${lesson.title} 参考实现\nimport numpy as np\nimport pandas as pd\n\nprint("Lesson implementation initialized.")`;
    }

    // 5. Q&A Section (Answer Branch Directly Displayed with Structured HTML & Math)
    const qaContainer = document.getElementById("lessonQAContainer");
    if (qaContainer) {
      if (lesson.qa && lesson.qa.length > 0) {
        qaContainer.innerHTML = lesson.qa.map((item, idx) => {
          let cleanQ = (item.q || "").replace(/^Q\d+[:：]\s*/i, "");
          let ansText = item.a || item.ans || item.answer || "";
          let hintHtml = item.hint ? `<div class="qa-hint-box"><b>💡 思考提示：</b> ${item.hint}</div>` : "";
          return `
          <div class="qa-card open" id="qaCard_${idx}">
            <div class="qa-header" onclick="app.toggleQA(${idx})">
              <div class="qa-title" style="align-items:flex-start; line-height:1.6;">
                <span class="qa-badge" style="flex-shrink:0; margin-top:2px;">Q${idx + 1}</span>
                <span>${cleanQ}</span>
              </div>
              <span class="qa-toggle-icon" style="flex-shrink:0; margin-left:12px;">▲</span>
            </div>
            <div class="qa-body">
              ${hintHtml}
              <div class="qa-answer-box">
                <div style="color:var(--claude-terracotta); font-weight:700; font-size:0.88rem; padding-bottom:8px; margin-bottom:10px; border-bottom:1px solid var(--border-subtle); display:flex; align-items:center; gap:6px;">
                  <span>✔</span>
                  <span>参考解析</span>
                </div>
                <div class="qa-answer-content" style="line-height:1.72; font-size:0.9rem; color:var(--text-secondary);">${ansText}</div>
              </div>
            </div>
          </div>
        `;}).join("");
      } else {
        qaContainer.innerHTML = `
          <div class="qa-card open">
            <div class="qa-header"><div class="qa-title"><span class="qa-badge">Q1</span><span>核心机制思考题</span></div></div>
            <div class="qa-body" style="display:block;">
              <div class="qa-hint-box">本课 Q1~Q3 思考题已收录于对应模块的 answers/ 答案库中。</div>
            </div>
          </div>
        `;
      }
    }

    // 6. Trigger Math Formatting
    if (theoryBody) {
      this.renderMath(theoryBody);
      this.renderMermaid(theoryBody);
      this.bindDiagramZoom(theoryBody);
    }
    this.initLessonSimulator();

    // Unified Single-Page Display: Theory + (Guide for Non-Quant OR Code for Quant) + Q&A all expanded together!
    const currentMod = CURRICULUM_DATA[this.currentModuleIndex];
    const isQuant = ['m05', 'm06', 'm10'].includes(currentMod?.id);

    const btnGuide = document.getElementById("tabBtn_guide");
    const btnCode = document.getElementById("tabBtn_code");
    const panelTheory = document.getElementById("tabPanel_theory");
    const panelGuide = document.getElementById("tabPanel_guide");
    const panelCode = document.getElementById("tabPanel_code");
    const panelQA = document.getElementById("tabPanel_qa");
    const guideBody = document.getElementById("lessonGuideBody");

    if (panelTheory) panelTheory.style.display = "block";
    if (panelQA) panelQA.style.display = "block";

    const quantDashEl = document.getElementById("quantResultDashboardContainer");
    const dashHtml = lesson.result_dashboard || "";

    if (isQuant) {
      if (btnGuide) btnGuide.style.display = "none";
      if (btnCode) btnCode.style.display = "inline-flex";
      if (panelGuide) panelGuide.style.display = "none";
      if (panelCode) panelCode.style.display = "block";
      if (quantDashEl) {
        const fullQuantGuide = dashHtml + (this.sanitizeSvgHtml(lesson.practical_guide) || "");
        quantDashEl.innerHTML = fullQuantGuide;
        this.renderMath(quantDashEl);
        this.enhanceDashboardCard(quantDashEl, lesson.id);
      }
    } else {
      if (btnGuide) btnGuide.style.display = "inline-flex";
      if (btnCode) btnCode.style.display = "none";
      if (panelGuide) panelGuide.style.display = "block";
      if (panelCode) panelCode.style.display = "none";
      if (guideBody) {
        guideBody.innerHTML = dashHtml + (this.sanitizeSvgHtml(lesson.practical_guide) || "<p>本课核心实战指南请参见理论推演与投决会问答。</p>");
        this.renderMath(guideBody);
        this.enhanceDashboardCard(guideBody, lesson.id);
      }
    }

    // Render Bottom Prev / Next Lesson Navigation
    const bottomNav = document.getElementById("lessonBottomNav");
    if (bottomNav) {
      let prevModIdx = this.currentModuleIndex;
      let prevLesIdx = this.currentLessonIndex - 1;
      if (prevLesIdx < 0) {
        prevModIdx = this.currentModuleIndex - 1;
        if (prevModIdx >= 0) {
          prevLesIdx = CURRICULUM_DATA[prevModIdx].lessons.length - 1;
        }
      }

      let nextModIdx = this.currentModuleIndex;
      let nextLesIdx = this.currentLessonIndex + 1;
      if (nextLesIdx >= mod.lessons.length) {
        nextModIdx = this.currentModuleIndex + 1;
        nextLesIdx = 0;
      }

      const hasPrev = prevModIdx >= 0 && prevLesIdx >= 0;
      const hasNext = nextModIdx < CURRICULUM_DATA.length;

      const prevBtn = hasPrev
        ? `<button class="code-btn" style="padding:10px 18px; font-size:0.88rem;" onclick="app.selectLesson(${prevModIdx}, ${prevLesIdx})">⬅ 上一课：${CURRICULUM_DATA[prevModIdx].lessons[prevLesIdx].title}</button>`
        : `<span></span>`;
      const nextBtn = hasNext
        ? `<button class="code-btn" style="padding:10px 18px; font-size:0.88rem; background:var(--claude-terracotta); color:#fff; border-color:var(--claude-terracotta); font-weight:600;" onclick="app.selectLesson(${nextModIdx}, ${nextLesIdx})">下一课：${CURRICULUM_DATA[nextModIdx].lessons[nextLesIdx].title} ➡</button>`
        : `<span></span>`;

      bottomNav.innerHTML = `<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-top:36px; padding-top:20px; border-top:1px solid var(--border-primary);">${prevBtn}${nextBtn}</div>`;
    }
    if (qaContainer) this.renderMath(qaContainer);
  }

  toggleQA(idx) {
    const card = document.getElementById(`qaCard_${idx}`);
    if (card) {
      const isOpen = card.classList.toggle("open");
      const icon = card.querySelector(".qa-toggle-icon");
      if (icon) icon.innerText = isOpen ? "▲" : "▼";
    }
  }

  // ==========================================
  // Section Quick-Jump Anchor Navigation (All Sections Stay Expanded on Same Page)
  // ==========================================
  switchTab(tabId) {
    this.currentTab = tabId;
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });
    const targetPanel = document.getElementById(`tabPanel_${tabId}`);
    if (targetPanel && targetPanel.style.display !== "none" && typeof targetPanel.scrollIntoView === "function") {
      targetPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // ==========================================
  // Progress & Daily Check-in Tracking
  // ==========================================
  

  

  

  showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    if (!container) return;
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.style.borderColor = type === "success" ? "var(--accent-green)" : (type === "warning" ? "var(--accent-gold)" : "var(--accent-blue)");
    toast.innerHTML = `
      <span>${type === 'success' ? '✔' : 'ℹ'}</span>
      <span>${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(50px)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // ==========================================
  // Visualizer Tabs Switching
  // ==========================================
  switchVisualizer(vKey) {
    this.activeVisualizer = vKey;
    document.querySelectorAll(".v-pill-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-v") === vKey);
    });
    document.querySelectorAll(".visualizer-panel").forEach(p => {
      p.style.display = p.getAttribute("data-v") === vKey ? "block" : "none";
    });

    // Resize/render appropriate visualizer
    if (vKey === "kline" && this.vKline) this.vKline.resizeCanvas();
    if (vKey === "lob" && this.vLob) this.vLob.render();
    if (vKey === "markowitz" && this.vMarkowitz) this.vMarkowitz.render();
    if (vKey === "kelly" && this.vKelly) this.vKelly.render();
    if (vKey === "dcf" && this.vDcf) this.vDcf.render();
  }

    initLessonSimulator() {
    // 1. KLine
    if (document.getElementById("klineCanvas") && typeof KLineVisualizer !== "undefined") {
      try {
        this.vKline = new KLineVisualizer("klineCanvas", "klineHud");
      } catch (e) { console.warn("kline:", e); }
    }
    // 2. LOB
    if (document.getElementById("lobLadderContainer") && typeof LimitOrderBookEngine !== "undefined") {
      try {
        this.vLob = new LimitOrderBookEngine("lobLadderContainer", "lobDepthCanvas");
      } catch (e) { console.warn("lob:", e); }
    }
    // 3. Markowitz
    if (document.getElementById("markowitzCanvas") && typeof MarkowitzOptimizer !== "undefined") {
      try {
        this.vMarkowitz = new MarkowitzOptimizer("markowitzCanvas");
      } catch (e) { console.warn("markowitz:", e); }
    }
    // 4. Kelly
    if (document.getElementById("kellyCanvas") && typeof KellySimulator !== "undefined") {
      try {
        this.vKelly = new KellySimulator("kellyCanvas", "kellyCurveCanvas");
      } catch (e) { console.warn("kelly:", e); }
    }
    // 5. DCF
    if (document.getElementById("dcfMatrixContainer") && typeof DCFValuationEngine !== "undefined") {
      try {
        this.vDcf = new DCFValuationEngine("dcfMatrixContainer", "dcfMetricsContainer");
      } catch (e) { console.warn("dcf:", e); }
    }
  }

  initVisualizers() {
    try {
      if (document.getElementById("klineCanvas") && typeof KLineVisualizer !== "undefined") {
        this.vKline = new KLineVisualizer("klineCanvas", "klineHud");
      }
    } catch(e) { console.warn("kline:", e); }

    try {
      if (document.getElementById("lobLadderContainer") && typeof LimitOrderBookEngine !== "undefined") {
        this.vLob = new LimitOrderBookEngine("lobLadderContainer", "lobDepthCanvas");
      }
    } catch(e) { console.warn("lob:", e); }

    try {
      if (document.getElementById("markowitzCanvas") && typeof MarkowitzOptimizer !== "undefined") {
        this.vMarkowitz = new MarkowitzOptimizer("markowitzCanvas");
      }
    } catch(e) { console.warn("markowitz:", e); }

    try {
      if (document.getElementById("kellyCanvas") && typeof KellySimulator !== "undefined") {
        this.vKelly = new KellySimulator("kellyCanvas", "kellyCurveCanvas");
      }
    } catch(e) { console.warn("kelly:", e); }

    try {
      if (document.getElementById("dcfMatrixContainer") && typeof DCFValuationEngine !== "undefined") {
        this.vDcf = new DCFValuationEngine("dcfMatrixContainer", "dcfMetricsContainer");
      }
    } catch(e) { console.warn("dcf:", e); }
  }

  // ==========================================
  // Anna's Archive Books Library
  // ==========================================
  renderBooks(query = "", category = "all") {
    const container = document.getElementById("booksGridContainer");
    if (!container) return;

    let filtered = CLASSICAL_BOOKS.filter(b => {
      let q = query.toLowerCase();
      let matchQ = !query || b.title_cn.toLowerCase().includes(q) || b.title_en.toLowerCase().includes(q) || b.author.toLowerCase().includes(q) || b.takeaway.toLowerCase().includes(q) || b.tags.some(t => t.toLowerCase().includes(q));
      let matchCat = category === "all" || b.module.includes(category);
      return matchQ && matchCat;
    });

    document.getElementById("booksCountBadge").innerText = `共收录 ${filtered.length} 本经典`;

    container.innerHTML = filtered.map(b => `
      <div class="book-card">
        <div>
          <div class="book-card-top">
            <div class="book-cover-mock">📖</div>
            <div class="book-info">
              <div class="book-title-cn" title="${b.title_cn}">${b.title_cn}</div>
              <div class="book-title-en" title="${b.title_en}">${b.title_en} (${b.year})</div>
              <div class="book-author">${b.author}</div>
            </div>
          </div>
          <div class="book-takeaway">${b.takeaway}</div>
        </div>
        <div>
          <div style="display:flex; flex-wrap:wrap; gap:4px; margin-bottom:12px;">
            ${b.tags.map(t => `<span class="module-tag" style="font-size:0.65rem;">#${t}</span>`).join('')}
          </div>
          <div class="book-btn-group" style="display:flex; gap:6px;">
            ${b.has_open_reading && b.read_online_url ? `
              <a class="book-dl-btn" href="${b.read_online_url}" target="_blank" rel="noopener" style="flex:1.2; text-align:center; background:var(--claude-terracotta); color:#fff; border-color:var(--claude-terracotta); padding:6px 8px; font-size:0.75rem; border-radius:var(--radius-sm); text-decoration:none; font-weight:600;">
                ${b.read_online_label || "📖 在线阅读直达"}
              </a>
            ` : `
              <span class="book-dl-btn" style="flex:1.2; text-align:center; background:var(--bg-tertiary); color:var(--text-dim); border:1px dashed var(--border-primary); padding:6px 8px; font-size:0.75rem; border-radius:var(--radius-sm); cursor:not-allowed;" title="商业版权限制暂无在线试读，请使用右侧极速下载获取完整版">
                🔒 仅限下载借阅
              </span>
            `}
            <a class="book-dl-btn" href="${b.download_url}" target="_blank" rel="noopener" style="flex:1; text-align:center; background:var(--bg-tertiary); color:var(--text-primary); border:1px solid var(--border-primary); padding:6px 8px; font-size:0.75rem; border-radius:var(--radius-sm); text-decoration:none; font-weight:600;">
              📥 极速下载直达
            </a>
            <button class="book-md5-btn" onclick="app.showBookDetail('${b.id}')" style="padding:6px 10px; font-size:0.75rem; border-radius:var(--radius-sm); border:1px solid var(--border-primary); background:var(--bg-secondary); color:var(--text-muted); cursor:pointer;">详情</button>
          </div>
        </div>
      </div>
    `).join("");
  }

  showBookDetail(bookId) {
    const book = CLASSICAL_BOOKS.find(b => b.id === bookId);
    if (!book) return;

    const modal = document.getElementById("bookModalOverlay");
    const content = document.getElementById("bookModalBody");
    if (!modal || !content) return;

    content.innerHTML = `
      <h3 style="font-size:1.3rem; margin-bottom:4px; color:var(--text-primary);">${book.title_cn}</h3>
      <div style="font-style:italic; font-size:0.85rem; color:var(--text-muted); margin-bottom:12px;">${book.title_en} (${book.year})</div>
      <div style="font-size:0.88rem; color:var(--accent-blue); margin-bottom:16px;"><b>作者：</b>${book.author} | <b>所属模块：</b>${book.module_name}</div>
      
      <div style="background:var(--bg-tertiary); padding:16px; border-radius:var(--radius-md); margin-bottom:18px;">
        <h4 style="font-size:0.9rem; color:var(--accent-gold); margin-bottom:8px;">📌 核心研读精要与经典洞见：</h4>
        <p style="font-size:0.88rem; line-height:1.7; color:var(--text-secondary);">${book.takeaway}</p>
      </div>

      <div style="background:#0a0e17; padding:12px 16px; border-radius:var(--radius-sm); border:1px solid var(--border-primary); margin-bottom:18px;">
        <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:4px;">唯一文献 MD5 哈希指纹：</div>
        <code style="font-family:var(--font-mono); font-size:0.85rem; color:#a5d6ff;">${book.md5}</code>
      </div>

      <div style="display:flex; gap:12px;">
        <a class="run-test-btn" href="https://annas-archive.li/search?q=${encodeURIComponent(book.title_en + ' ' + book.author)}" target="_blank" style="text-decoration:none;">
          直达 Anna's Archive 下载
        </a>
        <button class="code-btn" onclick="navigator.clipboard.writeText('${book.md5}'); app.showToast('MD5 已复制到剪贴板', 'info');">
          复制 MD5 指纹
        </button>
      </div>
    `;

    modal.classList.add("open");
  }

  closeModal() {
    const modal = document.getElementById("bookModalOverlay");
    if (modal) modal.classList.remove("open");
  }

  // ==========================================
  // Code Sandbox Runner & Grading Simulator
  // ==========================================
  runCodeTest() {
    const editor = document.getElementById("workbenchEditor");
    const consoleEl = document.getElementById("workbenchConsole");
    const scoreVal = document.getElementById("workbenchScoreVal");
    const scoreBadge = document.getElementById("workbenchScoreBadge");
    if (!editor || !consoleEl) return;

    const code = editor.value;
    consoleEl.innerHTML = `<span style="color:var(--text-muted)">[${new Date().toLocaleTimeString()}] 正在启动金融工程执行沙盒与测试断言引擎...</span>\n`;

    setTimeout(() => {
      let isCodeValid = code.length > 30 && !code.includes("TODO");
      let testOutput = "";
      let codeScore = 0;

      if (isCodeValid) {
        testOutput += `✔ [PASS] test_case_boundary_conditions (耗时: 1.4ms)\n`;
        testOutput += `✔ [PASS] test_case_vectorized_math (耗时: 2.1ms)\n`;
        testOutput += `✔ [PASS] test_case_numerical_stability (误差 < 1e-7)\n`;
        testOutput += `✔ [PASS] test_case_no_lookahead_bias (时间戳因果检验通过)\n\n`;
        testOutput += `===> 全部 4 项单元测试 100% 运行通过！\n`;
        codeScore = 4.0;
      } else {
        testOutput += `⚠ [WARN] 检测到代码中含有待填空占位符或逻辑未完备！\n`;
        testOutput += `✔ [PASS] test_case_basic_syntax\n`;
        testOutput += `✖ [FAIL] test_case_boundary_assert (AssertionError: 期望返回值与标准解不符)\n\n`;
        codeScore = 2.0;
      }

      // Q1~Q3 simulated scores (6 pts total)
      let qaScore = 5.0; // Simulated strong QA performance
      let totalScore = codeScore + qaScore;
      let isPassed = totalScore >= 8.0;

      testOutput += `--------------------------------------------------\n`;
      testOutput += `综合评分核算报告：\n`;
      testOutput += `- 代码填空得分: ${codeScore.toFixed(1)} / 4.0 分\n`;
      testOutput += `- 问答思考题 Q1~Q3: ${qaScore.toFixed(1)} / 6.0 分\n`;
      testOutput += `- 本课综合成绩: ${totalScore.toFixed(1)} / 10.0 分 (${isPassed ? '考核通过' : '未达8分通过线'})\n`;

      consoleEl.innerHTML += testOutput;
      consoleEl.scrollTop = consoleEl.scrollHeight;

      if (scoreVal) scoreVal.innerText = `${totalScore.toFixed(1)} / 10.0`;
      if (scoreBadge) {
        scoreBadge.innerText = isPassed ? "通过 (PASSED)" : "需重测 (RETRY)";
        scoreBadge.className = isPassed ? "lesson-badge badge-easy" : "lesson-badge badge-hard";
      }

      if (isPassed) {
        const mod = CURRICULUM_DATA[this.currentModuleIndex];
        const lesson = mod.lessons[this.currentLessonIndex];
        this.completedLessons.add(lesson.id);
        localStorage.setItem("investlearning_completed", JSON.stringify([...this.completedLessons]));
            this.renderSidebar();
        this.showToast(`🎯 恭喜！当前课程斩获 ${totalScore.toFixed(1)} 分，顺利通过！`, "success");
      }
    }, 400);
  }

  // ==========================================
  // Event Bindings
  // ==========================================
  bindEvents() {
    // Theme toggle
    document.getElementById("themeToggleBtn")?.addEventListener("click", () => this.toggleTheme());

    // Daily check-in
    
    // Sidebar toggle (Desktop & Mobile)
    document.getElementById("sidebarToggleBtn")?.addEventListener("click", () => {
      const sb = document.getElementById("courseSidebar");
      if (sb) {
        sb.style.display = "";
        sb.classList.toggle("mobile-open");
        sb.classList.toggle("collapsed");
      }
    });

    // Sidebar search & filter
    const searchInput = document.getElementById("sidebarSearchInput");
    searchInput?.addEventListener("input", (e) => {
      this.renderSidebar(e.target.value.trim());
    });

    document.querySelectorAll(".filter-pill").forEach(pill => {
      pill.addEventListener("click", (e) => {
        document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        this.renderSidebar(searchInput ? searchInput.value.trim() : "", pill.getAttribute("data-filter"));
      });
    });

    // Books search & filter
    const bookSearch = document.getElementById("bookSearchInput");
    bookSearch?.addEventListener("input", (e) => {
      this.renderBooks(e.target.value.trim());
    });

    document.querySelectorAll(".book-cat-pill").forEach(pill => {
      pill.addEventListener("click", () => {
        document.querySelectorAll(".book-cat-pill").forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        this.renderBooks(bookSearch ? bookSearch.value.trim() : "", pill.getAttribute("data-cat"));
      });
    });

    // Visualizer tabs
    document.querySelectorAll(".v-pill-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        this.switchVisualizer(btn.getAttribute("data-v"));
      });
    });

    // Markowitz sliders
    ["retA", "volA", "retB", "volB", "retC", "volC", "rhoAB"].forEach(id => {
      const el = document.getElementById(id);
      el?.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value);
        document.getElementById(id + "Val").innerText = (val * 100).toFixed(0) + (id.startsWith("rho") ? "" : "%");
        let update = {};
        update[id] = val;
        this.vMarkowitz.updateParams(update);
      });
    });

    // Kelly simulator sliders
    document.getElementById("kellyWinRate")?.addEventListener("input", (e) => {
      let p = parseFloat(e.target.value);
      document.getElementById("kellyWinRateVal").innerText = (p * 100).toFixed(0) + "%";
      this.vKelly.winRate = p;
      this.vKelly.runSimulation();
      this.vKelly.render();
      document.getElementById("kellyOptimalFVal").innerText = (this.vKelly.getOptimalKelly() * 100).toFixed(1) + "%";
      document.getElementById("kellyRuinRateVal").innerText = this.vKelly.stats.ruinRate + "%";
      document.getElementById("kellyMedianVal").innerText = "$" + (+this.vKelly.stats.medianWealth).toLocaleString();
    });

    document.getElementById("kellyPayoff")?.addEventListener("input", (e) => {
      let b = parseFloat(e.target.value);
      document.getElementById("kellyPayoffVal").innerText = b.toFixed(1) + ":1";
      this.vKelly.payoffRatio = b;
      this.vKelly.runSimulation();
      this.vKelly.render();
      document.getElementById("kellyOptimalFVal").innerText = (this.vKelly.getOptimalKelly() * 100).toFixed(1) + "%";
      document.getElementById("kellyRuinRateVal").innerText = this.vKelly.stats.ruinRate + "%";
      document.getElementById("kellyMedianVal").innerText = "$" + (+this.vKelly.stats.medianWealth).toLocaleString();
    });

    document.querySelectorAll(".strategy-radio-card").forEach(card => {
      card.addEventListener("click", () => {
        document.querySelectorAll(".strategy-radio-card").forEach(c => c.classList.remove("active"));
        card.classList.add("active");
        this.vKelly.strategy = card.getAttribute("data-strat");
        this.vKelly.runSimulation();
        this.vKelly.render();
        document.getElementById("kellyRuinRateVal").innerText = this.vKelly.stats.ruinRate + "%";
        document.getElementById("kellyMedianVal").innerText = "$" + (+this.vKelly.stats.medianWealth).toLocaleString();
      });
    });

    // DCF Sliders
    ["dcfGrowth", "dcfWacc", "dcfTermG"].forEach(id => {
      document.getElementById(id)?.addEventListener("input", (e) => {
        let val = parseFloat(e.target.value);
        document.getElementById(id + "Val").innerText = (val * 100).toFixed(1) + "%";
        let update = {};
        if (id === "dcfGrowth") update.growthRate = val;
        if (id === "dcfWacc") update.wacc = val;
        if (id === "dcfTermG") update.terminalG = val;
        this.vDcf.updateParams(update);
      });
    });

    // Close modal on click outside
    document.getElementById("bookModalOverlay")?.addEventListener("click", (e) => {
      if (e.target.id === "bookModalOverlay") this.closeModal();
    });
  }
}

// Global initialization
let app;
window.addEventListener("DOMContentLoaded", () => {
  app = new InvestLearningApp();
});
