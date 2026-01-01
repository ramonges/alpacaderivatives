# Alpaca Options Derivatives Dashboard

A real-time dashboard for visualizing S&P 500 options data including:
- **Smile Curve**: Implied Volatility vs Strike Price
- **Greeks**: Delta, Gamma, Theta, Vega, Rho visualization
- **IV Evolution**: Implied Volatility evolution over Time to Maturity

## Prerequisites

- Python 3.8+
- Node.js 18+
- Alpaca API account with options data access
- Supabase account

## Setup Instructions

### 1. Supabase Database Setup

1. Go to your Supabase project dashboard: https://bbxcukvhekihomnevirr.supabase.co
2. Navigate to the SQL Editor
3. Copy and run the SQL from `supabase_schema.sql` to create the necessary tables

Alternatively, you can create the tables manually using the Supabase Table Editor with the schema defined in `supabase_schema.sql`.

### 2. Backend Setup (Python)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Alpaca API secret key:
```
ALPACA_API_KEY=sacZc0e60Tffp4vbJcgvG62FpV0rrDXbGFEupQbn
ALPACA_SECRET_KEY=your_secret_key_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

4. **Verify S&P 500 Options Collection**:
   - The system is configured to fetch SPY (S&P 500 ETF) options
   - The collector will verify this on each run

5. **Collect Current Options Data** (one-time):
```bash
python backend/collector.py
```

6. **Backfill Historical S&P 500 Options Data**:
   - Alpaca provides historical options data from February 2024 onwards
   - To backfill historical data:
```bash
# Backfill last 30 days (default)
python backend/historical_backfill.py

# Backfill specific date range
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-03-01

# Backfill weekly data (faster, less granular)
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-03-01 --step 7
```

7. **For Continuous Data Collection** (every 15 minutes), modify `backend/collector.py` and uncomment:
```python
collector.run_continuous(interval_minutes=15)
```

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. The Supabase credentials are already configured in `.env.local`. If needed, verify:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

4. Run the development server:
```bash
npm run dev
```

5. Open your browser to `http://localhost:3000`

## Database Schema

The Supabase database uses three main tables:

- **`options_data`**: Stores raw options chain data from Alpaca
  - Symbol, strike price, expiration date, bid/ask prices
  - Implied volatility, underlying price, time to maturity

- **`greeks_data`**: Stores calculated option Greeks
  - Delta, Gamma, Theta, Vega, Rho
  - Linked to options_data via option_id

- **`iv_evolution`**: Tracks IV changes over time
  - Historical implied volatility data
  - Time series for analyzing IV evolution

## Features

### Smile Curve
Visualizes the volatility smile by plotting implied volatility against strike prices for both calls and puts. This helps identify market sentiment and potential arbitrage opportunities.

### Greeks Dashboard
Interactive visualization of option Greeks:
- **Delta**: Price sensitivity to underlying asset changes
- **Gamma**: Rate of change of delta
- **Theta**: Time decay
- **Vega**: Volatility sensitivity
- **Rho**: Interest rate sensitivity

### IV Evolution
Tracks how implied volatility changes as options approach expiration, helping identify volatility patterns and trading opportunities.

## Historical Data Collection

### Backfilling Historical S&P 500 Options Data

The system includes a historical backfill script to download past options data:

**Important Notes:**
- Alpaca historical options data is available from **February 2024 onwards**
- Historical data helps build the IV Evolution chart over time
- The backfill script automatically skips duplicate records

**Usage Examples:**
```bash
# Backfill last 30 days (default)
python backend/historical_backfill.py

# Backfill specific date range
python backend/historical_backfill.py --start-date 2024-02-15 --end-date 2024-03-15

# Weekly backfill (faster, less data points)
python backend/historical_backfill.py --start-date 2024-02-01 --end-date 2024-12-31 --step 7
```

**What Gets Stored:**
- Historical option prices (open, high, low, close)
- Volume data
- Calculated Greeks for each historical point
- IV evolution tracking over time

## Continuous Data Collection

The backend collector can run continuously to keep your database updated. You can:

1. Run it as a background process
2. Set up a cron job
3. Deploy it as a scheduled cloud function

**Note:** The collector automatically verifies it's fetching S&P 500 (SPY) options on each run.

## Troubleshooting

- **No data showing**: Make sure the data collector has run at least once and populated the database
- **API errors**: Verify your Alpaca API credentials and that you have options data access
- **Database connection issues**: Check your Supabase URL and anon key in the configuration files

