#!/usr/bin/env python3
"""
Portfolio analysis example
"""

import asyncio
from client import FinanceMCPClient

async def analyze_portfolio():
    """Analyze a sample portfolio"""
    client = FinanceMCPClient()
    
    try:
        if not await client.connect():
            print("Failed to connect")
            return
        
        # Define portfolio
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Must sum to 1.0
        
        print(f"Analyzing portfolio: {dict(zip(symbols, weights))}")
        
        # Get portfolio analysis
        response = await client.get_portfolio_analysis(symbols, weights, "1y")
        
        if response.success and "error" not in response.data:
            data = response.data
            portfolio_metrics = data["portfolio_metrics"]
            
            print("\nPortfolio Metrics:")
            print(f"  Annual Return: {portfolio_metrics.get('annual_return')}%")
            print(f"  Volatility: {portfolio_metrics.get('volatility')}%")
            print(f"  Sharpe Ratio: {portfolio_metrics.get('sharpe_ratio')}")
            print(f"  Max Drawdown: {portfolio_metrics.get('max_drawdown')}%")
            
            print("\nIndividual Holdings:")
            for symbol in symbols:
                metrics = data["individual_metrics"].get(symbol, {})
                print(f"  {symbol}: {metrics.get('weight')}% weight, "
                      f"{metrics.get('volatility')}% vol, "
                      f"Sharpe: {metrics.get('sharpe_ratio')}")
        else:
            print("Error analyzing portfolio")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(analyze_portfolio())

