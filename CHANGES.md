```markdown
# CHANGELOG: KrakenMomentumBot Enhanced Edition

Comparison of architectural and algorithmic modifications between upstream KrakenMomentumBot and KrakenMomentumBot-Enhanced.

## 1. Zero-Downtime Dynamic Configuration (Hot-Reloading)
- **Upstream:** Config was evaluated strictly once on launch in `main()`. Changing values required killing the process, severing the WebSocket connection, and clearing memory.
- **Enhanced:** Added global `CURRENT_CONFIG` tracking and integrated `load_config()` directly into the live HUD timer loop[cite: 5]. Parameters like targets, windows, and thresholds update live on disk without dropping active WebSocket feeds[cite: 5].

## 2. Decoupled 30-Minute Price History Buffering
- **Upstream:** `SymbolState` pruned any tick older than 60 seconds on ingest, making lookback window expansion require an indicator warm-up.
- **Enhanced:** Decoupled retention from calculation with `MAX_HISTORY_SEC = 1800` (30 minutes)[cite: 5]. `momentum_pct()` and `volatility_pct()` perform non-destructive windowed lookups, allowing instant on-the-fly lookback adjustments[cite: 5].

## 3. Real-Time Proximity Scanner (`hud_scanner`)
- **Upstream:** Pairs were evaluated invisibly inside `maybe_trade()` with no terminal visibility until an order fired.
- **Enhanced:** Added `hud_scanner()` to print a structured metric matrix every HUD cycle with a `🔥 [HOT]` badge for pairs approaching entry thresholds[cite: 5].

## 4. Fee Friction Awareness & Target Calibration
- **Upstream:** Default targets (1.5% TP, 1.0% trail) incurred net losses under Kraken's base round-trip taker fees.
- **Enhanced:** Calibrated defaults and trailing stop offsets to ensure captured runs overcome exchange friction and slippage.

## 5. Security & Repository Hygiene
- **Enhanced:** Added `.gitignore` for `.env`, `config.json`, and `*.jsonl` transaction ledgers alongside a clean `config.example.json` template to prevent accidental credential or operational data leaks.

## 6. Duplicate Entry Prevention & Multi-Position Capacity
- **Upstream:** Evaluated all pairs every tick cycle, causing repeated market orders on the same coin while already in a position.
- **Enhanced:** `maybe_trade()` skips any asset already present in `positions`[cite: 5]. This locks in the initial entry price, allows trailing stops and take-profits to calculate accurately, and preserves open position slots for other candidate coins[cite: 5].

## 7. Open Position HUD Telemetry
- **Upstream:** Open positions were only reflected as a generic integer count in the HUD line.
- **Enhanced:** Added dedicated `💼 [OPEN]` status tags inside `hud_scanner()`[cite: 5]. Tracked pairs actively held in inventory display live entry price, real-time floating dollar PnL, and percentage return side-by-side with incoming market metrics[cite: 5].

## 8. Order Placement Fill Verification (Phantom Liquidation Defense)
- **Upstream:** `place_order()` returned `None` without inspecting Kraken's API response[cite: 2, 4]. `maybe_trade()` added rejected orders (e.g., `EOrder:Insufficient funds`) into `positions` regardless[cite: 2, 3, 4], subsequently triggering stop-loss market sells that liquidated pre-existing spot wallet balances[cite: 1, 3].
- **Enhanced:** Refactored `place_order()` to return a boolean (`bool`)[cite: 5]. Live orders are checked for `resp["result"]["txid"]` and an empty `error` array before returning `True`[cite: 5]. `maybe_trade()` only registers the asset in `positions` upon confirmed order submission, logging `[ENTRY ABORTED]` on API rejections to protect long-term account holdings[cite: 5].

## 9. Automated Time-Decay Exit (`max_hold_sec`)
- **Upstream:** Positions could only exit via fixed take-profit, trailing stop, or hard stop-loss[cite: 2]. Stagnant, low-volatility chop could tie up trading capital for many hours without resolution.
- **Enhanced:** Added `entry_time` timestamping to `Position` objects and integrated a configurable `max_hold_sec` rule into `manage_positions()`[cite: 5]. If a position exceeds its maximum hold duration without hitting profit or stop thresholds, the bot automatically executes a market exit (`[EXIT] TIME LIMIT ... reason=max_hold`), freeing capital for active momentum opportunities[cite: 5].

## 10. Asynchronous Scheduled Universe Refresh (`refresh_universe_sec`)
- **Upstream:** CoinGecko universe discovery was executed strictly once during startup in `main()`[cite: 2]. Market shifts required restarting the bot to track newly trending coins.
- **Enhanced:** Integrated a periodic background universe refresh governed by `refresh_universe_sec`[cite: 5]. CoinGecko calls run asynchronously off the event loop via `loop.run_in_executor()` to prevent blocking tick processing[cite: 5]. Newly qualified pairs subscribe incrementally via Kraken WebSocket v2 without dropping the connection, while dropped pairs are pruned safely only if they do not hold an active open position[cite: 5].

```