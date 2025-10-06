# Fabric Copilot & Data Agent Consumption Estimation Accelerator

> IMPORTANT DISCLAIMER: Although the code in this repository was created by a Microsoft employee, this is **NOT** an official Microsoft product, service, toolkit, nor a supported deliverable. It is an **unofficial accelerator / learning sample** built from field experience with customers and the publicly available Microsoft documentation. Use it at your own risk, validate results independently, and always rely on official tooling for final commercial or capacity sizing decisions like Fabric Capacity Metrics.

Web Apllication for Copilot & Data Agent CU Cumsumption developed with current repo: https://igomes01.github.io/fabric-ai-skills-cumsumption/

Official reference documentation that informed this accelerator:
- Copilot consumption fundamentals: https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-consumption
- Data Agent consumption fundamentals: https://learn.microsoft.com/en-us/fabric/fundamentals/data-agent-consumption

---

## 1. Purpose
This repository helps you quickly approximate token usage and high‑level Capacity Unit (CU) consumption scenarios for exploratory or early planning discussions around Microsoft Fabric Copilot / Data Agent usage patterns. It provides both:

1. A static, infrastructure‑free web interface (for non‑developers) hosted easily via GitHub Pages.
2. Python CLI utilities (for higher fidelity token counts) using the same tokenization approach applied in internal experimentation (via `tiktoken`).

It is **not a replacement** for official guidance nor for the **Fabric Capacity Metrics application**, which remains the authoritative source for final sizing decisions. Treat every output here as a directional aid, not a commitment.

---

## 2. Accuracy Ladder
In order of increasing reliability:
1. **Static web interface** (`index.html`) – Uses simple heuristic (character length ÷ 4). Fast and lightweight, but least accurate.
2. **Python CLI scripts** (`tokens_calculator.py`, `manual_cu_estimator.py`) – Higher accuracy using native `tiktoken` library for proper tokenization.
3. **Official Fabric Capacity Metrics** ([outside this repo](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)) – Final and authoritative for planning & procurement.

Whenever possible, move “up” the ladder before making decisions.

---

## 3. Key Components

| File | Role |
|------|------|
| `index.html` | Static multi‑line token & word analyzer (client‑side; bilingual support) using simple heuristic tokenization. |
| `capacity.html` | Lightweight page to experiment with capacity KPIs given average token assumptions. |
| `tokens_calculator.py` | Consolidated CLI for multi‑line token analysis + optional capacity estimation (contains embedded analysis logic). |
| `manual_cu_estimator.py` | CLI focused on manual CU scenario calculations (users, questions per user, etc.). |
| `requirements.txt` | Python dependencies (not required for pure static site usage). |

*(Some earlier supporting modules were merged for simplicity.)*

---

## 4. Estimation Model (Simplified)

Current approximation (subject to refinement):

```
output_tokens = input_tokens * 4
cu_seconds    = (input_tokens * 100 + output_tokens * 400) / 1000
cu_hours      = cu_seconds / 3600
capacity_need = (requests_per_day * cu_hours) / 24
```

Where:
- `input_tokens` – Average prompt / question tokens.
- `output_tokens` – Assumes a 4× expansion factor (illustrative ratio; adjust as your scenario dictates).
- `requests_per_day` – Derived from `users_per_day * questions_per_user_per_day`.
- `capacity_need` – Approximate average CU requirement per day (directional only).

> CAUTION: Ratios and multipliers here are **not** official published guarantees; they are illustrative for early ideation. Always validate your real workloads and finalize with the Fabric Capacity Metrics.

---

## 5. Tokenization Strategy

CLI scripts use the Python `tiktoken` library (default model key: `gpt-4o-mini`, falling back to a base encoding for unknown models). 

The static site (`index.html`) uses a **simplified heuristic approach**: `length / 4` for all token estimations. This keeps the interface lightweight and dependency-free, but sacrifices accuracy compared to proper tokenization libraries.

**No external libraries or fallback chains are currently implemented in the web interface.** All processing remains local to the browser.

---

## 6. Getting Started (Python CLI)

### 6.1. Environment Setup (Windows example)
```cmd
cd "your-repo-folder"
python -m venv .venv
".venv\Scripts\activate"
pip install -r requirements.txt
```

### 6.2. Interactive Token & Capacity Exploration
```cmd
python tokens_calculator.py
```
Paste one question per line, press Enter on an empty line to finish, then opt-in to capacity estimation.

### 6.3. JSON Mode (Automated / Scripting)
```cmd
python tokens_calculator.py --json --text "What is sales by region?\nList top products" --capacity --users-per-day 1500 --questions-per-user 5
```

### 6.4. Manual CU Estimation Only
```cmd
python manual_cu_estimator.py
```

### 6.5. Piping Text (PowerShell)
```powershell
@" 
Compare regional sales performance
Highlight top 5 growth products
"@ | python tokens_calculator.py --json
```

---

## 7. Static Web Pages (GitHub Pages)

The web assets (`index.html`, `capacity.html`) are pure static files:
1. Enable GitHub Pages → Build from `main` branch (root).
2. Access `https://YOUR_USER.github.io/YOUR_REPO/`.
3. Paste lines, compute metrics, optionally export results.

> The web interface uses a simple character-based heuristic (length ÷ 4) for all tokenization, which is fast but not as accurate as proper tokenization. For the **most reliable token counts, prefer the Python CLI tools.**

---

## 8. Recommended Workflow

| Stage | Activity | Tool | Purpose |
|-------|----------|------|---------|
| Ideation | Rapid question drafting & rough sizing | Static site | Fast, no setup |
| Refinement | More accurate token counts | `tokens_calculator.py` | Real `tiktoken` usage |
| Scenario modeling | CU sensitivity (users / questions) | `manual_cu_estimator.py` | Focus on demand variables |
| Final validation | Official capacity alignment | Fabric Capacity Metrics | Authoritative |

---

## 9. Limitations
* Not an official licensing or billing tool.
* Ratios (e.g., output = 4 × input) are illustrative defaults.
* No guarantee of parity with evolving service internals.
* Does not model concurrency bursts, throttling, network overhead, or caching effects.
* Web interface heuristic (length ÷ 4) may significantly under/overestimate token counts, especially for non-English text or code samples.
* No consideration for model-specific tokenization differences in the web interface.

---

## 10. Extensibility Ideas
* Add configurable output token expansion ratios per scenario.
* Integrate empirical sampling (log real tokens from prototype instrumentation).
* Expose CSV / JSON batch processing for large prompt inventories.
* Add confidence bands (min / P50 / P95) over token volatility.

---

## 11. Contributing
Contributions are welcome strictly as community goodwill. By submitting a PR you acknowledge this is an **unofficial sample** and may change or be archived without notice.

Proposed flow:
1. Fork
2. Branch (`feat/your-improvement`)
3. Commit with clear message
4. Open Pull Request (describe rationale & validation)

---

## 12. Support & Warranty
No SLA, no formal support channel, no warranty—provided **AS IS**. For production design decisions consult official Microsoft documentation and tooling.

---

## 13. License
If a LICENSE file is not present, treat this as a sample provided without explicit license grant beyond typical fair use for learning. Add a license file (e.g., MIT) before distributing or incorporating into broader solutions.

---

## 14. Final Reminder
Always corroborate any directional estimates here with the **Fabric Capacity Metrics** and official documentation:
- https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-consumption
- https://learn.microsoft.com/en-us/fabric/fundamentals/data-agent-consumption

> This accelerator shortens the iteration loop; it does not replace authoritative sizing or commercial guidance.

---

_Built as an accelerator informed by real-world patterns and public docs—use responsibly and validate continuously._