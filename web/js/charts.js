/**
 * StockLearning - Interactive Financial & Quantitative Visualization Engines
 * 5 Full Native Canvas/SVG/JS Interactive Visualizers:
 * 1. Candlestick & Technical Indicators (OHLC, MA, Bollinger, MACD, RSI, Crosshair HUD)
 * 2. Limit Order Book (LOB) Depth Ladder & Interactive Trading Simulator
 * 3. Markowitz Efficient Frontier & Monte Carlo Portfolio Optimizer
 * 4. Kelly Criterion & Monte Carlo Wealth/Ruin Simulator
 * 5. DCF Cash Flow Discounting & Sensitivity Heatmap Engine
 */

// ===================================================================
// 1. Candlestick & Technical Indicators Interactive Visualizer
// ===================================================================
class KLineVisualizer {
  constructor(canvasId, hudId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.hud = document.getElementById(hudId);
    
    this.period = "1D";
    this.showMA = true;
    this.showBollinger = true;
    this.subIndicator = "MACD"; // 'MACD' or 'RSI'
    
    this.data = [];
    this.hoverIndex = -1;
    this.mouseX = -1;
    this.mouseY = -1;
    
    this.generateMarketData(100);
    this.initEvents();
    this.render();
  }

  generateMarketData(count = 100) {
    this.data = [];
    let price = 150.0;
    let baseDate = new Date();
    baseDate.setDate(baseDate.getDate() - count);

    for (let i = 0; i < count; i++) {
      let changePercent = (Math.random() - 0.49) * 0.04;
      let open = price;
      let close = open * (1 + changePercent);
      let high = Math.max(open, close) + Math.random() * open * 0.015;
      let low = Math.min(open, close) - Math.random() * open * 0.015;
      let volume = Math.floor(50000 + Math.random() * 120000 + Math.abs(changePercent) * 2000000);
      
      let d = new Date(baseDate);
      d.setDate(d.getDate() + i);
      let dateStr = d.toISOString().split('T')[0];

      this.data.push({ date: dateStr, open, high, low, close, volume });
      price = close;
    }
    this.calculateIndicators();
  }

  calculateIndicators() {
    const closes = this.data.map(d => d.close);
    const n = closes.length;

    // 1. Moving Averages
    for (let i = 0; i < n; i++) {
      this.data[i].ma5 = i >= 4 ? closes.slice(i - 4, i + 1).reduce((a, b) => a + b, 0) / 5 : null;
      this.data[i].ma20 = i >= 19 ? closes.slice(i - 19, i + 1).reduce((a, b) => a + b, 0) / 20 : null;
      this.data[i].ma60 = i >= 59 ? closes.slice(i - 59, i + 1).reduce((a, b) => a + b, 0) / 60 : null;

      // Bollinger Bands (20, 2)
      if (i >= 19) {
        let slice = closes.slice(i - 19, i + 1);
        let mean = this.data[i].ma20;
        let variance = slice.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / 20;
        let std = Math.sqrt(variance);
        this.data[i].bollUpper = mean + 2 * std;
        this.data[i].bollLower = mean - 2 * std;
      } else {
        this.data[i].bollUpper = null;
        this.data[i].bollLower = null;
      }
    }

    // 2. MACD (12, 26, 9)
    let ema12 = closes[0];
    let ema26 = closes[0];
    let k12 = 2 / 13;
    let k26 = 2 / 27;
    let k9 = 2 / 10;
    let dea = 0;

    for (let i = 0; i < n; i++) {
      if (i > 0) {
        ema12 = closes[i] * k12 + ema12 * (1 - k12);
        ema26 = closes[i] * k26 + ema26 * (1 - k26);
      }
      let dif = ema12 - ema26;
      dea = (i === 0) ? dif : dif * k9 + dea * (1 - k9);
      let hist = (dif - dea) * 2;
      this.data[i].macdDif = dif;
      this.data[i].macdDea = dea;
      this.data[i].macdHist = hist;
    }

    // 3. RSI (14)
    for (let i = 0; i < n; i++) {
      if (i < 14) {
        this.data[i].rsi = 50;
        continue;
      }
      let gains = 0, losses = 0;
      for (let j = i - 13; j <= i; j++) {
        let delta = closes[j] - closes[j - 1];
        if (delta > 0) gains += delta;
        else losses -= delta;
      }
      let rs = (losses === 0) ? 100 : (gains / 14) / (losses / 14);
      this.data[i].rsi = 100 - (100 / (1 + rs));
    }
  }

  addCandleTick() {
    let last = this.data[this.data.length - 1];
    let open = last.close;
    let change = (Math.random() - 0.48) * 0.035;
    let close = open * (1 + change);
    let high = Math.max(open, close) + Math.random() * open * 0.01;
    let low = Math.min(open, close) - Math.random() * open * 0.01;
    let volume = Math.floor(60000 + Math.random() * 150000);

    let d = new Date(last.date);
    d.setDate(d.getDate() + 1);
    let dateStr = d.toISOString().split('T')[0];

    this.data.push({ date: dateStr, open, high, low, close, volume });
    if (this.data.length > 120) this.data.shift();
    this.calculateIndicators();
    this.render();
  }

