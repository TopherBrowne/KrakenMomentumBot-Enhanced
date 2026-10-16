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
