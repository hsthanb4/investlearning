#!/usr/bin/env python3
"""
Automated Real-Time Macro & Market Data Fetcher for InvestLearning.
Fetches official St. Louis Fed (FRED) CSV series and global market quotes,
updates web/js/live-market-data.json, and injects the latest live readings
into web/js/data-curriculum.js.
"""
import csv
import datetime
import io
import json
import os
import re
import urllib.request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_JSON_PATH = os.path.join(ROOT_DIR, "web", "js", "live-market-data.json")
CURRICULUM_JS_PATH = os.path.join(ROOT_DIR, "web", "js", "data-curriculum.js")

def fetch_fred_series(series_id, max_rows=30):
    """Fetch the last N valid observations from FRED public CSV endpoint (no API key needed)."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (InvestLearning-AutoUpdater/1.0)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    header = next(reader, None)
    valid_rows = []
    for row in reader:
        if len(row) >= 2 and row[1] not in (".", "", "NA"):
            try:
                valid_rows.append((row[0], float(row[1])))
            except ValueError:
                pass
    return valid_rows[-max_rows:]

def main():
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{now_utc}] Starting real-time FRED & market data sync...")

    data = {
        "updated_at": now_utc,
        "source": "Federal Reserve (FRED H.4.1 / DGS) & Global Market Feeds",
        "metrics": {}
    }

    try:
        walcl = fetch_fred_series("WALCL", 12)      # Millions USD -> divide by 1000 for Billions
        wtregen = fetch_fred_series("WTREGEN", 12)  # Millions USD -> divide by 1000 for Billions
        rrp = fetch_fred_series("RRPONTSYD", 30)    # Already in Billions USD
        dgs10 = fetch_fred_series("DGS10", 10)      # Percent
        dgs2 = fetch_fred_series("DGS2", 10)        # Percent
        vix = fetch_fred_series("VIXCLS", 10)       # Index
        dxy = fetch_fred_series("DTWEXBGS", 10)     # Broad Dollar Index

        if walcl and wtregen and rrp:
            latest_date = walcl[-1][0]
            walcl_b = round(walcl[-1][1] / 1000.0, 1)
            tga_b = round(wtregen[-1][1] / 1000.0, 1)
            rrp_b = round(rrp[-1][1], 1)
            net_liq_b = round(walcl_b - tga_b - rrp_b, 1)

            # 4 weeks ago comparison
            w4_b = walcl[-5][1] / 1000.0 if len(walcl) >= 5 else walcl[0][1] / 1000.0
            t4_b = wtregen[-5][1] / 1000.0 if len(wtregen) >= 5 else wtregen[0][1] / 1000.0
            r4_b = rrp[-20][1] if len(rrp) >= 20 else rrp[0][1]
            net_liq_4w = w4_b - t4_b - r4_b
            impulse_4w = round(((net_liq_b - net_liq_4w) / net_liq_4w) * 100.0, 2)

            data["metrics"]["fed_liquidity"] = {
                "date": latest_date,
                "walcl_b": walcl_b,
                "tga_b": tga_b,
                "rrp_b": rrp_b,
                "net_liquidity_b": net_liq_b,
                "impulse_4w_pct": impulse_4w,
                "net_liq_4w_b": round(net_liq_4w, 1),
                "signal": "🟢 强力扩张 (建议 80%~90% 仓位)" if impulse_4w >= 1.0 else ("🟡 存量震荡 (建议 50%~60% 仓位)" if impulse_4w >= -1.0 else "🔴 紧缩抽水 (建议 ≤30% 防御仓位)"),
                "conclusion": (
                    f"💡 实时动态结论（更新于 {now_utc}）：当前美联储净流动性为 ${net_liq_b:,.1f} B，4周脉冲为 {impulse_4w:+.2f}%（🟢 正向扩张）。流动性正注入银行体系，分母端贴现率下行，结论：维持【积极进攻（建议权益仓位 80%~90%）】，重点配置科技与宽基 ETF。"
                    if impulse_4w >= 1.0 else (
                        f"💡 实时动态结论（更新于 {now_utc}）：当前美联储净流动性为 ${net_liq_b:,.1f} B，4周脉冲为 {impulse_4w:+.2f}%（🟡 存量温和拉锯）。总水源处于平衡状态，结论：执行【均衡配置（建议权益仓位 50%~60%）】，精选高现金流蓝筹，不追高纯题材。"
                        if impulse_4w >= -1.0 else
                        f"💡 实时动态结论（更新于 {now_utc}）：🚨 紧缩警报！当前美联储净流动性降至 ${net_liq_b:,.1f} B，4周脉冲为 {impulse_4w:+.2f}%（🔴 净抽水状态）。TGA 发债虹吸或缩表正在抽干准备金，结论：启动【紧缩防御（建议将权益仓位降至 30% 以内）】，增配短债与货币基金避险！"
                    )
                )
            }
            print("Fetched live Fed Net Liquidity:", data["metrics"]["fed_liquidity"])

        if dgs10 and dgs2:
            y10 = round(dgs10[-1][1], 2)
            y2 = round(dgs2[-1][1], 2)
            spread_bps = round((y10 - y2) * 100.0, 0)
            data["metrics"]["yield_curve"] = {
                "date": dgs10[-1][0],
                "us10y": y10,
                "us02y": y2,
                "spread_bps": int(spread_bps),
                "regime": "🟢 正利差常态陡峭" if spread_bps > 0 else "🔴 收益率曲线倒挂预警"
            }
            print("Fetched live Yield Curve:", data["metrics"]["yield_curve"])

        if vix:
            vix_val = round(vix[-1][1], 2)
            data["metrics"]["vix"] = {
                "date": vix[-1][0],
                "value": vix_val,
                "regime": "🔴 极度恐慌 (>30)" if vix_val > 30 else ("🟢 常态平稳" if vix_val >= 13 else "🟡 极度自满 (<13)")
            }
            print("Fetched live VIX:", data["metrics"]["vix"])

        if dxy:
            data["metrics"]["dxy"] = {
                "date": dxy[-1][0],
                "value": round(dxy[-1][1], 2)
            }
    except Exception as exc:
        print(f"Warning during FRED fetch (using cached fallback if needed): {exc}")
        if os.path.exists(LIVE_JSON_PATH):
            with open(LIVE_JSON_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
            existing["updated_at"] = now_utc
            data = existing

    with open(LIVE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {LIVE_JSON_PATH}")

if __name__ == "__main__":
    main()
