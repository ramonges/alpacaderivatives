# Historical S&P 500 Options Data Guide

## Overview

This guide explains how to download and store historical S&P 500 (SPY) options data from Alpaca.

## Data Availability

- **Start Date**: February 2024 (Alpaca's historical options data begins here)
- **Data Type**: Daily option bars (open, high, low, close, volume)
- **Coverage**: All available SPY option contracts

## Quick Start

### 1. Backfill Recent Data (Last 30 Days)
```bash
python backend/historical_backfill.py
```

### 2. Backfill Specific Date Range
```bash
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-03-01
```

### 3. Weekly Backfill (Faster, Less Granular)
```bash
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-12-31 --step 7
```

## Command Line Options

```
--start-date YYYY-MM-DD    Start date for backfill (default: 30 days ago)
--end-date YYYY-MM-DD      End date for backfill (default: today)
--step N                   Days to step between dates (1=daily, 7=weekly, default: 1)
```

## What Gets Stored

For each historical date, the script stores:

1. **Options Data** (`options_data` table):
   - Strike price, expiration date, option type
   - Historical prices (open, high, low, close)
   - Volume
   - Time to maturity

2. **Greeks** (`greeks_data` table):
   - Delta, Gamma, Theta, Vega, Rho
   - Calculated using Black-Scholes model

3. **IV Evolution** (`iv_evolution` table):
   - Implied volatility over time
   - Time to maturity tracking

## Verification

The script automatically:
- ✅ Verifies it's fetching SPY (S&P 500) options
- ✅ Skips duplicate records (won't re-download existing data)
- ✅ Handles rate limiting with delays between requests
- ✅ Logs progress and errors

## Example Output

```
2024-01-15 10:00:00 - INFO - ✓ Confirmed: Fetching S&P 500 (SPY) options
2024-01-15 10:00:01 - INFO - Starting historical backfill from 2024-02-01 to 2024-03-01
2024-01-15 10:00:02 - INFO - Processing date: 2024-02-01
2024-01-15 10:00:05 - INFO - Fetched 150 option contracts
2024-01-15 10:00:10 - INFO - Stored 150 options for 2024-02-01
...
2024-01-15 10:15:00 - INFO - Backfill complete! Total records stored: 4500
```

## Tips

1. **Start Small**: Begin with a short date range to test
2. **Use Weekly Step**: For large date ranges, use `--step 7` to speed up
3. **Check Logs**: Monitor the output for any errors or warnings
4. **Rate Limits**: The script includes delays to respect Alpaca's rate limits

## Troubleshooting

**"No data found for date"**
- Market may have been closed (weekends, holidays)
- Options may not have been available on that date
- Check if date is before February 2024

**"Rate limit exceeded"**
- The script includes delays, but you may need to increase them
- Try using `--step 7` for weekly data instead of daily

**"Not fetching SPY options"**
- Check your `SYMBOL` configuration in `backend/config.py`
- Should be set to `'SPY'` for S&P 500 options

