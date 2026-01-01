"""
Alpaca API client for fetching options data
"""
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import OptionContractsRequest, OptionSnapshotRequest, OptionBarsRequest
from alpaca.trading.client import TradingClient
from backend.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, SYMBOL
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from alpaca.data.timeframe import TimeFrame

logger = logging.getLogger(__name__)

class AlpacaOptionsClient:
    def __init__(self):
        """Initialize Alpaca clients"""
        self.data_client = StockHistoricalDataClient(
            api_key=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY
        )
        self.trading_client = TradingClient(
            api_key=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY,
            paper=True
        )
        self.symbol = SYMBOL
    
    def get_option_contracts(self, expiration_date: Optional[str] = None) -> List[Dict]:
        """
        Fetch option contracts for the symbol
        
        Args:
            expiration_date: Optional expiration date filter (YYYY-MM-DD)
        
        Returns:
            List of option contract dictionaries
        """
        try:
            request_params = OptionContractsRequest(
                underlying_symbol=self.symbol,
                expiration_date=expiration_date
            )
            
            contracts = self.data_client.get_option_contracts(request_params)
            
            contracts_list = []
            for contract in contracts:
                contracts_list.append({
                    'symbol': contract.symbol,
                    'underlying_symbol': contract.underlying_symbol,
                    'expiration_date': contract.expiration_date.isoformat() if contract.expiration_date else None,
                    'strike_price': float(contract.strike_price) if contract.strike_price else None,
                    'option_type': contract.option_type.value if contract.option_type else None,
                    'contract_type': contract.contract_type.value if contract.contract_type else None,
                })
            
            logger.info(f"Fetched {len(contracts_list)} option contracts")
            return contracts_list
            
        except Exception as e:
            logger.error(f"Error fetching option contracts: {str(e)}")
            return []
    
    def get_option_snapshot(self, contract_symbols: List[str]) -> Dict:
        """
        Get current snapshot data for option contracts
        
        Args:
            contract_symbols: List of option contract symbols
        
        Returns:
            Dictionary of option snapshots
        """
        try:
            request_params = OptionSnapshotRequest(underlying_symbol=self.symbol)
            snapshots = self.data_client.get_option_snapshot(request_params)
            
            snapshot_data = {}
            if snapshots:
                for symbol, snapshot in snapshots.items():
                    snapshot_data[symbol] = {}
                    
                    if hasattr(snapshot, 'latest_trade') and snapshot.latest_trade:
                        trade = snapshot.latest_trade
                        snapshot_data[symbol]['last_price'] = float(trade.price) if trade.price else None
                        snapshot_data[symbol]['timestamp'] = trade.timestamp.isoformat() if trade.timestamp else None
                    
                    if hasattr(snapshot, 'latest_quote') and snapshot.latest_quote:
                        quote = snapshot.latest_quote
                        snapshot_data[symbol]['bid_price'] = float(quote.bid_price) if quote.bid_price else None
                        snapshot_data[symbol]['ask_price'] = float(quote.ask_price) if quote.ask_price else None
            
            return snapshot_data
            
        except Exception as e:
            logger.error(f"Error fetching option snapshots: {str(e)}")
            return {}
    
    def get_underlying_price(self) -> Optional[float]:
        """Get current price of the underlying asset"""
        try:
            bars = self.data_client.get_latest_bar(self.symbol)
            if bars and hasattr(bars, 'close'):
                return float(bars.close)
            return None
        except Exception as e:
            logger.error(f"Error fetching underlying price: {str(e)}")
            return None
    
    def get_all_options_data(self) -> List[Dict]:
        """
        Fetch all available options data with current market data
        
        Returns:
            List of complete option data dictionaries
        """
        # Get all option contracts
        contracts = self.get_option_contracts()
        
        if not contracts:
            logger.warning("No option contracts found")
            return []
        
        # Get underlying price
        underlying_price = self.get_underlying_price()
        
        # Get contract symbols
        contract_symbols = [c['symbol'] for c in contracts]
        
        # Get snapshots for all contracts
        snapshots = self.get_option_snapshot(contract_symbols)
        
        # Combine contract data with snapshot data
        complete_data = []
        for contract in contracts:
            symbol = contract['symbol']
            snapshot = snapshots.get(symbol, {})
            
            # Calculate time to maturity
            time_to_maturity = None
            if contract['expiration_date']:
                exp_date = datetime.fromisoformat(contract['expiration_date'].split('T')[0])
                days_to_exp = (exp_date - datetime.now()).days
                time_to_maturity = days_to_exp / 365.0
            
            option_data = {
                'symbol': contract['underlying_symbol'],
                'option_symbol': symbol,
                'option_type': contract['option_type'],
                'strike_price': contract['strike_price'],
                'expiration_date': contract['expiration_date'],
                'bid_price': snapshot.get('bid_price'),
                'ask_price': snapshot.get('ask_price'),
                'last_price': snapshot.get('last_price'),
                'underlying_price': underlying_price,
                'time_to_maturity': time_to_maturity,
                'implied_volatility': None,  # Will be calculated or fetched if available
            }
            
            complete_data.append(option_data)
        
        logger.info(f"Collected data for {len(complete_data)} options")
        return complete_data
    
    def get_historical_option_bars(
        self,
        option_symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: TimeFrame = TimeFrame.Day
    ) -> List[Dict]:
        """
        Fetch historical option bars for a specific option contract
        
        Args:
            option_symbol: The option contract symbol (e.g., 'SPY240119C00450000')
            start_date: Start date for historical data
            end_date: End date for historical data
            timeframe: TimeFrame for bars (Day, Hour, Minute, etc.)
        
        Returns:
            List of historical bar data dictionaries
        """
        try:
            request_params = OptionBarsRequest(
                symbol_or_symbols=[option_symbol],
                start=start_date,
                end=end_date,
                timeframe=timeframe
            )
            
            bars = self.data_client.get_option_bars(request_params)
            
            historical_data = []
            if bars and option_symbol in bars:
                for bar in bars[option_symbol]:
                    historical_data.append({
                        'timestamp': bar.timestamp.isoformat() if bar.timestamp else None,
                        'open': float(bar.open) if bar.open else None,
                        'high': float(bar.high) if bar.high else None,
                        'low': float(bar.low) if bar.low else None,
                        'close': float(bar.close) if bar.close else None,
                        'volume': int(bar.volume) if bar.volume else None,
                        'trade_count': int(bar.trade_count) if hasattr(bar, 'trade_count') and bar.trade_count else None,
                        'vwap': float(bar.vwap) if hasattr(bar, 'vwap') and bar.vwap else None,
                    })
            
            logger.info(f"Fetched {len(historical_data)} historical bars for {option_symbol}")
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical bars for {option_symbol}: {str(e)}")
            return []
    
    def get_historical_options_for_date(
        self,
        target_date: datetime,
        expiration_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get historical options data for a specific date
        
        Args:
            target_date: The date to fetch historical data for
            expiration_date: Optional expiration date filter
        
        Returns:
            List of option data dictionaries with historical prices
        """
        try:
            # Get option contracts available on that date
            contracts = self.get_option_contracts(expiration_date=expiration_date)
            
            if not contracts:
                logger.warning(f"No option contracts found for date {target_date}")
                return []
            
            # Get historical bars for each contract
            historical_data = []
            for contract in contracts[:50]:  # Limit to first 50 to avoid rate limits
                option_symbol = contract['symbol']
                
                # Fetch historical bars for the target date
                bars = self.get_historical_option_bars(
                    option_symbol=option_symbol,
                    start_date=target_date,
                    end_date=target_date + timedelta(days=1),
                    timeframe=TimeFrame.Day
                )
                
                if bars and len(bars) > 0:
                    bar = bars[0]  # Get the bar for the target date
                    
                    # Calculate time to maturity
                    time_to_maturity = None
                    if contract['expiration_date']:
                        exp_date = datetime.fromisoformat(contract['expiration_date'].split('T')[0])
                        days_to_exp = (exp_date - target_date).days
                        time_to_maturity = days_to_exp / 365.0
                    
                    option_data = {
                        'symbol': contract['underlying_symbol'],
                        'option_symbol': option_symbol,
                        'option_type': contract['option_type'],
                        'strike_price': contract['strike_price'],
                        'expiration_date': contract['expiration_date'],
                        'bid_price': None,  # Historical bars don't have bid/ask
                        'ask_price': None,
                        'last_price': bar.get('close'),
                        'open_price': bar.get('open'),
                        'high_price': bar.get('high'),
                        'low_price': bar.get('low'),
                        'volume': bar.get('volume'),
                        'underlying_price': None,  # Would need to fetch separately
                        'time_to_maturity': time_to_maturity,
                        'timestamp': bar.get('timestamp'),
                        'implied_volatility': None,
                    }
                    
                    historical_data.append(option_data)
            
            logger.info(f"Collected historical data for {len(historical_data)} options on {target_date.date()}")
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical options data: {str(e)}")
            return []
    
    def verify_sp500_options(self) -> bool:
        """
        Verify that we're fetching S&P 500 options (SPY)
        
        Returns:
            True if symbol is SPY, False otherwise
        """
        if self.symbol.upper() == 'SPY':
            logger.info("✓ Confirmed: Fetching S&P 500 (SPY) options")
            return True
        else:
            logger.warning(f"⚠ Current symbol is {self.symbol}, not SPY (S&P 500)")
            return False

