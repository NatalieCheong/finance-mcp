#!/usr/bin/env python3
"""
Standalone Finance Application
Direct financial analysis without MCP client complexity
"""

import asyncio
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any

class FinanceAnalyzer:
    """Direct finance analyzer without MCP complexity"""
    
    def validate_symbol(self, symbol: str) -> str:
        """Validate and sanitize stock symbol"""
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")
        return symbol.upper().strip()
    
    def calculate_returns(self, prices: pd.Series) -> pd.Series:
        """Calculate daily returns"""
        return prices.pct_change().dropna()
    
    def calculate_volatility(self, returns: pd.Series, annualize: bool = True) -> float:
        """Calculate volatility (standard deviation of returns)"""
        vol = returns.std()
        if annualize:
            vol *= np.sqrt(252)  # Annualize assuming 252 trading days
        return vol
    
    async def get_stock_price(self, symbol: str, period: str = "1mo") -> Dict[str, Any]:
        """Get current and historical stock price data"""
        try:
            symbol = self.validate_symbol(symbol)
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": f"No data found for symbol {symbol}"}
            
            current_price = hist['Close'].iloc[-1]
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "previous_close": round(hist['Close'].iloc[-2] if len(hist) > 1 else current_price, 2),
                "change": round(current_price - hist['Close'].iloc[-2] if len(hist) > 1 else 0, 2),
                "change_percent": round(((current_price / hist['Close'].iloc[-2] - 1) * 100) if len(hist) > 1 else 0, 2),
                "volume": int(hist['Volume'].iloc[-1]),
                "high_52w": round(hist['High'].max(), 2),
                "low_52w": round(hist['Low'].min(), 2),
                "period": period,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def get_volatility_analysis(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Calculate volatility metrics for a stock"""
        try:
            symbol = self.validate_symbol(symbol)
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty or len(hist) < 2:
                return {"error": f"Insufficient data for volatility analysis of {symbol}"}
            
            returns = self.calculate_returns(hist['Close'])
            
            daily_vol = self.calculate_volatility(returns, annualize=False)
            annual_vol = self.calculate_volatility(returns, annualize=True)
            
            return {
                "symbol": symbol,
                "period": period,
                "daily_volatility": round(daily_vol * 100, 2),
                "annual_volatility": round(annual_vol * 100, 2),
                "max_daily_return": round(returns.max() * 100, 2),
                "min_daily_return": round(returns.min() * 100, 2),
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def compare_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, Any]:
        """Compare multiple stocks"""
        try:
            if not symbols or len(symbols) < 2:
                return {"error": "At least 2 symbols required for comparison"}
            
            symbols = [self.validate_symbol(s) for s in symbols]
            
            comparison_data = {}
            
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period)
                    
                    if hist.empty:
                        comparison_data[symbol] = {"error": "No data available"}
                        continue
                    
                    current_price = hist['Close'].iloc[-1]
                    start_price = hist['Close'].iloc[0]
                    total_return = (current_price / start_price - 1) * 100
                    
                    returns = self.calculate_returns(hist['Close'])
                    volatility = self.calculate_volatility(returns) * 100
                    
                    comparison_data[symbol] = {
                        "current_price": round(current_price, 2),
                        "total_return": round(total_return, 2),
                        "volatility": round(volatility, 2),
                        "data_points": len(hist)
                    }
                    
                except Exception as e:
                    comparison_data[symbol] = {"error": str(e)}
            
            return {
                "comparison": comparison_data,
                "period": period,
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}

class FinanceApp:
    """Standalone Finance Application"""
    
    def __init__(self):
        self.analyzer = FinanceAnalyzer()
        self.is_running = False
    
    async def start(self):
        """Start the application"""
        print("🏦 Standalone Finance Application")
        print("=" * 50)
        print("✅ Ready to analyze!")
        self.is_running = True
        await self.main_menu()
    
    async def main_menu(self):
        """Display and handle main menu"""
        while self.is_running:
            print("\n" + "=" * 50)
            print("📊 FINANCE ANALYZER - MAIN MENU")
            print("=" * 50)
            print("1. 📈 Get Stock Price")
            print("2. 📊 Volatility Analysis") 
            print("3. 🔍 Compare Stocks")
            print("4. 💡 Quick Analysis")
            print("0. 🚪 Exit")
            print("=" * 50)
            
            try:
                choice = input("\n👉 Enter your choice (0-4): ").strip()
                
                if choice == "0":
                    self.is_running = False
                    print("\n👋 Goodbye!")
                    break
                elif choice == "1":
                    await self.handle_stock_price()
                elif choice == "2":
                    await self.handle_volatility_analysis()
                elif choice == "3":
                    await self.handle_compare_stocks()
                elif choice == "4":
                    await self.handle_quick_analysis()
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                self.is_running = False
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    async def handle_stock_price(self):
        """Handle stock price request"""
        print("\n📈 STOCK PRICE LOOKUP")
        print("-" * 30)
        
        symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
        
        period = input("Enter period (1d/5d/1mo/3mo/6mo/1y, default: 1mo): ").strip() or "1mo"
        
        print(f"\n🔄 Getting price data for {symbol}...")
        result = await self.analyzer.get_stock_price(symbol, period)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n📊 STOCK PRICE REPORT")
            print("=" * 40)
            print(f"Symbol:           {result['symbol']}")
            print(f"Current Price:    ${result['current_price']}")
            print(f"Previous Close:   ${result['previous_close']}")
            print(f"Change:           ${result['change']} ({result['change_percent']:+.2f}%)")
            print(f"Volume:           {result['volume']:,}")
            print(f"52W High:         ${result['high_52w']}")
            print(f"52W Low:          ${result['low_52w']}")
            print("=" * 40)
    
    async def handle_volatility_analysis(self):
        """Handle volatility analysis"""
        print("\n📊 VOLATILITY ANALYSIS")
        print("-" * 30)
        
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
        
        period = input("Enter period (1mo/3mo/6mo/1y/2y, default: 1y): ").strip() or "1y"
        
        print(f"\n🔄 Analyzing volatility for {symbol}...")
        result = await self.analyzer.get_volatility_analysis(symbol, period)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n📈 VOLATILITY ANALYSIS REPORT")
            print("=" * 40)
            print(f"Symbol:              {result['symbol']}")
            print(f"Daily Volatility:    {result['daily_volatility']}%")
            print(f"Annual Volatility:   {result['annual_volatility']}%")
            print(f"Max Daily Return:    {result['max_daily_return']}%")
            print(f"Min Daily Return:    {result['min_daily_return']}%")
            print(f"Period:              {result['period']}")
            print("=" * 40)
    
    async def handle_compare_stocks(self):
        """Handle stock comparison"""
        print("\n🔍 STOCK COMPARISON")
        print("-" * 30)
        
        symbols_input = input("Enter symbols separated by commas (e.g., AAPL,MSFT,GOOGL): ").strip()
        if not symbols_input:
            print("❌ Symbols cannot be empty")
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        period = input("Enter period (default: 1y): ").strip() or "1y"
        
        print(f"\n🔄 Comparing {len(symbols)} stocks...")
        result = await self.analyzer.compare_stocks(symbols, period)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n🔍 STOCK COMPARISON REPORT")
            print("=" * 60)
            print(f"Period: {result['period']}")
            print()
            
            comparison = result['comparison']
            for symbol, metrics in comparison.items():
                if 'error' in metrics:
                    print(f"{symbol}: ❌ {metrics['error']}")
                else:
                    print(f"{symbol}:")
                    print(f"  Current Price:    ${metrics['current_price']}")
                    print(f"  Total Return:     {metrics['total_return']:+.2f}%")
                    print(f"  Volatility:       {metrics['volatility']:.2f}%")
                    print()
            print("=" * 60)
    
    async def handle_quick_analysis(self):
        """Handle quick analysis of popular stocks"""
        print("\n💡 QUICK ANALYSIS")
        print("-" * 30)
        
        popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        print("🔄 Analyzing popular stocks...")
        result = await self.analyzer.compare_stocks(popular_stocks, "1mo")
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n💡 POPULAR STOCKS QUICK ANALYSIS")
            print("=" * 50)
            
            comparison = result['comparison']
            print(f"{'Symbol':<8} {'Price':<10} {'Return':<10} {'Volatility':<12}")
            print("-" * 50)
            
            for symbol, metrics in comparison.items():
                if 'error' not in metrics:
                    price = f"${metrics['current_price']}"
                    ret = f"{metrics['total_return']:+.1f}%"
                    vol = f"{metrics['volatility']:.1f}%"
                    print(f"{symbol:<8} {price:<10} {ret:<10} {vol:<12}")
            print("=" * 50)

async def main():
    """Main entry point"""
    app = FinanceApp()
    try:
        await app.start()
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
