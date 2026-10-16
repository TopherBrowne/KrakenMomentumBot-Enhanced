# CHANGELOG: KrakenMomentumBot Enhanced Edition

Comparison of architectural and algorithmic modifications between upstream KrakenMomentumBot and KrakenMomentumBot-Enhanced.

## 1. Zero-Downtime Dynamic Configuration (Hot-Reloading)
- Upstream: Config was evaluated strictly once on launch in main(). Changing values required killing the process, severing the WebSocket connection, and clearing memory.
- Enhanced: Added global CURRENT_CONFIG tracking and integrated load_config() directly into the 10-second HUD timer loop. Parameters update live without dropping feeds.

## 2. Decoupled 30-Minute Price History Buffering
- Upstream: SymbolState pruned any tick older than 60 seconds on ingest, making window expansion require an indicator warm-up.
- Enhanced: Decoupled retention from calculation with MAX_HISTORY_SEC = 1800 (30 minutes). momentum_pct() and volatility_pct() now perform non-destructive lookups, allowing instant lookback adjustments.

## 3. Real-Time Proximity Scanner (hud_scanner)
- Upstream: Pairs were evaluated invisibly inside maybe_trade() with no visibility until an order fired.
- Enhanced: Added hud_scanner() to print a structured metric matrix every 10 seconds with a ?? [HOT] badge for pairs nearing entry gates.

## 4. Fee Friction Awareness & Target Calibration
- Upstream: Default targets (1.5% TP, 1.0% trail) incurred losses under Kraken's ~1.60% round-trip taker fees.
- Enhanced: Calibrated targets to 4.5% TP and 2.5% trail start to clear exchange friction hurdles.

## 5. Security & Repository Hygiene
- Enhanced: Added .gitignore for .env, config.json, and *.jsonl transaction ledgers alongside a clean config.example.json template.

## 6. Fixed redundant orders once thresholds are met
- Eliminates redundant orders: If an asset already has an open position in positions, it is bypassed during candidate scoring. This locks in the initial entry price, allows trailing stops and take-profits to calculate accurately, and preserves open position capacity for other coins.

## 7. Added open positions to HUD
- Show open positions for pairs. Display entry and PnL. Normal display if not open.