  initEvents() {
    window.addEventListener('resize', () => this.resizeCanvas());
    this.resizeCanvas();

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouseX = (e.clientX - rect.left) * (this.canvas.width / rect.width);
      this.mouseY = (e.clientY - rect.top) * (this.canvas.height / rect.height);
      this.handleHover();
      this.render();
    });

    this.canvas.addEventListener('mouseleave', () => {
      this.hoverIndex = -1;
      this.mouseX = -1;
      this.mouseY = -1;
      this.updateHudDefault();
      this.render();
    });
  }

  resizeCanvas() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height || 480;
    this.render();
  }

  handleHover() {
    if (this.mouseX < 0 || this.data.length === 0) return;
    const padding = { left: 50, right: 60, top: 20, bottom: 30 };
    const chartW = this.canvas.width - padding.left - padding.right;
    const candleW = chartW / this.data.length;
    let idx = Math.floor((this.mouseX - padding.left) / candleW);
    idx = Math.max(0, Math.min(this.data.length - 1, idx));
    this.hoverIndex = idx;
    this.updateHud(this.data[idx]);
  }

  updateHud(d) {
    if (!this.hud || !d) return;
    let chg = ((d.close - d.open) / d.open) * 100;
    let isUp = chg >= 0;
    let colorClass = isUp ? "up" : "down";
    let sign = isUp ? "+" : "";

    this.hud.innerHTML = `
      <span>日期: <b>${d.date}</b></span>
      <span>开: <b>${d.open.toFixed(2)}</b></span>
      <span>高: <b>${d.high.toFixed(2)}</b></span>
      <span>低: <b>${d.low.toFixed(2)}</b></span>
      <span>收: <b class="${colorClass}">${d.close.toFixed(2)}</b></span>
      <span>涨跌: <b class="${colorClass}">${sign}${chg.toFixed(2)}%</b></span>
      <span>量: <b>${(d.volume / 1000).toFixed(0)}k</b></span>
      ${d.ma5 ? `<span style="color:#f59e0b">MA5: ${d.ma5.toFixed(2)}</span>` : ''}
      ${d.ma20 ? `<span style="color:#38bdf8">MA20: ${d.ma20.toFixed(2)}</span>` : ''}
      ${this.subIndicator === 'RSI' ? `<span style="color:#a855f7">RSI: ${d.rsi.toFixed(1)}</span>` : `<span style="color:#10b981">DIF: ${d.macdDif.toFixed(2)}</span>`}
    `;
  }

  updateHudDefault() {
    if (this.data.length > 0) {
      this.updateHud(this.data[this.data.length - 1]);
    }
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    if (!ctx || w === 0 || h === 0) return;

    ctx.clearRect(0, 0, w, h);

    const pad = { left: 40, right: 60, top: 25, bottom: 25 };
    const mainH = (h - pad.top - pad.bottom) * 0.65;
    const subH = (h - pad.top - pad.bottom) * 0.28;
    const gap = (h - pad.top - pad.bottom) * 0.07;
    const subTop = pad.top + mainH + gap;
    const chartW = w - pad.left - pad.right;

    const n = this.data.length;
    if (n === 0) return;
    const candleW = chartW / n;

    // Price Bounds
    let minPrice = Infinity, maxPrice = -Infinity;
    let maxVol = 0;
    for (let d of this.data) {
      if (d.low < minPrice) minPrice = d.low;
      if (d.high > maxPrice) maxPrice = d.high;
      if (this.showBollinger && d.bollUpper && d.bollUpper > maxPrice) maxPrice = d.bollUpper;
      if (this.showBollinger && d.bollLower && d.bollLower < minPrice) minPrice = d.bollLower;
      if (d.volume > maxVol) maxVol = d.volume;
    }
    const priceMargin = (maxPrice - minPrice) * 0.06;
    minPrice -= priceMargin;
    maxPrice += priceMargin;

    const priceToY = (p) => pad.top + (1 - (p - minPrice) / (maxPrice - minPrice)) * mainH;
    const volToH = (v) => (v / (maxVol || 1)) * (mainH * 0.22);

    // 1. Grid Lines
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      let py = pad.top + (mainH / 4) * i;
      ctx.beginPath();
      ctx.moveTo(pad.left, py);
      ctx.lineTo(w - pad.right, py);
      ctx.stroke();

      // Right axis labels
      let val = maxPrice - ((maxPrice - minPrice) / 4) * i;
      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono, monospace";
      ctx.textAlign = "left";
      ctx.fillText(val.toFixed(2), w - pad.right + 6, py + 3);
    }

    // Sub-chart grid
    for (let i = 0; i <= 2; i++) {
      let sy = subTop + (subH / 2) * i;
      ctx.beginPath();
      ctx.moveTo(pad.left, sy);
      ctx.lineTo(w - pad.right, sy);
      ctx.stroke();
    }

    // 2. Bollinger Bands Corridor
    if (this.showBollinger) {
      ctx.beginPath();
      let started = false;
      for (let i = 0; i < n; i++) {
        if (this.data[i].bollUpper !== null) {
          let x = pad.left + i * candleW + candleW / 2;
          let y = priceToY(this.data[i].bollUpper);
          if (!started) { ctx.moveTo(x, y); started = true; }
          else ctx.lineTo(x, y);
        }
      }
      for (let i = n - 1; i >= 0; i--) {
        if (this.data[i].bollLower !== null) {
          let x = pad.left + i * candleW + candleW / 2;
          let y = priceToY(this.data[i].bollLower);
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();
      ctx.fillStyle = "rgba(56, 189, 248, 0.05)";
      ctx.fill();

      // Upper and Lower Lines
      ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // 3. Candlesticks and Volume
    for (let i = 0; i < n; i++) {
      const d = this.data[i];
      const x = pad.left + i * candleW;
      const isUp = d.close >= d.open;
      const color = isUp ? "#10b981" : "#f43f5e";
      const bodyTop = priceToY(Math.max(d.open, d.close));
      const bodyBottom = priceToY(Math.min(d.open, d.close));
      const bodyH = Math.max(1, bodyBottom - bodyTop);

      // Volume bar
      ctx.fillStyle = isUp ? "rgba(16, 185, 129, 0.25)" : "rgba(244, 63, 94, 0.25)";
      const vh = volToH(d.volume);
      ctx.fillRect(x + candleW * 0.15, pad.top + mainH - vh, candleW * 0.7, vh);

      // Wick
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(x + candleW / 2, priceToY(d.high));
      ctx.lineTo(x + candleW / 2, priceToY(d.low));
      ctx.stroke();

      // Candle Body
      ctx.fillStyle = color;
      ctx.fillRect(x + candleW * 0.15, bodyTop, candleW * 0.7, bodyH);
    }

    // 4. Moving Averages (MA5, MA20, MA60)
    if (this.showMA) {
      const drawLine = (prop, col) => {
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        let init = false;
        for (let i = 0; i < n; i++) {
          if (this.data[i][prop] !== null) {
            let cx = pad.left + i * candleW + candleW / 2;
            let cy = priceToY(this.data[i][prop]);
            if (!init) { ctx.moveTo(cx, cy); init = true; }
            else ctx.lineTo(cx, cy);
          }
        }
        ctx.stroke();
      };
      drawLine("ma5", "#f59e0b");
      drawLine("ma20", "#38bdf8");
      drawLine("ma60", "#a855f7");
    }

    // 5. Sub-indicator (MACD or RSI)
    if (this.subIndicator === "MACD") {
      let maxM = 0;
      for (let d of this.data) {
        maxM = Math.max(maxM, Math.abs(d.macdDif || 0), Math.abs(d.macdDea || 0), Math.abs(d.macdHist || 0));
      }
      maxM = (maxM || 1) * 1.2;
      const macdToY = (v) => subTop + (subH / 2) - (v / maxM) * (subH / 2);

      // Zero line
      ctx.strokeStyle = "#334155";
      ctx.beginPath();
      ctx.moveTo(pad.left, subTop + subH / 2);
      ctx.lineTo(w - pad.right, subTop + subH / 2);
      ctx.stroke();

      // Histogram
      for (let i = 0; i < n; i++) {
        let d = this.data[i];
        let x = pad.left + i * candleW;
        let hy = macdToY(d.macdHist);
        let zy = subTop + subH / 2;
        ctx.fillStyle = d.macdHist >= 0 ? "rgba(16, 185, 129, 0.7)" : "rgba(244, 63, 94, 0.7)";
        ctx.fillRect(x + candleW * 0.2, Math.min(hy, zy), candleW * 0.6, Math.abs(hy - zy));
      }

      // DIF & DEA Lines
      const drawSubLine = (prop, color) => {
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        for (let i = 0; i < n; i++) {
          let cx = pad.left + i * candleW + candleW / 2;
          let cy = macdToY(this.data[i][prop]);
          if (i === 0) ctx.moveTo(cx, cy);
          else ctx.lineTo(cx, cy);
        }
        ctx.stroke();
      };
      drawSubLine("macdDif", "#38bdf8");
      drawSubLine("macdDea", "#f59e0b");
      
      // Label
      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono";
      ctx.fillText("MACD (12,26,9)", pad.left + 8, subTop + 14);
    } else {
      // RSI (14)
      const rsiToY = (r) => subTop + (1 - r / 100) * subH;
      // Overbought 70 / Oversold 30
      ctx.strokeStyle = "rgba(244, 63, 94, 0.4)";
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(pad.left, rsiToY(70));
      ctx.lineTo(w - pad.right, rsiToY(70));
      ctx.stroke();

      ctx.strokeStyle = "rgba(16, 185, 129, 0.4)";
      ctx.beginPath();
      ctx.moveTo(pad.left, rsiToY(30));
      ctx.lineTo(w - pad.right, rsiToY(30));
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.strokeStyle = "#a855f7";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let i = 0; i < n; i++) {
        let cx = pad.left + i * candleW + candleW / 2;
        let cy = rsiToY(this.data[i].rsi);
        if (i === 0) ctx.moveTo(cx, cy);
        else ctx.lineTo(cx, cy);
      }
      ctx.stroke();

      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono";
      ctx.fillText("RSI (14)", pad.left + 8, subTop + 14);
    }

    // 6. Interactive Crosshair Hover
    if (this.hoverIndex >= 0 && this.hoverIndex < n) {
      let cx = pad.left + this.hoverIndex * candleW + candleW / 2;
      let d = this.data[this.hoverIndex];
      let cy = priceToY(d.close);

      ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
      ctx.lineWidth = 1;
      ctx.setLineDash([3, 3]);

      // Vertical line
      ctx.beginPath();
      ctx.moveTo(cx, pad.top);
      ctx.lineTo(cx, h - pad.bottom);
      ctx.stroke();

      // Horizontal line
      ctx.beginPath();
      ctx.moveTo(pad.left, cy);
      ctx.lineTo(w - pad.right, cy);
      ctx.stroke();
      ctx.setLineDash([]);

      // Floating Price Badge on Right Axis
      ctx.fillStyle = "#2563eb";
      ctx.fillRect(w - pad.right, cy - 10, pad.right, 20);
      ctx.fillStyle = "#ffffff";
      ctx.font = "10px JetBrains Mono";
      ctx.textAlign = "center";
      ctx.fillText(d.close.toFixed(2), w - pad.right / 2, cy + 3);

      // Date Badge on Bottom Axis
      ctx.fillStyle = "#1e293b";
      ctx.fillRect(cx - 35, h - pad.bottom, 70, 18);
      ctx.fillStyle = "#cbd5e1";
      ctx.fillText(d.date.slice(5), cx, h - pad.bottom + 13);
    }
  }
}

