# FinSight ✦ Fractional CFO & Runway Decision Engine

> **A domain-specific AI financial co-pilot built to solve "runway blindness" for independent operators, tech freelancers, and agencies navigating macroeconomic volatility.**

![FinSight Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Deterministic%20%2B%20LLM-00f2fe?style=for-the-badge)
![Eval Accuracy](https://img.shields.io/badge/Eval%20Benchmark-90%25%20Accuracy-00ff88?style=for-the-badge)
![Avg Latency](https://img.shields.io/badge/Inference%20Latency-~1.5s-ffd166?style=for-the-badge)

---

## 💡 The Problem
In high-inflation, volatile economies (like Nigeria's dynamic market), business operators face constant financial shocks: 30–60 day client invoice lags, sudden fuel/overhead spikes, and currency depreciation. Most independent operators make major commitments (hiring staff, leasing office space, purchasing workstations) based on raw bank account balances rather than true cash runway, leading to sudden insolvency.

**FinSight bridges the gap between raw natural language questions and rigid financial math.**

---

## 🏛️ System Architecture

FinSight follows **Rule #1 of Production AI Engineering**: *Never ask an LLM to do arithmetic that deterministic code can compute with 100% precision.*

```text
   [ User Query / Prompt ]
              │
              ▼
  ┌───────────────────────┐
  │  FastAPI NLP Extractor│ ───► Gemini 3.5 Flash-Lite (Pydantic Schema)
  └───────────────────────┘      Extracts: income, expenses, savings, cost
              │
              ▼
  ┌───────────────────────┐
  │ Deterministic Engine  │ ───► Calculates:
  │   (React Client)      │      • Net Balance & Cash Left After Decision
  └───────────────────────┘      • Emergency Runway Months (to 0.1 precision)
              │
              ▼
  ┌───────────────────────┐
  │  Fractional CFO Model │ ───► Structured Executive Briefing
  │      (FastAPI)        │      • 1. Verdict (Safe / Caution / Hold)
  └───────────────────────┘      • 2. 60-Day Invoice Lag Stress Test
                                 • 3. Tactical Risk Mitigation Steps

```
---

## ⚡ Key Features

1. **Natural Language Scenario Extraction (`/api/extract`):**
   * Translates messy human queries (*"I make 2.5m and spend 800k, can I rent an office for 400k?"*) into validated financial figures.
   * Handles local financial shorthand (`k` -> 1,000, `m` -> 1,000,000).
   * Enforces strict Pydantic JSON contracts via Gemini Structured Outputs.

2. **Deterministic Stress-Testing & Interactive Sliders:**
   * Instant recalculation of runway cushions and a simulated 20% revenue drop scenario.
   * Bidirectional sync between natural language input and UI slider state.

3. **Resilient Async Backend with Exponential Backoff:**
   * Offloads synchronous SDK calls to worker threads (`asyncio.to_thread`) to prevent blocking FastAPI's event loop.
   * Built-in retry mechanism with exponential backoff (`2 ** attempt`) for API rate-limit resilience.

4. **Production-Grade Evaluation Suite (`test_evals.py`):**
   * Decoupled 10-case evaluation dataset representing real-world Nigerian macroeconomic shocks (Lekki rent traps, FX windfalls, ghosting clients).
   * Benchmarked at **90.0% accuracy** with an average latency of **~1.5s per decision**.

---

## 📊 Evaluation & Benchmarks

Automated regression suite run against real-world economic edge cases:

| Scenario | Financial Profile | Expected Verdict | AI Decision | Latency | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| Luxury car with ₦150k savings | ₦400k Inc / ₦2.5M Cost | `CRITICAL RISK - HOLD` | `CRITICAL RISK - HOLD` | 1.63s | ✅ PASS |
| Lekki rent + diesel eating 85% | ₦1.2M Inc / ₦400k Cost | `CRITICAL RISK - HOLD` | `CRITICAL RISK - HOLD` | 0.94s | ✅ PASS |
| Client invoice delay (₦0 revenue) | ₦0 Inc / ₦350k Cost | `CRITICAL RISK - HOLD` | `CRITICAL RISK - HOLD` | 0.95s | ✅ PASS |
| Premature agency hiring | ₦1M Inc / ₦600k Cost | `CRITICAL RISK - HOLD` | `CRITICAL RISK - HOLD` | 0.95s | ✅ PASS |
| FX contract + ₦1.8M solar inverter | ₦3M Inc / ₦9M Sav | `PROCEED WITH CAUTION` | `PROCEED WITH CAUTION` | 3.25s | ✅ PASS |
| Safe social media hire | ₦3.5M Inc / ₦12M Sav | `SAFE TO PROCEED` | `SAFE TO PROCEED` | 1.21s | ✅ PASS |
| Productivity M3 MacBook purchase | ₦2.5M Inc / ₦8M Sav | `PROCEED WITH CAUTION` | `PROCEED WITH CAUTION` | 1.91s | ✅ PASS |
| Wuse 2 co-working space upgrade | ₦1.5M Inc / ₦3.8M Sav | `PROCEED WITH CAUTION` | `PROCEED WITH CAUTION` | 0.96s | ✅ PASS |
| Retainer drop ad-spend test | ₦1.2M Inc / ₦3.5M Sav | `PROCEED WITH CAUTION` | `PROCEED WITH CAUTION` | 2.29s | ✅ PASS |
| Camera equipment lease | ₦1.4M Inc / ₦3M Sav | `PROCEED WITH CAUTION` | `PROCEED WITH CAUTION` | 4.97s | ✅ PASS |

**Overall Benchmark Score: 10/10 (100% Calibrated Accuracy) | Mean Latency: 1.84s**

---

## 🛠️ Tech Stack

* **Frontend:** React 19, Vite, React Markdown, Vanilla CSS (Custom Obsidian/Cyan Glassmorphic Design Tokens)
* **Backend:** Python 3.12+, FastAPI, Uvicorn, Pydantic v2
* **AI & LLM:** Google Gemini 3.5 Flash-Lite via `google-genai` SDK
* **Testing & Evals:** Custom automated evaluation runner with latency and accuracy instrumentation

---

### 🚀 Quickstart Guide

### 1. Backend Setup
```bash
cd server
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `server/` directory:
```env
GEMINI_API_KEY=your_api_key_here
```

Start the FastAPI Server:
```bash
uvicorn main:app --reload --port 8000
```

Run the AI Evaluation suite:
```bash
python test_evals.py
```

### 2. Frontend Setup
```bash
# In the project root
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🛡️ License & Acknowledgments
Built as part of my AI Engineering Journey and as my Debut Project. Designed with a tailored economic focus for independent operators navigating volatile market conditions.
