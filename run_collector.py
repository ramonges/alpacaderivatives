#!/usr/bin/env python3
"""
Simple runner script for data collector
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from backend.collector import OptionsDataCollector
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("S&P 500 Options Data Collector")
    print("=" * 60)
    print("Fetching current SPY options data...")
    print()
    
    collector = OptionsDataCollector()
    collector.collect_and_store_data()
    
    print()
    print("✅ Data collection complete!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease install dependencies:")
    print("  pip install alpaca-py supabase python-dotenv pandas numpy scipy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