// ===================================================================
// 2. Limit Order Book (LOB) Depth Ladder & Interactive Engine
// ===================================================================
class LimitOrderBookEngine {
  constructor(ladderContainerId, chartCanvasId) {
    this.container = document.getElementById(ladderContainerId);
    this.canvas = document.getElementById(chartCanvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;

    this.bids = [];
    this.asks = [];
    this.midPrice = 180.00;
    this.autoTickTimer = null;

    this.initBook();
    this.render();
  }

  initBook() {
    this.bids = [];
    this.asks = [];
    let base = this.midPrice;

    // Generate 8 bid levels
    let cumBid = 0;
    for (let i = 1; i <= 8; i++) {
      let price = +(base - i * 0.05).toFixed(2);
      let qty = Math.floor(80 + Math.random() * 250);
      cumBid += qty;
      this.bids.push({ price, qty, cumQty: cumBid });
    }

    // Generate 8 ask levels
    let cumAsk = 0;
    for (let i = 1; i <= 8; i++) {
      let price = +(base + i * 0.05).toFixed(2);
      let qty = Math.floor(80 + Math.random() * 250);
      cumAsk += qty;
      this.asks.push({ price, qty, cumQty: cumAsk });
    }
  }

  submitOrder(side, type, price, qty) {
    qty = parseInt(qty) || 100;
    price = parseFloat(price) || this.midPrice;

    let executedQty = 0;
    let totalCost = 0;
    let logMsg = "";

    if (type === "MARKET") {
      if (side === "BUY") {
        while (qty > 0 && this.asks.length > 0) {
          let topAsk = this.asks[0];
          let fill = Math.min(qty, topAsk.qty);
          qty -= fill;
          topAsk.qty -= fill;
          executedQty += fill;
          totalCost += fill * topAsk.price;
          if (topAsk.qty === 0) this.asks.shift();
        }
      } else {
        while (qty > 0 && this.bids.length > 0) {
          let topBid = this.bids[0];
          let fill = Math.min(qty, topBid.qty);
          qty -= fill;
          topBid.qty -= fill;
          executedQty += fill;
          totalCost += fill * topBid.price;
          if (topBid.qty === 0) this.bids.shift();
        }
      }
      let avgP = executedQty > 0 ? (totalCost / executedQty).toFixed(2) : "0.00";
      logMsg = `市价${side === 'BUY' ? '买入' : '卖出'}成交 ${executedQty} 股，均价 $${avgP}`;
    } else {
      // LIMIT ORDER
      if (side === "BUY") {
        if (this.asks.length > 0 && price >= this.asks[0].price) {
          return this.submitOrder("BUY", "MARKET", price, qty);
        }
        let existing = this.bids.find(b => b.price === price);
        if (existing) existing.qty += qty;
        else this.bids.push({ price, qty, cumQty: 0 });
        this.bids.sort((a, b) => b.price - a.price);
        logMsg = `挂单限价买入 $${price}，数量 ${qty} 股`;
      } else {
        if (this.bids.length > 0 && price <= this.bids[0].price) {
          return this.submitOrder("SELL", "MARKET", price, qty);
        }
        let existing = this.asks.find(a => a.price === price);
        if (existing) existing.qty += qty;
        else this.asks.push({ price, qty, cumQty: 0 });
        this.asks.sort((a, b) => a.price - b.price);
        logMsg = `挂单限价卖出 $${price}，数量 ${qty} 股`;
      }
    }

    this.recomputeCumulatives();
    this.render();
    return logMsg;
  }

  recomputeCumulatives() {
    let cb = 0;
    this.bids.forEach(b => { cb += b.qty; b.cumQty = cb; });
    let ca = 0;
    this.asks.forEach(a => { ca += a.qty; a.cumQty = ca; });

    let bb = this.bids[0] ? this.bids[0].price : this.midPrice - 0.05;
    let ba = this.asks[0] ? this.asks[0].price : this.midPrice + 0.05;
    this.midPrice = +((bb + ba) / 2).toFixed(2);
  }

  randomTick() {
    if (Math.random() < 0.5) {
      this.submitOrder("BUY", "LIMIT", +(this.midPrice - 0.05 * (Math.floor(Math.random() * 3) + 1)).toFixed(2), Math.floor(Math.random() * 50) + 10);
    } else {
      this.submitOrder("SELL", "LIMIT", +(this.midPrice + 0.05 * (Math.floor(Math.random() * 3) + 1)).toFixed(2), Math.floor(Math.random() * 50) + 10);
    }
  }

  render() {
    if (!this.container) return;

    let bestBid = this.bids[0] ? this.bids[0].price : 0;
    let bestAsk = this.asks[0] ? this.asks[0].price : 0;
    let spread = +(bestAsk - bestBid).toFixed(2);
    let maxCum = Math.max(
      this.bids[this.bids.length - 1]?.cumQty || 1,
      this.asks[this.asks.length - 1]?.cumQty || 1
    );

    let html = `
      <div class="lob-ladder-panel">
        <div class="lob-ladder-header">
          <span>深度占比</span>
          <span>挂单量</span>
          <span>价格 ($)</span>
          <span style="text-align:right">累积量</span>
        </div>
        <div class="lob-asks-list" style="display:flex; flex-direction:column-reverse;">
    `;

    // Render 6 Asks
    for (let i = Math.min(5, this.asks.length - 1); i >= 0; i--) {
      let a = this.asks[i];
      let pct = ((a.cumQty / maxCum) * 100).toFixed(0);
      html += `
        <div class="lob-row">
          <div class="lob-depth-bar ask" style="width: ${pct}%"></div>
          <span style="color:var(--accent-red)">${pct}%</span>
          <span style="font-weight:600">${a.qty}</span>
          <span style="color:var(--accent-red); font-weight:700;">$${a.price.toFixed(2)}</span>
          <span style="text-align:right; color:var(--text-muted)">${a.cumQty}</span>
        </div>
      `;
    }

    html += `
      </div>
      <div class="lob-mid-spread">
        <span>中间价: <b style="color:var(--accent-gold)">$${this.midPrice.toFixed(2)}</b></span>
        <span>买卖点差: <b style="color:var(--text-primary)">$${spread.toFixed(2)}</b> (${((spread / this.midPrice) * 10000).toFixed(1)} bps)</span>
      </div>
      <div class="lob-bids-list">
    `;

    // Render 6 Bids
    for (let i = 0; i < Math.min(6, this.bids.length); i++) {
      let b = this.bids[i];
      let pct = ((b.cumQty / maxCum) * 100).toFixed(0);
      html += `
        <div class="lob-row">
          <div class="lob-depth-bar bid" style="width: ${pct}%"></div>
          <span style="color:var(--accent-green)">${pct}%</span>
          <span style="font-weight:600">${b.qty}</span>
          <span style="color:var(--accent-green); font-weight:700;">$${b.price.toFixed(2)}</span>
          <span style="text-align:right; color:var(--text-muted)">${b.cumQty}</span>
        </div>
      `;
    }

    html += `</div></div>`;
    this.container.innerHTML = html;
    this.renderDepthChart();
  }

  renderDepthChart() {
    if (!this.ctx || !this.canvas) return;
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    ctx.clearRect(0, 0, w, h);

    const pad = 25;
    const maxCum = Math.max(
      this.bids[this.bids.length - 1]?.cumQty || 1000,
      this.asks[this.asks.length - 1]?.cumQty || 1000
    ) * 1.1;

    // Draw Bids (Green area, left side)
    ctx.beginPath();
    ctx.moveTo(w / 2, h - pad);
    for (let i = 0; i < this.bids.length; i++) {
      let x = (w / 2) - (i / this.bids.length) * (w / 2 - pad);
      let y = (h - pad) - (this.bids[i].cumQty / maxCum) * (h - pad * 2);
      ctx.lineTo(x, y);
    }
    ctx.lineTo(pad, h - pad);
    ctx.closePath();
    ctx.fillStyle = "rgba(16, 185, 129, 0.2)";
    ctx.fill();
    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw Asks (Red area, right side)
    ctx.beginPath();
    ctx.moveTo(w / 2, h - pad);
    for (let i = 0; i < this.asks.length; i++) {
      let x = (w / 2) + (i / this.asks.length) * (w / 2 - pad);
      let y = (h - pad) - (this.asks[i].cumQty / maxCum) * (h - pad * 2);
      ctx.lineTo(x, y);
    }
    ctx.lineTo(w - pad, h - pad);
    ctx.closePath();
    ctx.fillStyle = "rgba(244, 63, 94, 0.2)";
    ctx.fill();
    ctx.strokeStyle = "#f43f5e";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Mid price dividing line
    ctx.strokeStyle = "rgba(245, 158, 11, 0.7)";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(w / 2, 10);
    ctx.lineTo(w / 2, h - pad);
    ctx.stroke();
    ctx.setLineDash([]);
  }
}

// ===================================================================
// 3. Markowitz Efficient Frontier Optimizer
// ===================================================================
class MarkowitzOptimizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    // Default asset expectations
    this.retA = 0.12; this.volA = 0.18; // Equities
    this.retB = 0.04; this.volB = 0.06; // Treasuries
    this.retC = 0.08; this.volC = 0.14; // Gold / Commodity
    this.rhoAB = -0.10;
    this.rhoAC = 0.15;
    this.rhoBC = 0.05;
    this.rf = 0.025;

