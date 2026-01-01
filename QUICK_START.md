# Quick Start Guide - S&P 500 Options Data

## ✅ System is Configured for S&P 500 (SPY) Options

The system is already set up to download S&P 500 options data. Here's how to use it:

## Step 1: Set Up Database

1. Go to Supabase: https://bbxcukvhekihomnevirr.supabase.co
2. Run SQL from `supabase_schema.sql` in SQL Editor

## Step 2: Configure API Keys

Create `.env` file:
```bash
ALPACA_API_KEY=sacZc0e60Tffp4vbJcgvG62FpV0rrDXbGFEupQbn
ALPACA_SECRET_KEY=your_secret_key_here
```

## Step 3: Download Historical S&P 500 Options Data

### Option A: Backfill Last 30 Days (Recommended First)
```bash
python backend/historical_backfill.py
```

### Option B: Backfill Specific Date Range
```bash
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-03-01
```

**Note**: Historical data available from February 2024 onwards

## Step 4: Collect Current Data

```bash
python backend/collector.py
```

This will:
- ✅ Verify it's fetching SPY (S&P 500) options
- ✅ Download current options chain
- ✅ Calculate Greeks
- ✅ Store in Supabase

## Step 5: Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

## Verification

The system automatically verifies S&P 500 options on each run. You'll see:
```
✓ Confirmed: Fetching S&P 500 (SPY) options
```

## What Data Gets Downloaded

### Historical Data (Backfill):
- SPY option contracts
- Historical prices (OHLCV)
- From February 2024 onwards
- Daily or weekly bars

### Current Data (Collector):
- Current SPY options chain
- Real-time bid/ask prices
- Latest trade prices
- Calculated Greeks

## Troubleshooting

**"No option contracts found"**
- Check market hours (options data during trading hours)
- Verify Alpaca API credentials
- Ensure you have options data subscription

**"Not fetching SPY options"**
- Check `backend/config.py` - `SYMBOL` should be `'SPY'`
- It's already configured correctly!

**Historical data errors**
- Use dates >= 2024-02-01
- Market must have been open on that date

## Next Steps

1. ✅ Database setup (done)
2. ✅ Configure API keys (add secret key)
3. ✅ Backfill historical data
4. ✅ Run current data collector
5. ✅ Start frontend dashboard

Your system is ready to download and visualize S&P 500 options data!

