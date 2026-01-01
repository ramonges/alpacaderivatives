#!/usr/bin/env python3
"""
Runner script for historical backfill
"""
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from backend.historical_backfill import HistoricalBackfill
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Run historical backfill for last 30 days"""
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Ensure start date is not before Feb 2024 (Alpaca's limit)
    if start_date < datetime(2024, 2, 1):
        print("⚠️  Alpaca historical options data is only available from February 2024 onwards")
        print(f"   Adjusting start date from {start_date.date()} to 2024-02-01")
        start_date = datetime(2024, 2, 1)
    
    print("=" * 60)
    print("S&P 500 Options Historical Data Backfill")
    print("=" * 60)
    print(f"Symbol: SPY (S&P 500 ETF)")
    print(f"Start Date: {start_date.date()}")
    print(f"End Date: {end_date.date()}")
    print(f"Days to process: {(end_date - start_date).days}")
    print("=" * 60)
    print()
    
    try:
        backfill = HistoricalBackfill()
        backfill.backfill_date_range(start_date, end_date, days_step=1)
        print()
        print("✅ Backfill complete!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

