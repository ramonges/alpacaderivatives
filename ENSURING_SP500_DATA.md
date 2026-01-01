# Ensuring S&P 500 Options Data Collection

## How the System Ensures S&P 500 Options Data

### 1. Symbol Configuration
The system is configured to fetch **SPY** (S&P 500 ETF) options by default:

**File**: `backend/config.py`
```python
SYMBOL = 'SPY'  # S&P 500 ETF
```

### 2. Automatic Verification
The collector automatically verifies it's fetching SPY options on each run:

**File**: `backend/alpaca_client.py`
- `verify_sp500_options()` method checks the symbol
- Logs confirmation or warning if not SPY

**File**: `backend/collector.py`
- Calls verification before data collection
- Ensures you're getting S&P 500 options, not other symbols

### 3. Historical Data Collection

#### Current Data (Real-time)
```bash
python backend/collector.py
```
- Fetches current SPY options chain
- Gets latest prices and market data
- Verifies SPY symbol before fetching

#### Historical Data (Backfill)
```bash
# Backfill last 30 days
python backend/historical_backfill.py

# Backfill specific range
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-03-01
```

The historical backfill:
- ✅ Verifies SPY symbol before starting
- ✅ Fetches historical option bars for SPY contracts
- ✅ Stores data with timestamps for IV evolution tracking
- ✅ Skips duplicates to avoid re-downloading

### 4. What Gets Downloaded

#### Current Data Collection:
- All available SPY option contracts
- Current bid/ask prices
- Latest trade prices
- Underlying SPY price
- Calculated Greeks

#### Historical Data Collection:
- Historical option bars (OHLCV) for SPY options
- Daily data from February 2024 onwards
- Volume and trade count
- Time-stamped for IV evolution analysis

### 5. Verification Steps

**Check Configuration:**
```python
# In backend/config.py
SYMBOL = 'SPY'  # Must be 'SPY' for S&P 500
```

**Run Test:**
```bash
python test_setup.py
```
This will verify:
- ✓ Supabase connection
- ✓ Alpaca connection
- ✓ Options fetch (should show SPY contracts)

**Check Logs:**
When running the collector, you should see:
```
✓ Confirmed: Fetching S&P 500 (SPY) options
Fetched X option contracts
```

### 6. Database Storage

All data is stored with the symbol field:
- `symbol`: 'SPY' (S&P 500 ETF)
- `option_type`: 'call' or 'put'
- `strike_price`: Strike price of the option
- `expiration_date`: Option expiration date
- `timestamp`: When the data was recorded

### 7. Frontend Display

The dashboard automatically:
- Filters data by symbol (SPY)
- Groups by expiration date
- Shows S&P 500 options analytics

## Troubleshooting

**Not seeing SPY options?**
1. Check `backend/config.py` - `SYMBOL` should be `'SPY'`
2. Verify your Alpaca account has options data access
3. Check market hours (options data available during trading hours)

**Historical data not available?**
- Alpaca historical options data starts from February 2024
- Use dates on or after 2024-02-01
- Market must have been open on that date

**Wrong symbol in database?**
- Check the `symbol` column in `options_data` table
- Should all be 'SPY' for S&P 500 options
- If not, verify your configuration and re-run collector

## Summary

✅ **Symbol is hardcoded to 'SPY'** in config
✅ **Automatic verification** on each data collection run
✅ **Historical backfill** specifically targets SPY options
✅ **Database stores** all data with SPY symbol
✅ **Frontend displays** only SPY options data

The system is designed to ensure you're always downloading S&P 500 (SPY) options data, both current and historical.

