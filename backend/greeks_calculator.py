"""
Calculate option Greeks using Black-Scholes model
"""
import numpy as np
from scipy.stats import norm
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GreeksCalculator:
    @staticmethod
    def black_scholes(
        S: float,  # Spot price
        K: float,  # Strike price
        T: float,  # Time to maturity (years)
        r: float,  # Risk-free rate
        sigma: float,  # Volatility
        option_type: str = 'call'  # 'call' or 'put'
    ) -> Dict[str, float]:
        """
        Calculate Black-Scholes option price and Greeks
        
        Returns:
            Dictionary with price, delta, gamma, theta, vega, rho
        """
        if T <= 0:
            # Option expired
            if option_type == 'call':
                price = max(S - K, 0)
            else:
                price = max(K - S, 0)
            return {
                'price': price,
                'delta': 1.0 if (option_type == 'call' and S > K) or (option_type == 'put' and S < K) else 0.0,
                'gamma': 0.0,
                'theta': 0.0,
                'vega': 0.0,
                'rho': 0.0
            }
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            delta = norm.cdf(d1)
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                    - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = -norm.cdf(-d1)
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                    + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        
        return {
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    @staticmethod
    def calculate_implied_volatility(
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: str = 'call',
        max_iterations: int = 100,
        tolerance: float = 0.0001
    ) -> Optional[float]:
        """
        Calculate implied volatility using Newton-Raphson method
        
        Returns:
            Implied volatility or None if calculation fails
        """
        if T <= 0 or market_price <= 0:
            return None
        
        # Initial guess
        sigma = 0.2
        
        for _ in range(max_iterations):
            greeks = GreeksCalculator.black_scholes(S, K, T, r, sigma, option_type)
            price = greeks['price']
            vega = greeks['vega']
            
            if abs(price - market_price) < tolerance:
                return sigma
            
            if vega < 1e-10:  # Avoid division by zero
                break
            
            sigma = sigma - (price - market_price) / (vega * 100)  # vega is per 1% change
            
            if sigma < 0:
                sigma = 0.01
            if sigma > 5:
                sigma = 5
        
        return None
    
    @staticmethod
    def calculate_greeks_for_option(
        S: float,
        K: float,
        T: float,
        r: float = 0.05,  # Default risk-free rate (5%)
        sigma: Optional[float] = None,
        market_price: Optional[float] = None,
        option_type: str = 'call'
    ) -> Dict[str, Optional[float]]:
        """
        Calculate Greeks for an option
        
        If sigma is not provided, it will be calculated from market_price if available
        """
        if sigma is None and market_price is not None:
            sigma = GreeksCalculator.calculate_implied_volatility(
                market_price, S, K, T, r, option_type
            )
        
        if sigma is None:
            # Use a default volatility if we can't calculate it
            sigma = 0.2
        
        greeks = GreeksCalculator.black_scholes(S, K, T, r, sigma, option_type)
        
        return {
            'implied_volatility': sigma,
            'delta': greeks['delta'],
            'gamma': greeks['gamma'],
            'theta': greeks['theta'],
            'vega': greeks['vega'],
            'rho': greeks['rho']
        }

