# How to Fix 404 NOT_FOUND Error

## The Problem

You're seeing this error:
```
404: NOT_FOUND
Code: NOT_FOUND
ID: iad1::ccg4h-1767282921238-8bcf99a66e9c
```

This means **the Supabase database tables don't exist yet**.

## The Solution (2 Minutes)

### Step 1: Open Supabase Dashboard
1. Go to: https://supabase.com/dashboard
2. Select your project: `bbxcukvhekihomnevirr`

### Step 2: Run the SQL Schema
1. Click **"SQL Editor"** in the left sidebar
2. Click **"New query"** button
3. Open the file `supabase_schema.sql` from this project
4. **Copy ALL the SQL code** (lines 1-74)
5. **Paste it** into the SQL Editor
6. Click **"Run"** button (or press Cmd+Enter / Ctrl+Enter)

### Step 3: Verify Tables Created
1. Click **"Table Editor"** in the left sidebar
2. You should see 3 tables:
   - ✅ `options_data`
   - ✅ `greeks_data`
   - ✅ `iv_evolution`

### Step 4: Refresh Your App
- Refresh your browser
- The 404 error should be gone!

## Quick Copy-Paste SQL

If you want to copy the SQL directly, here's what to run:

```sql
-- Copy everything from supabase_schema.sql
-- Or run this in Supabase SQL Editor:

CREATE TABLE IF NOT EXISTS options_data (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    option_type VARCHAR(4) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    bid_price DECIMAL(10, 4),
    ask_price DECIMAL(10, 4),
    last_price DECIMAL(10, 4),
    volume INTEGER,
    open_interest INTEGER,
    implied_volatility DECIMAL(8, 6),
    underlying_price DECIMAL(10, 2),
    time_to_maturity DECIMAL(10, 6),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS greeks_data (
    id BIGSERIAL PRIMARY KEY,
    option_id BIGINT REFERENCES options_data(id),
    symbol VARCHAR(10) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    option_type VARCHAR(4) NOT NULL,
    delta DECIMAL(10, 6),
    gamma DECIMAL(10, 6),
    theta DECIMAL(10, 6),
    vega DECIMAL(10, 6),
    rho DECIMAL(10, 6),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS iv_evolution (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    option_type VARCHAR(4) NOT NULL,
    implied_volatility DECIMAL(8, 6),
    time_to_maturity DECIMAL(10, 6),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_options_symbol_exp ON options_data(symbol, expiration_date);
CREATE INDEX IF NOT EXISTS idx_options_created_at ON options_data(created_at);
CREATE INDEX IF NOT EXISTS idx_greeks_option_id ON greeks_data(option_id);
CREATE INDEX IF NOT EXISTS idx_greeks_symbol_exp ON greeks_data(symbol, expiration_date);
CREATE INDEX IF NOT EXISTS idx_iv_evolution_symbol_exp ON iv_evolution(symbol, expiration_date, strike_price);
CREATE INDEX IF NOT EXISTS idx_iv_evolution_recorded_at ON iv_evolution(recorded_at);

-- Row Level Security
ALTER TABLE options_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE greeks_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE iv_evolution ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Allow public read access" ON options_data FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON greeks_data FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON iv_evolution FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON options_data FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert" ON greeks_data FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert" ON iv_evolution FOR INSERT WITH CHECK (true);
```

## After Fixing

Once you've created the tables:
1. ✅ The 404 error will disappear
2. ✅ You can run the data collector: `python backend/collector.py`
3. ✅ The dashboard will work properly

## Still Getting Errors?

1. **Check Supabase URL**: Should be `https://bbxcukvhekihomnevirr.supabase.co`
2. **Check API Key**: Should be in `frontend/.env.local`
3. **Check Browser Console**: Look for more specific error messages
4. **Verify Tables**: Go to Table Editor and confirm all 3 tables exist

That's it! The 404 error should be fixed after creating the tables.

