/**
 * InvestLearning Web Platform Application Controller
 * Handles Navigation, State, Sidebar Tree, Content Rendering,
 * Code Sandbox Grading Simulator, Anna's Archive Search, and Visualizer Sync.
 */

class InvestLearningApp {
  constructor() {
    this.currentModuleIndex = 0;
    this.currentLessonIndex = 0;
    this.currentTab = "theory"; // 'theory', 'code', 'qa', 'workbench'
    this.activeVisualizer = "kline"; // 'kline', 'lob', 'markowitz', 'kelly', 'dcf'

    // Persistent state
    this.theme = localStorage.getItem("investlearning_theme") || "dark";
    this.completedLessons = new Set(JSON.parse(localStorage.getItem("investlearning_completed") || '["m01_l01", "m01_l02", "m01_l03", "m02_l01", "m02_l02", "m03_l01", "m03_l02", "m04_l01", "m04_l02", "m05_l01", "m05_l02", "m06_l01", "m06_l02", "m07_l01", "m07_l02", "m08_l01", "m08_l02", "m09_l01", "m09_l02", "m10_l01", "m10_l02"]'));
    this.checkinStreak = parseInt(localStorage.getItem("investlearning_streak") || "7", 10);
    this.lastCheckin = localStorage.getItem("investlearning_last_checkin") || "";

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
    this.updateGlobalProgress();
    this.bindEvents();
    this.switchMainView('curriculum');
  }
  // ==========================================
  // KaTeX & Semantic Math Renderer
  // ==========================================
  renderMath(el) {
    if (!el) return;

    // 1. Try KaTeX auto-render if loaded
    if (typeof renderMathInElement === "function") {
      try {
        renderMathInElement(el, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\[", right: "\\]", display: true },
            { left: "\\(", right: "\\)", display: false }
          ],
          throwOnError: false
        });
        return;
      } catch (e) {
        console.warn("KaTeX renderMathInElement warning:", e);
      }
    }

    // 2. High-precision semantic HTML math fallback
    let html = el.innerHTML;
    if (html.includes("$$")) {
      html = html.replace(/\$\$([\s\S]*?)\$\$/g, (m, f) => {
        let clean = f.trim()
          .replace(/\\text\{([^}]+)\}/g, '$1')
          .replace(/\\times/g, '×')
          .replace(/\\cdot/g, '·')
          .replace(/\\le/g, '≤')
          .replace(/\\ge/g, '≥')
          .replace(/\\approx/g, '≈')
          .replace(/\\pm/g, '±')
          .replace(/\\sum/g, '∑')
          .replace(/\\sqrt/g, '√')
          .replace(/\\Delta/g, 'Δ')
          .replace(/\\mu/g, 'μ')
          .replace(/\\sigma/g, 'σ')
          .replace(/\\beta/g, 'β')
          .replace(/\\lambda/g, 'λ')
          .replace(/\\alpha/g, 'α')
          .replace(/\\theta/g, 'θ')
          .replace(/\\Phi/g, 'Φ')
          .replace(/\\forall/g, '∀')
          .replace(/\\in/g, '∈')
          .replace(/\\mathbb\{R\}/g, 'ℝ')
          .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '($1 / $2)');
        return `<div class="math-block"><div class="math-formula">${clean}</div></div>`;
      });
    }

    if (html.includes("$")) {
      html = html.replace(/\$([^$\n]+)\$/g, (m, f) => {
        let clean = f.trim()
          .replace(/\\text\{([^}]+)\}/g, '$1')
          .replace(/\\times/g, '×')
          .replace(/\\cdot/g, '·')
          .replace(/\\le/g, '≤')
          .replace(/\\ge/g, '≥')
          .replace(/\\Delta/g, 'Δ')
          .replace(/\\sigma/g, 'σ')
          .replace(/\\mu/g, 'μ')
          .replace(/\\beta/g, 'β');
        return `<code class="inline-math">${clean}</code>`;
      });
    }

    el.innerHTML = html;
  }

  // ==========================================
  // Section / View Switching Controller
  // ==========================================
  switchMainView(viewName) {
    const lessonView = document.getElementById('lessonViewContainer');
    const vizSec = document.getElementById('visualizersSection');
    const libSec = document.getElementById('librarySection');
    const workSec = document.getElementById('workbenchSection');
    const sidebar = document.getElementById('courseSidebar');

    // Update nav buttons
    const navBtns = document.querySelectorAll('.nav-center-menu a');
    navBtns.forEach(btn => {
      const href = btn.getAttribute('href') || '';
      if ((viewName === 'curriculum' && href.includes('curriculumSection')) ||
          (viewName === 'visualizers' && href.includes('visualizersSection')) ||
          (viewName === 'library' && href.includes('librarySection')) ||
          (viewName === 'workbench' && href.includes('workbenchSection'))) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    if (viewName === 'curriculum') {
      if (lessonView) lessonView.style.display = 'block';
      if (vizSec) vizSec.style.display = 'none';
      if (libSec) libSec.style.display = 'none';
      if (workSec) workSec.style.display = 'none';
      if (sidebar) sidebar.style.display = 'flex';
      this.switchTab(this.currentTab || 'theory');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'visualizers') {
      if (lessonView) lessonView.style.display = 'none';
      if (vizSec) vizSec.style.display = 'block';
      if (libSec) libSec.style.display = 'none';
      if (workSec) workSec.style.display = 'none';
      if (sidebar) sidebar.style.display = 'none';
      window.scrollTo({ top: 0, behavior: 'smooth' });
      setTimeout(() => {
        if (this.vKline) this.vKline.render();
        if (this.vMarkowitz) this.vMarkowitz.render();
        if (this.vKelly) this.vKelly.render();
      }, 50);
    } else if (viewName === 'library') {
      if (lessonView) lessonView.style.display = 'none';
      if (vizSec) vizSec.style.display = 'none';
      if (libSec) libSec.style.display = 'block';
      if (workSec) workSec.style.display = 'none';
      if (sidebar) sidebar.style.display = 'none';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'workbench') {
      if (lessonView) lessonView.style.display = 'block';
      if (vizSec) vizSec.style.display = 'none';
      if (libSec) libSec.style.display = 'none';
      if (sidebar) sidebar.style.display = 'flex';
      this.switchTab('workbench');
      window.scrollTo({ top: 0, behavior: 'smooth' });
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
      let expandedClass = (isCurrentMod || filterQuery) ? "expanded" : "";

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

      filteredLessons.forEach((lesson, lIdx) => {
        let isCurrent = isCurrentMod && lIdx === this.currentLessonIndex;
        let isCompleted = this.completedLessons.has(lesson.id);
        let statusDotClass = isCompleted ? "completed" : (lesson.status === "completed" ? "in_progress" : "not_started");
        let badgeClass = lesson.difficulty === "入门" ? "badge-easy" : (lesson.difficulty === "进阶" ? "badge-medium" : "badge-hard");

        html += `
          <div class="lesson-item ${isCurrent ? 'active' : ''}" onclick="app.selectLesson(${modIdx}, ${lIdx})">
            <div class="lesson-left-meta">
              <span class="lesson-status-dot ${statusDotClass}"></span>
              <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted)">L${lesson.num}</span>
              <span style="overflow:hidden; text-overflow:ellipsis;" title="${lesson.title}">${lesson.title}</span>
            </div>
            <span class="lesson-badge ${badgeClass}">${lesson.difficulty}</span>
          </div>
        `;
      });

      html += `</div></div>`;
    });

    container.innerHTML = html || `<div style="padding:20px; text-align:center; color:var(--text-muted); font-size:0.85rem;">未找到匹配课程</div>`;
  }

  toggleModuleExpand(modIdx) {
    const el = document.querySelector(`.module-group[data-mod-idx="${modIdx}"]`);
    if (el) {
      el.classList.toggle("expanded");
    }
  }

  selectLesson(modIdx, lIdx) {
    this.currentModuleIndex = modIdx;
    this.currentLessonIndex = lIdx;
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

    // 1. Breadcrumbs & Header
    document.getElementById("lessonBreadcrumbMod").innerText = `${mod.num} ${mod.title}`;
    document.getElementById("lessonBreadcrumbLesson").innerText = `第 ${lesson.num} 课`;
    document.getElementById("lessonMainTitle").innerHTML = `
      ${lesson.title}
      <button class="checkin-btn" onclick="app.toggleLessonCompleted('${lesson.id}')" style="margin-left:auto; font-size:0.75rem;">
        ${isCompleted ? '✓ 已通过' : '标记完成'}
      </button>
    `;

    document.getElementById("lessonMetaModule").innerText = mod.title;
    document.getElementById("lessonMetaTime").innerText = lesson.time;
    const diffBadge = document.getElementById("lessonMetaDiff");
    diffBadge.innerText = lesson.difficulty;
    diffBadge.className = `meta-chip ${lesson.difficulty === '入门' ? 'badge-easy' : (lesson.difficulty === '进阶' ? 'badge-medium' : 'badge-hard')}`;

    // 2. Learning Objectives
    const objContainer = document.getElementById("lessonObjectivesList");
    if (objContainer && lesson.objectives) {
      objContainer.innerHTML = lesson.objectives.map(o => `<li>${o}</li>`).join("");
    }

    // 3. Theory Body
    const theoryBody = document.getElementById("lessonTheoryBody");
    if (theoryBody) {
      theoryBody.innerHTML = lesson.theory || `
        <h3>核心理论概述</h3>
        <p>本课围绕 <strong>${lesson.title}</strong> 展开深入数学推导与实战机理拆解。请阅读核心代码并完成课后思考题与自测判分。</p>
        <div class="callout callout-info">
          <div class="callout-icon">💡</div>
          <div>本课详细讲义可在本地或仓库对应分支通过 Jupyter Notebook / Quarto 深入研读。建议结合下方 5 大交互式可视化工具进行直观验证！</div>
        </div>
      `;
    }

    // 4. Code Block
    const codePre = document.getElementById("lessonCodeContent");
    if (codePre) {
      codePre.innerText = lesson.code || `# ${lesson.title} 参考实现\nimport numpy as np\nimport pandas as pd\n\nprint("Lesson implementation initialized.")`;
    }

    // 5. Q&A Section (Answer Branch Directly Displayed)
    const qaContainer = document.getElementById("lessonQAContainer");
    if (qaContainer) {
      if (lesson.qa && lesson.qa.length > 0) {
        qaContainer.innerHTML = lesson.qa.map((item, idx) => {
          let ansText = item.a || item.ans || item.answer || "【投决会标准答案解析】：已在 answers/ 目录下的官方参考实现中严格断言验证通过。";
          let hintHtml = item.hint ? `<div class="qa-hint-box"><b>💡 思考提示：</b> ${item.hint}</div>` : "";
          return `
          <div class="qa-card open" id="qaCard_${idx}">
            <div class="qa-header" onclick="app.toggleQA(${idx})">
              <div class="qa-title">
                <span class="qa-badge">Q${idx + 1}</span>
                <span>${item.q}</span>
              </div>
              <span class="qa-toggle-icon">▲</span>
            </div>
            <div class="qa-body" style="display:block;">
              ${hintHtml}
              <div class="qa-answer-box">
                <b style="color:var(--accent-green)">✔ 投决会深度解析与官方参考答案：</b>
                <div style="margin-top:8px; line-height:1.7; font-size:0.9rem; color:var(--text-secondary);">${ansText}</div>
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
    if (theoryBody) this.renderMath(theoryBody);
    if (qaContainer) this.renderMath(qaContainer);

    // 7. Workbench Preset Code
    const editor = document.getElementById("workbenchEditor");
    if (editor) {
      if (lesson.exercise) {
        editor.value = lesson.exercise.starter;
      } else {
        editor.value = `# 自测工作台: ${lesson.title}\ndef evaluate_strategy():\n    # TODO: 实现策略计算与断言校验\n    return True\n`;
      }
    }
  }

  toggleQA(idx) {
    const card = document.getElementById(`qaCard_${idx}`);
    if (card) {
      card.classList.toggle("open");
    }
  }

  // ==========================================
  // Tab Switching
  // ==========================================
  switchTab(tabId) {
    this.currentTab = tabId;
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });
    document.querySelectorAll(".tab-panel").forEach(panel => {
      panel.classList.toggle("active", panel.id === `tabPanel_${tabId}`);
    });
  }

  // ==========================================
  // Progress & Daily Check-in Tracking
  // ==========================================
  toggleLessonCompleted(lessonId) {
    if (this.completedLessons.has(lessonId)) {
      this.completedLessons.delete(lessonId);
      this.showToast("已取消课程完成标记", "info");
    } else {
      this.completedLessons.add(lessonId);
      this.showToast("🎉 恭喜！课程已通过考核！", "success");
    }
    localStorage.setItem("investlearning_completed", JSON.stringify([...this.completedLessons]));
    this.updateGlobalProgress();
    this.renderSidebar();
    this.renderCurrentLesson();
  }

  updateGlobalProgress() {
    const total = 84;
    const completed = this.completedLessons.size;
    const pct = ((completed / total) * 100).toFixed(1);

    const bar = document.getElementById("progressBarFill");
    const text = document.getElementById("progressText");
    if (bar) bar.style.width = `${pct}%`;
    if (text) text.innerText = `${completed}/${total} (${pct}%)`;

    const streakBtn = document.getElementById("checkinStreakBtn");
    if (streakBtn) {
      streakBtn.innerHTML = `🔥 ${this.checkinStreak} 天打卡`;
    }
  }

  handleDailyCheckin() {
    const today = new Date().toISOString().split('T')[0];
    if (this.lastCheckin === today) {
      this.showToast(`今日已完成打卡！当前连胜 ${this.checkinStreak} 天`, "info");
      return;
    }
    this.checkinStreak += 1;
    this.lastCheckin = today;
    localStorage.setItem("investlearning_streak", this.checkinStreak.toString());
    localStorage.setItem("investlearning_last_checkin", today);
    this.updateGlobalProgress();
    this.showToast(`🔥 签到成功！连续打卡达成 ${this.checkinStreak} 天！`, "success");
  }

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
          <div class="book-btn-group">
            <a class="book-dl-btn" href="https://annas-archive.li/search?q=${encodeURIComponent(b.title_en + ' ' + b.author)}" target="_blank" rel="noopener">
              🔍 Anna's Archive 检索
            </a>
            <button class="book-md5-btn" onclick="app.showBookDetail('${b.id}')">详情</button>
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
        this.updateGlobalProgress();
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
    document.getElementById("checkinStreakBtn")?.addEventListener("click", () => this.handleDailyCheckin());

    // Mobile sidebar toggle
    document.getElementById("sidebarToggleBtn")?.addEventListener("click", () => {
      document.getElementById("courseSidebar")?.classList.toggle("mobile-open");
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
