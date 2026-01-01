"""
Alpaca API client for fetching options data
"""
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import OptionContractsRequest, OptionSnapshotRequest
from alpaca.trading.client import TradingClient
from backend.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, SYMBOL
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

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

