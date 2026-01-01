"""
Main data collector script that fetches options data from Alpaca
and stores it in Supabase continuously
"""
import logging
import schedule
import time
from datetime import datetime
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

class OptionsDataCollector:
    def __init__(self):
        self.alpaca_client = AlpacaOptionsClient()
        self.supabase = get_supabase_client()
        self.greeks_calc = GreeksCalculator()
        self.risk_free_rate = 0.05  # 5% risk-free rate (can be updated from Treasury rates)
    
    def collect_and_store_data(self):
        """Main function to collect options data and store in Supabase"""
        try:
            logger.info(f"Starting data collection for {SYMBOL}")
            
            # Fetch options data from Alpaca
            options_data = self.alpaca_client.get_all_options_data()
            
            if not options_data:
                logger.warning("No options data retrieved")
                return
            
            # Process and store each option
            stored_count = 0
            for option in options_data:
                try:
                    # Prepare options_data record
                    option_record = {
                        'symbol': option['symbol'],
                        'option_type': option['option_type'],
                        'strike_price': float(option['strike_price']) if option['strike_price'] else None,
                        'expiration_date': option['expiration_date'],
                        'bid_price': float(option['bid_price']) if option['bid_price'] else None,
                        'ask_price': float(option['ask_price']) if option['ask_price'] else None,
                        'last_price': float(option['last_price']) if option['last_price'] else None,
                        'underlying_price': float(option['underlying_price']) if option['underlying_price'] else None,
                        'time_to_maturity': float(option['time_to_maturity']) if option['time_to_maturity'] else None,
                        'implied_volatility': option.get('implied_volatility'),
                    }
                    
                    # Use mid price for calculations if available
                    mid_price = None
                    if option['bid_price'] and option['ask_price']:
                        mid_price = (option['bid_price'] + option['ask_price']) / 2
                    elif option['last_price']:
                        mid_price = option['last_price']
                    
                    # Calculate Greeks if we have necessary data
                    if (option['underlying_price'] and option['strike_price'] and 
                        option['time_to_maturity'] and mid_price):
                        
                        greeks = self.greeks_calc.calculate_greeks_for_option(
                            S=option['underlying_price'],
                            K=option['strike_price'],
                            T=option['time_to_maturity'],
                            r=self.risk_free_rate,
                            market_price=mid_price,
                            option_type=option['option_type']
                        )
                        
                        # Update implied volatility if calculated
                        if greeks['implied_volatility']:
                            option_record['implied_volatility'] = greeks['implied_volatility']
                    
                    # Insert into options_data table
                    result = self.supabase.table('options_data').insert(option_record).execute()
                    
                    if result.data:
                        option_id = result.data[0]['id']
                        stored_count += 1
                        
                        # Store Greeks if calculated
                        if (option['underlying_price'] and option['strike_price'] and 
                            option['time_to_maturity'] and mid_price):
                            
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
                            }
                            
                            self.supabase.table('greeks_data').insert(greeks_record).execute()
                        
                        # Store IV evolution data
                        if option_record['implied_volatility']:
                            iv_record = {
                                'symbol': option['symbol'],
                                'strike_price': float(option['strike_price']),
                                'expiration_date': option['expiration_date'],
                                'option_type': option['option_type'],
                                'implied_volatility': float(option_record['implied_volatility']),
                                'time_to_maturity': float(option['time_to_maturity']) if option['time_to_maturity'] else None,
                            }
                            
                            self.supabase.table('iv_evolution').insert(iv_record).execute()
                
                except Exception as e:
                    logger.error(f"Error processing option {option.get('option_symbol', 'unknown')}: {str(e)}")
                    logger.debug(traceback.format_exc())
                    continue
            
            logger.info(f"Successfully stored {stored_count} options records")
            
        except Exception as e:
            logger.error(f"Error in data collection: {str(e)}")
            logger.debug(traceback.format_exc())
    
    def run_continuous(self, interval_minutes: int = 15):
        """Run data collection continuously at specified intervals"""
        logger.info(f"Starting continuous data collection (every {interval_minutes} minutes)")
        
        # Run immediately
        self.collect_and_store_data()
        
        # Schedule periodic collection
        schedule.every(interval_minutes).minutes.do(self.collect_and_store_data)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    collector = OptionsDataCollector()
    
    # Run once for testing, or uncomment the line below for continuous collection
    collector.collect_and_store_data()
    
    # Uncomment to run continuously (every 15 minutes)
    # collector.run_continuous(interval_minutes=15)

