"""
Script to backfill historical S&P 500 options data from Alpaca
"""
import logging
import sys
from datetime import datetime, timedelta
from backend.config import SYMBOL
from backend.alpaca_client import AlpacaOptionsClient
from backend.database import get_supabase_client
from backend.greeks_calculator import GreeksCalculator
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HistoricalBackfill:
    def __init__(self):
        self.alpaca_client = AlpacaOptionsClient()
        self.supabase = get_supabase_client()
        self.greeks_calc = GreeksCalculator()
        self.risk_free_rate = 0.05
        
        # Verify we're getting S&P 500 options
        if not self.alpaca_client.verify_sp500_options():
            logger.warning("Not fetching SPY options. Check your SYMBOL configuration.")
    
    def backfill_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        days_step: int = 1
    ):
        """
        Backfill historical options data for a date range
        
        Args:
            start_date: Start date for backfill
            end_date: End date for backfill
            days_step: Number of days to step (1 = daily, 7 = weekly)
        """
        logger.info(f"Starting historical backfill from {start_date.date()} to {end_date.date()}")
        
        current_date = start_date
        total_stored = 0
        
        while current_date <= end_date:
            try:
                logger.info(f"Processing date: {current_date.date()}")
                
                # Fetch historical options data for this date
                options_data = self.alpaca_client.get_historical_options_for_date(current_date)
                
                if not options_data:
                    logger.warning(f"No data found for {current_date.date()}")
                    current_date += timedelta(days=days_step)
                    continue
                
                # Store each option
                stored_count = 0
                for option in options_data:
                    try:
                        # Check if record already exists
                        existing = self.supabase.table('options_data')\
                            .select('id')\
                            .eq('symbol', option['symbol'])\
                            .eq('strike_price', option['strike_price'])\
                            .eq('expiration_date', option['expiration_date'])\
                            .eq('option_type', option['option_type'])\
                            .gte('created_at', current_date.isoformat())\
                            .lt('created_at', (current_date + timedelta(days=1)).isoformat())\
                            .limit(1)\
                            .execute()
                        
                        if existing.data and len(existing.data) > 0:
                            logger.debug(f"Skipping duplicate: {option['option_symbol']}")
                            continue
                        
                        # Prepare record
                        option_record = {
                            'symbol': option['symbol'],
                            'option_type': option['option_type'],
                            'strike_price': float(option['strike_price']) if option['strike_price'] else None,
                            'expiration_date': option['expiration_date'],
                            'bid_price': float(option['bid_price']) if option.get('bid_price') else None,
                            'ask_price': float(option['ask_price']) if option.get('ask_price') else None,
                            'last_price': float(option['last_price']) if option.get('last_price') else None,
                            'underlying_price': float(option['underlying_price']) if option.get('underlying_price') else None,
                            'time_to_maturity': float(option['time_to_maturity']) if option.get('time_to_maturity') else None,
                            'implied_volatility': option.get('implied_volatility'),
                            'created_at': option.get('timestamp', current_date.isoformat()),
                        }
                        
                        # Insert into database
                        result = self.supabase.table('options_data').insert(option_record).execute()
                        
                        if result.data:
                            option_id = result.data[0]['id']
                            stored_count += 1
                            
                            # Calculate and store Greeks if we have necessary data
                            if (option.get('underlying_price') and option.get('strike_price') and 
                                option.get('time_to_maturity') and option.get('last_price')):
                                
                                greeks = self.greeks_calc.calculate_greeks_for_option(
                                    S=option['underlying_price'],
                                    K=option['strike_price'],
                                    T=option['time_to_maturity'],
                                    r=self.risk_free_rate,
                                    market_price=option['last_price'],
                                    option_type=option['option_type']
                                )
                                
                                if greeks['implied_volatility']:
                                    option_record['implied_volatility'] = greeks['implied_volatility']
                                
                                greeks_record = {
                                    'option_id': option_id,
                                    'symbol': option['symbol'],
                                    'strike_price': float(option['strike_price']),
                                    'expiration_date': option['expiration_date'],
                                    'option_type': option['option_type'],
                                    'delta': greeks['delta'],
                                    'gamma': greeks['gamma'],
                                    'theta': greeks['theta'],
                                    'vega': greeks['vega'],
                                    'rho': greeks['rho'],
                                    'created_at': option.get('timestamp', current_date.isoformat()),
                                }
                                
                                self.supabase.table('greeks_data').insert(greeks_record).execute()
                                
                                # Store IV evolution
                                if greeks['implied_volatility']:
                                    iv_record = {
                                        'symbol': option['symbol'],
                                        'strike_price': float(option['strike_price']),
                                        'expiration_date': option['expiration_date'],
                                        'option_type': option['option_type'],
                                        'implied_volatility': float(greeks['implied_volatility']),
                                        'time_to_maturity': float(option['time_to_maturity']),
                                        'recorded_at': option.get('timestamp', current_date.isoformat()),
                                    }
                                    
                                    self.supabase.table('iv_evolution').insert(iv_record).execute()
                    
                    except Exception as e:
                        logger.error(f"Error processing option {option.get('option_symbol', 'unknown')}: {str(e)}")
                        logger.debug(traceback.format_exc())
                        continue
                
                total_stored += stored_count
                logger.info(f"Stored {stored_count} options for {current_date.date()}")
                
                # Move to next date
                current_date += timedelta(days=days_step)
                
                # Rate limiting - wait a bit between requests
                import time
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing date {current_date.date()}: {str(e)}")
                logger.debug(traceback.format_exc())
                current_date += timedelta(days=days_step)
                continue
        
        logger.info(f"Backfill complete! Total records stored: {total_stored}")

def main():
    """Main function to run historical backfill"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backfill historical S&P 500 options data')
    parser.add_argument(
        '--start-date',
        type=str,
        default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        help='Start date (YYYY-MM-DD). Default: 30 days ago'
    )
    parser.add_argument(
        '--end-date',
        type=str,
        default=datetime.now().strftime('%Y-%m-%d'),
        help='End date (YYYY-MM-DD). Default: today'
    )
    parser.add_argument(
        '--step',
        type=int,
        default=1,
        help='Days to step (1=daily, 7=weekly). Default: 1'
    )
    
    args = parser.parse_args()
    
    try:
        start_date = datetime.fromisoformat(args.start_date)
        end_date = datetime.fromisoformat(args.end_date)
    except ValueError as e:
        logger.error(f"Invalid date format: {str(e)}")
        logger.info("Use YYYY-MM-DD format (e.g., 2024-01-15)")
        sys.exit(1)
    
    if start_date > end_date:
        logger.error("Start date must be before end date")
        sys.exit(1)
    
    # Note: Alpaca historical options data is available from February 2024
    if start_date < datetime(2024, 2, 1):
        logger.warning("Alpaca historical options data is only available from February 2024 onwards")
        logger.info("Adjusting start date to 2024-02-01")
        start_date = max(start_date, datetime(2024, 2, 1))
    
    backfill = HistoricalBackfill()
    backfill.backfill_date_range(start_date, end_date, days_step=args.step)

if __name__ == "__main__":
    main()