    this.portfolios = [];
    this.tangency = null;
    this.mvp = null;

    this.solve();
    this.render();
  }

  updateParams(params) {
    Object.assign(this, params);
    this.solve();
    this.render();
  }

  solve() {
    this.portfolios = [];
    const count = 1200;
    let maxSharpe = -Infinity;
    let minVol = Infinity;

    const rA = this.retA, rB = this.retB, rC = this.retC;
    const sA = this.volA, sB = this.volB, sC = this.volC;
    const covAB = this.rhoAB * sA * sB;
    const covAC = this.rhoAC * sA * sC;
    const covBC = this.rhoBC * sB * sC;

    for (let i = 0; i < count; i++) {
      let u1 = Math.random(), u2 = Math.random(), u3 = Math.random();
      let sum = u1 + u2 + u3;
      let w1 = u1 / sum, w2 = u2 / sum, w3 = u3 / sum;

      let pRet = w1 * rA + w2 * rB + w3 * rC;
      let pVar = (w1 * sA) ** 2 + (w2 * sB) ** 2 + (w3 * sC) ** 2 +
                 2 * w1 * w2 * covAB + 2 * w1 * w3 * covAC + 2 * w2 * w3 * covBC;
      let pVol = Math.sqrt(Math.max(0.0001, pVar));
      let sharpe = (pRet - this.rf) / pVol;

      let p = { w1, w2, w3, ret: pRet, vol: pVol, sharpe };
      this.portfolios.push(p);

      if (sharpe > maxSharpe) {
        maxSharpe = sharpe;
        this.tangency = p;
      }
      if (pVol < minVol) {
        minVol = pVol;
        this.mvp = p;
      }
    }
  }

  render() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    if (!ctx || w === 0 || h === 0) return;

    ctx.clearRect(0, 0, w, h);

    const pad = { left: 55, right: 30, top: 30, bottom: 40 };
    const maxVol = 0.25;
    const minRet = 0.01;
    const maxRet = 0.16;

    const volToX = (v) => pad.left + (v / maxVol) * (w - pad.left - pad.right);
    const retToY = (r) => (h - pad.bottom) - ((r - minRet) / (maxRet - minRet)) * (h - pad.top - pad.bottom);

    // Grid & Axes
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      let v = (maxVol / 5) * i;
      let x = volToX(v);
      ctx.beginPath(); ctx.moveTo(x, pad.top); ctx.lineTo(x, h - pad.bottom); ctx.stroke();
      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono";
      ctx.textAlign = "center";
      ctx.fillText((v * 100).toFixed(0) + "%", x, h - pad.bottom + 15);
    }
    for (let i = 0; i <= 4; i++) {
      let r = minRet + ((maxRet - minRet) / 4) * i;
      let y = retToY(r);
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono";
      ctx.textAlign = "right";
      ctx.fillText((r * 100).toFixed(1) + "%", pad.left - 8, y + 4);
    }

    // Axis Titles
    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px system-ui";
    ctx.fillText("年化预期收益率 E(R)", pad.left + 50, pad.top - 12);
    ctx.fillText("组合波动率 σ", w - pad.right - 20, h - pad.bottom + 30);

    // Draw Portfolios (Scatter Dots)
    for (let p of this.portfolios) {
      let x = volToX(p.vol);
      let y = retToY(p.ret);
      let s = p.sharpe;
      // Color gradient by Sharpe
      let r = Math.min(255, Math.floor(Math.max(0, s - 0.2) * 200));
      let g = Math.min(255, Math.floor(Math.max(0, s) * 180));
      let b = 255 - Math.min(200, Math.floor(s * 150));
      ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.4)`;
      ctx.beginPath();
      ctx.arc(x, y, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw Individual Assets
    const drawAssetDot = (ret, vol, label, color) => {
      let x = volToX(vol), y = retToY(ret);
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#f8fafc";
      ctx.font = "bold 10px system-ui";
      ctx.fillText(label, x + 8, y + 3);
    };
    drawAssetDot(this.retA, this.volA, "资产A(股票)", "#f43f5e");
    drawAssetDot(this.retB, this.volB, "资产B(国债)", "#38bdf8");
    drawAssetDot(this.retC, this.volC, "资产C(黄金)", "#f59e0b");

    // Draw CAL (Capital Allocation Line)
    if (this.tangency) {
      let rfX = volToX(0);
      let rfY = retToY(this.rf);
      let tanX = volToX(this.tangency.vol);
      let tanY = retToY(this.tangency.ret);

      ctx.strokeStyle = "#fbbf24";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(rfX, rfY);
      // extend CAL
      let slope = (tanY - rfY) / (tanX - rfX);
      ctx.lineTo(volToX(0.24), rfY + slope * (volToX(0.24) - rfX));
      ctx.stroke();

      // Tangency Portfolio Dot (Max Sharpe)
      ctx.fillStyle = "#fbbf24";
      ctx.beginPath();
      ctx.arc(tanX, tanY, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = "#fbbf24";
      ctx.font = "bold 11px system-ui";
      ctx.fillText(`★ 切点组合(Max Sharpe=${this.tangency.sharpe.toFixed(2)})`, tanX + 10, tanY - 6);
    }

    // Minimum Variance Portfolio (MVP)
    if (this.mvp) {
      let mx = volToX(this.mvp.vol);
      let my = retToY(this.mvp.ret);
      ctx.fillStyle = "#10b981";
      ctx.beginPath();
      ctx.arc(mx, my, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText(`● MVP 最小方差`, mx + 8, my + 14);
    }
  }
}

// ===================================================================
// 4. Kelly Criterion & Monte Carlo Wealth Simulator
// ===================================================================
class KellySimulator {
  constructor(canvasId, curveCanvasId) {
    this.canvas = document.getElementById(canvasId);
    this.curveCanvas = document.getElementById(curveCanvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.curveCtx = this.curveCanvas ? this.curveCanvas.getContext('2d') : null;

    this.winRate = 0.55;       // p
    this.payoffRatio = 1.5;    // b
    this.strategy = "HALF_KELLY"; // FULL, HALF, DOUBLE, FIXED
    this.customF = null;

    this.initialCapital = 10000;
    this.numRounds = 100;
    this.numPaths = 50;

    this.paths = [];
    this.stats = {};

    this.runSimulation();
    this.render();
  }

  getOptimalKelly() {
    let p = this.winRate;
    let b = this.payoffRatio;
    let q = 1 - p;
    let f = (b * p - q) / b;
    return Math.max(0, f);
  }

  getBetFraction() {
    let opt = this.getOptimalKelly();
    if (this.customF !== null) return this.customF;
    if (this.strategy === "FULL_KELLY") return opt;
    if (this.strategy === "HALF_KELLY") return opt * 0.5;
    if (this.strategy === "DOUBLE_KELLY") return opt * 2.0;
    if (this.strategy === "FIXED_2PCT") return 0.02;
    return opt * 0.5;
  }

  runSimulation() {
    this.paths = [];
    let f = this.getBetFraction();
    let p = this.winRate;
    let b = this.payoffRatio;
    let ruinedCount = 0;
    let terminalWealths = [];

    for (let path = 0; path < this.numPaths; path++) {
      let series = [this.initialCapital];
      let capital = this.initialCapital;
      let isRuined = false;

      for (let t = 1; t <= this.numRounds; t++) {
        if (capital <= 10) {
          capital = 0;
          series.push(0);
          isRuined = true;
          continue;
        }
        let bet = capital * f;
        let win = Math.random() < p;
        if (win) {
          capital += bet * b;
        } else {
          capital -= bet;
        }
        series.push(capital);
        if (capital < this.initialCapital * 0.15) isRuined = true;
      }
      this.paths.push(series);
      if (isRuined) ruinedCount++;
      terminalWealths.push(capital);
    }

    terminalWealths.sort((a, b) => a - b);
    let median = terminalWealths[Math.floor(terminalWealths.length / 2)];

    this.stats = {
      f: f,
      optF: this.getOptimalKelly(),
      ruinRate: ((ruinedCount / this.numPaths) * 100).toFixed(1),
      medianWealth: median.toFixed(0),
      growthRate: (p * Math.log(1 + b * f) + (1 - p) * Math.log(Math.max(0.0001, 1 - f))).toFixed(4)
    };
  }

  render() {
    this.renderPaths();
    this.renderGrowthCurve();
  }

  renderPaths() {
    if (!this.ctx || !this.canvas) return;
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    ctx.clearRect(0, 0, w, h);

    const pad = { left: 60, right: 30, top: 25, bottom: 30 };
    // Log scale from $100 to $1,000,000
    const minY = 2; // 10^2 = 100
    const maxY = 6; // 10^6 = 1,000,000

    const tToX = (t) => pad.left + (t / this.numRounds) * (w - pad.left - pad.right);
    const wealthToY = (val) => {
      let logV = Math.log10(Math.max(10, val));
      let clamped = Math.max(minY, Math.min(maxY, logV));
      return (h - pad.bottom) - ((clamped - minY) / (maxY - minY)) * (h - pad.top - pad.bottom);
    };

    // Log Grid
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 1;
    for (let p = minY; p <= maxY; p++) {
      let y = wealthToY(Math.pow(10, p));
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
      ctx.fillStyle = "#64748b";
      ctx.font = "10px JetBrains Mono";
      ctx.textAlign = "right";
      ctx.fillText("$" + Math.pow(10, p).toLocaleString(), pad.left - 8, y + 3);
    }

    // Initial Capital Line ($10,000)
    let initY = wealthToY(this.initialCapital);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
    ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(pad.left, initY); ctx.lineTo(w - pad.right, initY); ctx.stroke();
    ctx.setLineDash([]);

    // Draw Paths
    for (let path of this.paths) {
      ctx.beginPath();
      let terminal = path[path.length - 1];
      let color = terminal > this.initialCapital ? "rgba(16, 185, 129, 0.35)" : "rgba(244, 63, 94, 0.4)";
      if (this.strategy === "FULL_KELLY") color = "rgba(56, 189, 248, 0.4)";
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;

      for (let t = 0; t <= this.numRounds; t++) {
        let x = tToX(t);
        let y = wealthToY(path[t]);
        if (t === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  }

  renderGrowthCurve() {
    if (!this.curveCtx || !this.curveCanvas) return;
    const ctx = this.curveCtx;
    const w = this.curveCanvas.width;
    const h = this.curveCanvas.height;
    ctx.clearRect(0, 0, w, h);

    const pad = 25;
    const p = this.winRate;
    const b = this.payoffRatio;
    const optF = this.getOptimalKelly();
    const currentF = this.getBetFraction();

    // Plot g(f) for f in [0, 0.9]
    let maxG = -Infinity, minG = Infinity;
    let points = [];
    for (let f = 0.01; f < 0.9; f += 0.01) {
      let g = p * Math.log(1 + b * f) + (1 - p) * Math.log(Math.max(0.001, 1 - f));
      points.push({ f, g });
      if (g > maxG) maxG = g;
      if (g < minG && g > -0.2) minG = g;
    }
    minG = Math.min(-0.05, minG);
    maxG = Math.max(0.05, maxG);

    const fToX = (f) => pad + (f / 0.9) * (w - pad * 2);
    const gToY = (g) => (h - pad) - ((g - minG) / (maxG - minG)) * (h - pad * 2);

    // Zero growth line
    let zy = gToY(0);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
    ctx.beginPath(); ctx.moveTo(pad, zy); ctx.lineTo(w - pad, zy); ctx.stroke();

    // Growth Curve
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    points.forEach((pt, i) => {
      let x = fToX(pt.f);
      let y = gToY(Math.max(minG, pt.g));
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Mark Peak (Optimal Kelly)
    let peakX = fToX(optF);
    let peakG = p * Math.log(1 + b * optF) + (1 - p) * Math.log(1 - optF);
    let peakY = gToY(peakG);
    ctx.fillStyle = "#fbbf24";
    ctx.beginPath(); ctx.arc(peakX, peakY, 5, 0, Math.PI * 2); ctx.fill();

    // Current Bet Indicator
    let curX = fToX(currentF);
    let curG = p * Math.log(1 + b * currentF) + (1 - p) * Math.log(Math.max(0.001, 1 - currentF));
    let curY = gToY(Math.max(minG, curG));
    ctx.fillStyle = "#f43f5e";
    ctx.beginPath(); ctx.arc(curX, curY, 6, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = "#cbd5e1";
    ctx.font = "10px JetBrains Mono";
    ctx.fillText(`Optimal f*=${(optF * 100).toFixed(1)}%`, peakX - 25, peakY - 8);
  }
}

// ===================================================================
// 5. DCF Valuation & Sensitivity Matrix Engine
// ===================================================================
class DCFValuationEngine {
  constructor(matrixContainerId, metricsContainerId) {
    this.matrixContainer = document.getElementById(matrixContainerId);
    this.metricsContainer = document.getElementById(metricsContainerId);

    this.fcf0 = 1200;       // 百万元
    this.growthYears = 5;   // 显性预测期
    this.growthRate = 0.15; // 高速增长阶段 g1
    this.terminalG = 0.025; // 永续增长率 g2
    this.wacc = 0.085;      // 折现率 WACC
    this.netDebt = 1500;    // 净债务
    this.shares = 600;      // 总股本 (百万股)
    this.currentPrice = 48.0; // 当前市场价

    this.render();
  }

  updateParams(params) {
    Object.assign(this, params);
    this.render();
  }

  calculateDCF(customWACC = this.wacc, customTermG = this.terminalG) {
    let pvFCF = 0;
    let lastFCF = this.fcf0;

    for (let t = 1; t <= this.growthYears; t++) {
      lastFCF *= (1 + this.growthRate);
      let pv = lastFCF / Math.pow(1 + customWACC, t);
      pvFCF += pv;
    }

    // Terminal Value (Gordon Growth)
    let tv = (lastFCF * (1 + customTermG)) / Math.max(0.005, customWACC - customTermG);
    let pvTV = tv / Math.pow(1 + customWACC, this.growthYears);

    let enterpriseValue = pvFCF + pvTV;
    let equityValue = enterpriseValue - this.netDebt;
    let intrinsicPerShare = equityValue / this.shares;
    let marginOfSafety = ((intrinsicPerShare - this.currentPrice) / this.currentPrice) * 100;

    return {
      pvFCF,
      pvTV,
      enterpriseValue,
      equityValue,
      intrinsicPerShare,
      marginOfSafety
    };
  }

  render() {
    const baseResult = this.calculateDCF();

    // 1. Render Summary Metrics
    if (this.metricsContainer) {
      let isUnder = baseResult.marginOfSafety >= 0;
      let tagClass = isUnder ? "badge-easy" : "badge-hard";
      this.metricsContainer.innerHTML = `
        <div class="stat-metric-card">
          <div class="stat-metric-title">每股内在价值 (Intrinsic Value)</div>
          <div class="stat-metric-val" style="color: ${isUnder ? 'var(--accent-green)' : 'var(--accent-red)'}">
            $${baseResult.intrinsicPerShare.toFixed(2)}
          </div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">
            当前股价: $${this.currentPrice.toFixed(2)} | 安全边际: 
            <span class="${tagClass}">${baseResult.marginOfSafety >= 0 ? '+' : ''}${baseResult.marginOfSafety.toFixed(1)}%</span>
          </div>
        </div>
        <div class="stat-metric-card">
          <div class="stat-metric-title">企业总价值 (Enterprise Value)</div>
          <div class="stat-metric-val">$${(baseResult.enterpriseValue / 1000).toFixed(2)}B</div>
          <div style="font-size:0.72rem; color:var(--text-muted); margin-top:2px;">
            显性现金流现值: $${(baseResult.pvFCF / 1000).toFixed(2)}B | 终值现值: $${(baseResult.pvTV / 1000).toFixed(2)}B
          </div>
        </div>
      `;
    }

    // 2. Render 5x5 Sensitivity Heatmap Table
    if (this.matrixContainer) {
      const waccs = [0.075, 0.080, 0.085, 0.090, 0.095];
      const termGs = [0.015, 0.020, 0.025, 0.030, 0.035];

      let html = `
        <table class="heatmap-table">
          <thead>
            <tr>
              <th style="text-align:left;">永续增长 \\ WACC</th>
              ${waccs.map(w => `<th ${w === this.wacc ? 'style="color:var(--accent-gold); border-bottom:2px solid var(--accent-gold)"' : ''}>${(w * 100).toFixed(1)}%</th>`).join('')}
            </tr>
          </thead>
          <tbody>
      `;

      termGs.forEach(g => {
        let isCurrentG = Math.abs(g - this.terminalG) < 0.001;
        html += `<tr><td style="font-weight:700; background:var(--bg-tertiary); ${isCurrentG ? 'color:var(--accent-gold);' : ''}">${(g * 100).toFixed(1)}%</td>`;

        waccs.forEach(w => {
          let res = this.calculateDCF(w, g);
          let diff = res.marginOfSafety;
          let isCurrentCell = isCurrentG && Math.abs(w - this.wacc) < 0.001;

          // Color scale
          let bgCol = "transparent";
          let textCol = "var(--text-primary)";
          if (diff > 25) {
            bgCol = "rgba(16, 185, 129, 0.35)";
            textCol = "#34d399";
          } else if (diff > 5) {
            bgCol = "rgba(16, 185, 129, 0.18)";
            textCol = "#10b981";
          } else if (diff > -5) {
            bgCol = "rgba(245, 158, 11, 0.2)";
            textCol = "#fbbf24";
          } else if (diff > -25) {
            bgCol = "rgba(244, 63, 94, 0.2)";
            textCol = "#f87171";
          } else {
            bgCol = "rgba(244, 63, 94, 0.4)";
            textCol = "#f43f5e";
          }

          let borderStyle = isCurrentCell ? 'outline: 2px solid var(--accent-gold); box-shadow: 0 0 10px rgba(245,158,11,0.5);' : '';
          html += `
            <td class="heatmap-cell" style="background:${bgCol}; color:${textCol}; ${borderStyle}" title="WACC: ${(w*100).toFixed(1)}%, g: ${(g*100).toFixed(1)}%, 估值: $${res.intrinsicPerShare.toFixed(2)}">
              $${res.intrinsicPerShare.toFixed(1)}
            </td>
          `;
        });
        html += `</tr>`;
      });

      html += `</tbody></table>`;
      this.matrixContainer.innerHTML = html;
    }
  }
}
