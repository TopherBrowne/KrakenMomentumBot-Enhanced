# KrakenMomentumBot (Open-Source Edition)

A fully standalone, paper-mode-first momentum trading bot for Kraken.

This bot uses:

- Real-time Kraken WebSocket price data
- Momentum signals
- RSI filtering
- Volatility filtering
- Monte Carlo-style confidence scoring
- Trailing stops
- Hard stop-loss
- Take-profit logic

There is:

- No Overseer system
- No AI Reviewer
- No regime engine
- No private infrastructure
- No bundled API keys

Everything runs locally and independently.

## Default Mode: PAPER (Safe)

By default, the bot runs in PAPER mode:

- No real orders are sent
- No API keys are required
- All trades are simulated
- Logs are local

This is ideal for learning, testing, and experimentation.

## Live Trading (Optional, At Your Own Risk)

To enable live trading:

1. Copy config.example.json to config.json
2. In config.json, change:

   "mode": "paper"

   to:

   "mode": "live"

3. Set your Kraken API keys as environment variables:

   KRAKEN_API_KEY=your_key_here  
   KRAKEN_API_SECRET=your_secret_here  

4. Restart the bot.

Your keys are never stored in this repo. You must provide your own.

## Legal & Safety Disclaimer

This project is provided for educational and experimental purposes only.

- This is NOT financial advice.
- You assume all risk when using this bot.
- You are responsible for complying with your local laws.
- You are responsible for your own trading decisions.
- The authors and contributors are NOT liable for any financial losses.

If you enable live trading, you do so at your own risk.

# CONFIG SETTINGS & PARAMETER DEFINITIONS

Below is the complete `config.json` schema and detailed parameter reference incorporating the settings calibrated for `KrakenMomentumBot-Enhanced`:

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
  "take_profit_pct": 4.5,
  "hard_sl_pct": 0.7,
  "trail_start_pct": 2.5,
  "trail_step_pct": 0.5,
  "mc_min_conf": 0.55,
  "mc_paths": 1000,
  "mc_horizon_sec": 60,
  "hud_interval_sec": 10.0
}

```

---

## Parameter Definitions

### Capital Allocation & Risk Management

* **`base_position_usd`** `(float)`: Baseline order size in USD prior to Monte Carlo sizing multipliers. Calibrated to `133.0` so that maximum Monte Carlo path confidence (1.5x) caps position sizing at exactly **$200** notional.
* **`max_open_positions`** `(int)`: Maximum number of concurrent active positions allowed across the universe. Calibrated to `3` to allocate up to **$600** total trading capital (3 x $200).
* **`hard_sl_pct`** `(float)`: Fixed stop-loss percentage below entry price. Immediately triggers a market exit order if breached. Calibrated to `0.7` (-0.7%).
* **`take_profit_pct`** `(float)`: Fixed take-profit target percentage above entry price. Triggers an immediate market exit to lock in gains. Calibrated to `4.5` (+4.5%) to clear Kraken's ~1.60% round-trip taker friction and secure net profitability.
* **`trail_start_pct`** `(float)`: Percentage gain above entry required before the dynamic trailing stop activates. Calibrated to `2.5` (+2.5%) to ensure stops only lock in after crossing the round-trip fee hurdle.
* **`trail_step_pct`** `(float)`: Percentage distance maintained below the peak price once trailing is engaged. If price drops by this percentage from its highest recorded peak, the position closes. Calibrated to `0.5` (0.5%).

### Momentum & Signal Filters

* **`momentum_window_sec`** `(int)`: Rolling lookback window in seconds used to evaluate price velocity without modifying the global memory retention buffer. Calibrated to `180` (3 minutes) to smooth out tick-level noise while preserving short-term momentum signals.
* **`momentum_threshold_pct`** `(float)`: Minimum percentage price gain required across the lookback window to qualify as a valid entry candidate. Calibrated to `0.25` (+0.25%).
* **`rsi_period`** `(int)`: Number of closed tick intervals used to calculate Relative Strength Index. Calibrated to `14`.
* **`rsi_min_long`** `(float)`: Minimum RSI threshold required to approve a long entry. Calibrated to `48.0` to permit entry on early-stage reversal bounces off local lows.
* **`vol_min_pct`** `(float)`: Minimum rolling volatility required over the window to ensure sufficient liquidity and price movement. Calibrated to `0.05` (0.05%).
* **`vol_max_pct`** `(float)`: Maximum rolling volatility percentage allowed. Calibrated to `3.0` (3.0%) to prevent entering erratic slippage spikes or abnormal order book spreads.

### Monte Carlo Simulation Engine

* **`mc_min_conf`** `(float)`: Minimum simulated forward-path win probability required to approve execution. Calibrated to `0.55` (55% positive forward paths).
* **`mc_paths`** `(int)`: Number of simulated price paths computed per candidate coin during each evaluation pass. Calibrated to `1000`.
* **`mc_horizon_sec`** `(int)`: Forward projection horizon in seconds for each simulated path. Calibrated to `60`.

### System & Hot-Reload Engine

* **`hud_interval_sec`** `(float)`: Evaluation frequency in seconds. Controls the interval between live market scans, console HUD table refreshes, position management checks, and config.json disk hot-reloads. Calibrated to `10.0`.

```

```

## Project Structure

- bot.py — main trading engine
- config.example.json — example configuration (copy to config.json)
- requirements.txt — Python dependencies
- README.md — this file

## Installation

Clone the repo:

    git clone https://github.com/YourUser/KrakenMomentumBot.git
    cd KrakenMomentumBot

Install dependencies:

    pip install -r requirements.txt

Copy the example config:

    cp config.example.json config.json

Run the bot:

    python bot.py

## Standalone Design

This open-source edition is:

- Fully standalone
- No AI Reviewer
- No regime engine
- No Overseer integration
- No internal file paths
- No private modules

Everything runs locally and independently.
