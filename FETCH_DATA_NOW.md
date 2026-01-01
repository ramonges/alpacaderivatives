# Fetch S&P 500 Options Data - Quick Guide

## Current Status
✅ Tables exist in Supabase  
✅ Code is ready  
⚠️  Need Alpaca secret key to fetch data

## Step 1: Add Alpaca Secret Key

1. **Create/Edit `.env` file** in the project root:
```bash
ALPACA_API_KEY=sacZc0e60Tffp4vbJcgvG62FpV0rrDXbGFEupQbn
ALPACA_SECRET_KEY=your_secret_key_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets

SUPABASE_URL=https://bbxcukvhekihomnevirr.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJieGN1a3ZoZWtpaG9tbmV2aXJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyODA2MjAsImV4cCI6MjA4Mjg1NjYyMH0.k-xiLQIaMw_11Unr1EtfhZS55Pa66u7-apArBTOyDoQ
```

2. **Get your Alpaca Secret Key**:
   - Go to: https://app.alpaca.markets/paper/dashboard/overview
   - Click on your API keys
   - Copy the "Secret Key"
   - Paste it in `.env` file as `ALPACA_SECRET_KEY`

## Step 2: Fetch Current Data

Once you've added the secret key, run:

```bash
python run_collector.py
```

This will:
- ✅ Verify it's fetching SPY (S&P 500) options
- ✅ Download current options chain
- ✅ Calculate Greeks
- ✅ Store in Supabase

## Step 3: Fetch Historical Data (Last 30 Days)

After getting current data, you can backfill historical:

```bash
python run_backfill.py
```

**Note**: Historical data is available from February 2024 onwards.

## What Gets Stored

- **options_data**: Current option prices, strikes, expirations
- **greeks_data**: Delta, Gamma, Theta, Vega, Rho
- **iv_evolution**: Implied volatility over time

## Troubleshooting

**"secret_key must be supplied"**
→ Add `ALPACA_SECRET_KEY` to `.env` file

**"No option contracts found"**
→ Check market hours (options data during trading hours)
→ Verify you have options data subscription in Alpaca

**"Table does not exist"**
→ Run `supabase_schema.sql` in Supabase SQL Editor

## Quick Start Command

```bash
# 1. Add secret key to .env
# 2. Then run:
python run_collector.py
```

That's it! Your database will be populated with S&P 500 options data.

