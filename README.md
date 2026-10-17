```markdown
# KrakenMomentumBot (Enhanced Edition)

A fully standalone, high-performance momentum trading bot built for Kraken Spot Markets[cite: 5].

`KrakenMomentumBot-Enhanced` combines real-time streaming data, statistical momentum filters, Monte Carlo predictive path simulation, hot-reloading configurations, dynamic exchange catalog discovery, and granular execution risk controls[cite: 5].

---

## Key Features

- **Real-Time Kraken WebSocket v2 Streaming:** Continuous market feed ingestion without polling latency[cite: 5].
- **Dynamic Asset Discovery:** Scans Kraken's public `/0/public/AssetPairs` catalog on startup and during scheduled hourly intervals to identify and trade qualifying USD spot pairs dynamically without hardcoded whitelists[cite: 5].
- **CoinGecko Market Intersection:** Filters candidates by cross-referencing top volume and top market cap lists while excluding pegged stablecoins[cite: 5].
- **Decoupled 30-Minute Price History Buffering:** Non-destructive rolling lookback memory allows changing indicators on the fly without waiting for a re-warm period[cite: 5].
- **Multi-Factor Entry Scoring:** Combines price velocity (momentum), RSI, volatility fences, and forward Monte Carlo path confidence[cite: 5].
- **Live Proximity Scanner (`hud_scanner`):** Terminal UI showing real-time metrics, live floating PnL on open positions, and a `🔥 [HOT]` radar for coins nearing entry thresholds[cite: 5].
- **Execution Validation Guard:** Validates order placement responses before recording positions, eliminating phantom position tracking and accidental account liquidations[cite: 5].
- **Time-Decay Exit (`max_hold_sec`):** Closes trades automatically if price action chops sideways without triggering take-profit or stop-loss limits[cite: 5].
- **Zero-Downtime Hot-Reloading:** Adjust parameters in `config.json` while the bot is running; updates take effect on the next HUD tick without dropping WebSocket connections[cite: 5].
- **Zero Private Dependencies:** No proprietary AI, regime engines, or remote servers required[cite: 6]. Everything runs locally and deterministically[cite: 6].

---

## Operating Modes

### 1. PAPER Mode (Default, Safe)

By default, the bot runs in `PAPER` mode[cite: 5, 6]:
- Simulated order execution with zero capital risk[cite: 6].
- No API keys required[cite: 6].
- Full signal evaluation, Monte Carlo simulation, and position tracking[cite: 5].
- All activities logged locally to `kraken_orders_log.jsonl`[cite: 5, 6].

To explicitly set or reset your environment to paper mode:

```powershell
$env:KRAKEN_MOMENTUM_MODE = "paper"

```

### 2. LIVE Mode (Real Trading)

To engage live execution on Kraken Spot:

1. Set your environment variable:
```powershell
$env:KRAKEN_MOMENTUM_MODE = "live"

```


2. Export your Kraken API credentials:
```powershell
$env:KRAKEN_API_KEY = "your_api_key_here"
$env:KRAKEN_API_SECRET = "your_api_secret_here"

```


3. Configure your risk and sizing parameters in `config.json`.


4. Launch `bot.py`.



Note: API keys are loaded strictly from system environment variables and are never stored in repository files.

---

# CONFIG SETTINGS & PARAMETER DEFINITIONS

Below is the complete `config.json` schema incorporating all risk management, momentum, simulation, and discovery parameters:

```json
{
  "base_position_usd": 133.0,
  "max_open_positions": 3,
  "momentum_window_sec": 180,
  "momentum_threshold_pct": 0.25,
  "rsi_period": 14,
  "rsi_min_long": 48.0,
  "vol_min_pct": 0.05,
  "vol_max_pct": 3.0,
  "take_profit_pct": 2.5,
  "hard_sl_pct": 0.7,
  "trail_start_pct": 1.2,
  "trail_step_pct": 0.4,
  "max_hold_sec": 3600,
  "refresh_universe_sec": 3600,
  "mc_min_conf": 0.55,
  "mc_paths": 1000,
  "mc_horizon_sec": 60,
  "hud_interval_sec": 10.0
}

