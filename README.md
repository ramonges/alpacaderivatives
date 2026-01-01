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

4. Run the data collector (one-time):
```bash
python backend/collector.py
```

5. For continuous data collection (every 15 minutes), modify `backend/collector.py` and uncomment:
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

## Continuous Data Collection

The backend collector can run continuously to keep your database updated. You can:

1. Run it as a background process
2. Set up a cron job
3. Deploy it as a scheduled cloud function

## Troubleshooting

- **No data showing**: Make sure the data collector has run at least once and populated the database
- **API errors**: Verify your Alpaca API credentials and that you have options data access
- **Database connection issues**: Check your Supabase URL and anon key in the configuration files

