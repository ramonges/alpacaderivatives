"""
Database setup and utilities for Supabase
"""
from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY
import logging

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    """
    Create necessary tables in Supabase.
    Note: This is a reference. You should create these tables manually in Supabase dashboard
    or use SQL migrations.
    """
    supabase = get_supabase_client()
    
    # SQL to create tables (run this in Supabase SQL editor)
    sql_statements = """
    -- Options data table
    CREATE TABLE IF NOT EXISTS options_data (
        id BIGSERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL,
        option_type VARCHAR(4) NOT NULL, -- 'call' or 'put'
        strike_price DECIMAL(10, 2) NOT NULL,
        expiration_date DATE NOT NULL,
        bid_price DECIMAL(10, 4),
        ask_price DECIMAL(10, 4),
        last_price DECIMAL(10, 4),
        volume INTEGER,
        open_interest INTEGER,
        implied_volatility DECIMAL(8, 6),
        underlying_price DECIMAL(10, 2),
        time_to_maturity DECIMAL(10, 6), -- in years
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Greeks data table
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

    -- IV evolution table
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

    -- Create indexes for better query performance
    CREATE INDEX IF NOT EXISTS idx_options_symbol_exp ON options_data(symbol, expiration_date);
    CREATE INDEX IF NOT EXISTS idx_options_created_at ON options_data(created_at);
    CREATE INDEX IF NOT EXISTS idx_greeks_option_id ON greeks_data(option_id);
    CREATE INDEX IF NOT EXISTS idx_iv_evolution_symbol_exp ON iv_evolution(symbol, expiration_date, strike_price);
    """
    
    logger.info("Please run the following SQL in your Supabase SQL editor:")
    logger.info(sql_statements)
    return sql_statements

if __name__ == "__main__":
    create_tables()