```

---

## Parameter Definitions

### Capital Allocation & Position Risk Management

* **`base_position_usd`** `(float)`: Baseline order size in USD prior to Monte Carlo sizing multipliers. Sizing multiplies up to 1.5x based on path confidence, capping allocation per trade.


* **`max_open_positions`** `(int)`: Maximum number of concurrent active positions allowed across the entire universe. Once reached, new candidate scoring is bypassed until a position closes.


* **`hard_sl_pct`** `(float)`: Fixed stop-loss percentage below entry price. Immediately triggers a market flat exit order if breached.


* **`take_profit_pct`** `(float)`: Fixed take-profit target percentage above entry price. Automatically liquidates the position to lock in peak gains during strong price spikes.


* **`trail_start_pct`** `(float)`: Percentage gain above entry required before the dynamic trailing stop activates. Ensures trailing only engages once fee friction hurdles have been cleared.


* **`trail_step_pct`** `(float)`: Percentage distance maintained below the peak price once trailing is engaged. If the market pulls back by this percentage from its highest recorded peak, the trade closes.


* **`max_hold_sec`** `(float | int)`: Maximum holding duration in seconds for any open position. If a trade does not reach a take-profit or stop-loss within this timeframe, it is exited via market order to free capital. Set to `0` to disable.



### Momentum, Trend & Volatility Filters

* **`momentum_window_sec`** `(int)`: Rolling lookback window in seconds used to evaluate price velocity. Dynamically slices the internal 30-minute buffer without requiring an indicator re-warm.


* **`momentum_threshold_pct`** `(float)`: Minimum percentage price gain required across the lookback window to qualify as a valid entry candidate.


* **`rsi_period`** `(int)`: Number of closed price intervals used to calculate the Relative Strength Index.


* **`rsi_min_long`** `(float)`: Minimum RSI threshold required to approve a long entry. Filters out stagnant assets while permitting entries on momentum breakouts.


* **`vol_min_pct`** `(float)`: Minimum price movement percentage required over the lookback window to confirm active market liquidity.


* **`vol_max_pct`** `(float)`: Maximum allowable price volatility percentage over the lookback window. Rejects trades during erratic spreads or abnormal wick spikes.



### Dynamic Universe & Discovery

* **`refresh_universe_sec`** `(float | int)`: Frequency in seconds at which the bot queries CoinGecko and Kraken's `/0/public/AssetPairs` catalog in the background. Dynamically subscribes to newly qualified movers and prunes flat pairs without interrupting WebSocket connectivity or active positions.



### Monte Carlo Simulation Engine

* **`mc_min_conf`** `(float)`: Minimum forward-path win probability required to approve an order.


* **`mc_paths`** `(int)`: Number of simulated price trajectories computed per candidate coin during each evaluation pass.


* **`mc_horizon_sec`** `(int)`: Forward projection horizon in seconds for each simulated trajectory.



### Telemetry & Hot-Reload Engine

* **`hud_interval_sec`** `(float)`: Cadence in seconds between terminal UI table refreshes, position management evaluations, and `config.json` disk hot-reloads.



---

## Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/YourUser/KrakenMomentumBot.git](https://github.com/YourUser/KrakenMomentumBot.git)
cd KrakenMomentumBot

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up configuration:**
```bash
cp config.example.json config.json

```


4. **Launch the bot:**
```bash
python bot.py

```



---

## Repository Structure

* `bot.py` — Primary asynchronous trading engine, WebSocket feed handler, and position manager.


* `config.json.normal` — Reasonable normal configuration file loaded and reloaded on the fly. Copy to CONFIG.JSON


* `config.json.wild` — WILD and UNREASONABLE configuration template. Use to test triggers and logic in development mode. Kinda fun to watch in PAPER MODE ONLY


* `kraken_orders_log.jsonl` — Local append-only log recording every simulated and live order event.


* `requirements.txt` — Python package dependencies (`websockets`, `requests`).


* `CHANGELOG.md` — Detailed record of architectural and algorithmic modifications.
* `README.md` — Documentation and operational guide.



---

## Legal & Safety Disclaimer

This software is for educational, research, and experimental purposes only.

* **Not Financial Advice:** Nothing contained in this software or documentation constitutes investment or financial advice.


* **No Liability:** Cryptocurrency trading involves substantial financial risk. The authors and contributors assume no liability for financial losses, software bugs, execution slippage, exchange outages, or API errors.


* **User Responsibility:** You are solely responsible for testing strategies in `PAPER` mode, verifying order sizing, securing API credentials, and complying with all relevant local financial regulations.



```

```