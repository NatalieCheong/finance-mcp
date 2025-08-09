#!/usr/bin/env python3
"""
Finance MCP Main Application
Interactive command-line interface for the Finance MCP system
"""

import asyncio
import json
import sys
from typing import Dict, List, Any
import argparse
from datetime import datetime

# Import our client
from client import FinanceMCPClient, MCPResponse

class FinanceApp:
    """Main Finance Application using MCP"""
    
    def __init__(self):
        self.client = FinanceMCPClient()
        self.is_running = False
        
    async def start(self):
        """Start the application"""
        print("🏦 Finance MCP Application")
        print("=" * 50)
        
        # Connect to MCP server
        print("Connecting to Finance MCP Server...")
        if not await self.client.connect():
            print("❌ Failed to connect to server. Please ensure server.py is available.")
            return
        
        print("✅ Connected successfully!")
        self.is_running = True
        
        # Show main menu
        await self.main_menu()
        
    async def stop(self):
        """Stop the application"""
        if self.client:
            await self.client.disconnect()
        self.is_running = False
        print("\n👋 Goodbye!")
        
    async def main_menu(self):
        """Display and handle main menu"""
        while self.is_running:
            print("\n" + "=" * 50)
            print("📊 FINANCE MCP - MAIN MENU")
            print("=" * 50)
            print("1.  📈 Get Stock Price")
            print("2.  📊 Stock Analysis (Volatility)")
            print("3.  📈 Trend Analysis") 
            print("4.  ⚠️  Risk Analysis")
            print("5.  🔍 Compare Stocks")
            print("6.  📋 Financial Summary")
            print("7.  💼 Portfolio Analysis")
            print("8.  🏛️  Market Indices")
            print("9.  🔍 Search Stocks")
            print("10. 📊 Custom Analysis Menu")
            print("11. ❓ Help")
            print("0.  🚪 Exit")
            print("=" * 50)
            
            try:
                choice = input("\n👉 Enter your choice (0-11): ").strip()
                
                if choice == "0":
                    await self.stop()
                    break
                elif choice == "1":
                    await self.handle_stock_price()
                elif choice == "2":
                    await self.handle_volatility_analysis()
                elif choice == "3":
                    await self.handle_trend_analysis()
                elif choice == "4":
                    await self.handle_risk_analysis()
                elif choice == "5":
                    await self.handle_compare_stocks()
                elif choice == "6":
                    await self.handle_financial_summary()
                elif choice == "7":
                    await self.handle_portfolio_analysis()
                elif choice == "8":
                    await self.handle_market_indices()
                elif choice == "9":
                    await self.handle_search_stocks()
                elif choice == "10":
                    await self.custom_analysis_menu()
                elif choice == "11":
                    self.show_help()
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                await self.stop()
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
            
        print("\nAvailable periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y")
        period = input("Enter period (default: 1mo): ").strip() or "1mo"
        
        print(f"\n🔄 Getting price data for {symbol}...")
        response = await self.client.get_stock_price(symbol, period)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_stock_price(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_stock_price(self, data: Dict[str, Any]):
        """Display stock price data"""
        print(f"\n📊 STOCK PRICE REPORT")
        print("=" * 40)
        print(f"Symbol:           {data.get('symbol')}")
        print(f"Current Price:    ${data.get('current_price')}")
        print(f"Previous Close:   ${data.get('previous_close')}")
        print(f"Change:           ${data.get('change')} ({data.get('change_percent', 0):+.2f}%)")
        print(f"Volume:           {data.get('volume'):,}")
        print(f"52W High:         ${data.get('high_52w')}")
        print(f"52W Low:          ${data.get('low_52w')}")
        print(f"Currency:         {data.get('currency')}")
        print(f"Period:           {data.get('period')}")
        print(f"Data Points:      {data.get('data_points')}")
        print("=" * 40)
    
    async def handle_volatility_analysis(self):
        """Handle volatility analysis"""
        print("\n📊 VOLATILITY ANALYSIS")
        print("-" * 30)
        
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
            
        period = input("Enter period (default: 1y): ").strip() or "1y"
        
        print(f"\n🔄 Analyzing volatility for {symbol}...")
        response = await self.client.get_volatility_analysis(symbol, period)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_volatility_analysis(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_volatility_analysis(self, data: Dict[str, Any]):
        """Display volatility analysis"""
        print(f"\n📈 VOLATILITY ANALYSIS REPORT")
        print("=" * 40)
        print(f"Symbol:              {data.get('symbol')}")
        print(f"Daily Volatility:    {data.get('daily_volatility')}%")
        print(f"Annual Volatility:   {data.get('annual_volatility')}%")
        print(f"30-Day Volatility:   {data.get('current_30d_volatility')}%")
        print(f"60-Day Volatility:   {data.get('current_60d_volatility')}%")
        print(f"Volatility Trend:    {data.get('volatility_trend')}")
        print(f"Max Daily Return:    {data.get('max_daily_return')}%")
        print(f"Min Daily Return:    {data.get('min_daily_return')}%")
        print(f"Period:              {data.get('period')}")
        print("=" * 40)
    
    async def handle_trend_analysis(self):
        """Handle trend analysis"""
        print("\n📈 TREND ANALYSIS")
        print("-" * 30)
        
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
            
        period = input("Enter period (default: 6mo): ").strip() or "6mo"
        
        print(f"\n🔄 Analyzing trends for {symbol}...")
        response = await self.client.get_trend_analysis(symbol, period)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_trend_analysis(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_trend_analysis(self, data: Dict[str, Any]):
        """Display trend analysis"""
        print(f"\n📊 TREND ANALYSIS REPORT")
        print("=" * 40)
        print(f"Symbol:              {data.get('symbol')}")
        print(f"Current Price:       ${data.get('current_price')}")
        print(f"20-Day MA:           ${data.get('ma_20')}")
        print(f"50-Day MA:           ${data.get('ma_50')}")
        print(f"200-Day MA:          ${data.get('ma_200')}")
        print(f"Short-term Trend:    {data.get('short_term_trend')}")
        print(f"Medium-term Trend:   {data.get('medium_term_trend')}")
        print(f"Long-term Trend:     {data.get('long_term_trend')}")
        print(f"Overall Trend:       {data.get('overall_trend')}")
        print(f"Golden Cross:        {data.get('golden_cross')}")
        print(f"10-Day Momentum:     {data.get('momentum_10d')}%")
        print(f"30-Day Momentum:     {data.get('momentum_30d')}%")
        print("=" * 40)
    
    async def handle_risk_analysis(self):
        """Handle risk analysis"""
        print("\n⚠️ RISK ANALYSIS")
        print("-" * 30)
        
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
            
        period = input("Enter period (default: 1y): ").strip() or "1y"
        benchmark = input("Enter benchmark (default: ^GSPC): ").strip() or "^GSPC"
        
        print(f"\n🔄 Analyzing risk for {symbol}...")
        response = await self.client.get_risk_analysis(symbol, period, benchmark)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_risk_analysis(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_risk_analysis(self, data: Dict[str, Any]):
        """Display risk analysis"""
        print(f"\n⚠️ RISK ANALYSIS REPORT")
        print("=" * 40)
        print(f"Symbol:               {data.get('symbol')}")
        print(f"Benchmark:            {data.get('benchmark')}")
        print(f"Annual Volatility:    {data.get('volatility_annual')}%")
        print(f"Sharpe Ratio:         {data.get('sharpe_ratio')}")
        print(f"Beta:                 {data.get('beta')}")
        print(f"VaR (5%):             {data.get('var_5_percent')}%")
        print(f"VaR (1%):             {data.get('var_1_percent')}%")
        print(f"Max Drawdown:         {data.get('max_drawdown')}%")
        print(f"Downside Deviation:   {data.get('downside_deviation')}%")
        print(f"Risk Rating:          {data.get('risk_rating')}")
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
        response = await self.client.compare_stocks(symbols, period)
        
        if response.success:
            data = response.data
            self.display_stock_comparison(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_stock_comparison(self, data: Dict[str, Any]):
        """Display stock comparison"""
        print(f"\n🔍 STOCK COMPARISON REPORT")
        print("=" * 60)
        print(f"Period: {data.get('period')}")
        print(f"Symbols Analyzed: {data.get('symbols_analyzed')}")
        print()
        
        comparison = data.get('comparison', {})
        for symbol, metrics in comparison.items():
            if 'error' in metrics:
                print(f"{symbol}: ❌ {metrics['error']}")
            else:
                print(f"{symbol}:")
                print(f"  Current Price:    ${metrics.get('current_price')}")
                print(f"  Total Return:     {metrics.get('total_return')}%")
                print(f"  Annual Return:    {metrics.get('annual_return')}%")
                print(f"  Volatility:       {metrics.get('volatility')}%")
                print(f"  Sharpe Ratio:     {metrics.get('sharpe_ratio')}")
                print(f"  Beta:             {metrics.get('beta')}")
                print()
        
        # Best performers
        if data.get('best_return_symbol'):
            print(f"🏆 Best Return: {data.get('best_return_symbol')}")
        if data.get('best_sharpe_symbol'):
            print(f"🏆 Best Sharpe: {data.get('best_sharpe_symbol')}")
        if data.get('lowest_volatility_symbol'):
            print(f"🏆 Lowest Volatility: {data.get('lowest_volatility_symbol')}")
        print("=" * 60)
    
    async def handle_financial_summary(self):
        """Handle financial summary"""
        print("\n📋 FINANCIAL SUMMARY")
        print("-" * 30)
        
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("❌ Symbol cannot be empty")
            return
        
        print(f"\n🔄 Getting financial summary for {symbol}...")
        response = await self.client.get_financial_summary(symbol)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_financial_summary(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_financial_summary(self, data: Dict[str, Any]):
        """Display financial summary"""
        print(f"\n📋 FINANCIAL SUMMARY REPORT")
        print("=" * 50)
        print(f"Company:          {data.get('company_name')}")
        print(f"Symbol:           {data.get('symbol')}")
        print(f"Sector:           {data.get('sector')}")
        print(f"Industry:         {data.get('industry')}")
        print(f"Market Cap:       {data.get('market_cap_formatted', 'N/A')}")
        print(f"P/E Ratio:        {data.get('pe_ratio', 'N/A')}")
        print(f"Forward P/E:      {data.get('forward_pe', 'N/A')}")
        print(f"Price to Book:    {data.get('price_to_book', 'N/A')}")
        print(f"Debt to Equity:   {data.get('debt_to_equity', 'N/A')}")
        print(f"ROE:              {data.get('roe', 'N/A')}")
        print(f"Profit Margin:    {data.get('profit_margin', 'N/A')}")
        print(f"Dividend Yield:   {data.get('dividend_yield', 'N/A')}")
        print(f"Beta:             {data.get('beta', 'N/A')}")
        print(f"52W High:         ${data.get('52_week_high', 'N/A')}")
        print(f"52W Low:          ${data.get('52_week_low', 'N/A')}")
        print(f"Valuation:        {data.get('valuation', 'N/A')}")
        print("=" * 50)
        
        if data.get('description') and data['description'] != 'N/A':
            print(f"\nDescription:\n{data['description']}")
            print("=" * 50)
    
    async def handle_portfolio_analysis(self):
        """Handle portfolio analysis"""
        print("\n💼 PORTFOLIO ANALYSIS")
        print("-" * 30)
        
        symbols_input = input("Enter symbols separated by commas: ").strip()
        if not symbols_input:
            print("❌ Symbols cannot be empty")
            return
            
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        
        weights_input = input("Enter weights separated by commas (or press Enter for equal weights): ").strip()
        weights = None
        if weights_input:
            try:
                weights = [float(w.strip()) for w in weights_input.split(',')]
            except ValueError:
                print("❌ Invalid weights format")
                return
        
        period = input("Enter period (default: 1y): ").strip() or "1y"
        
        print(f"\n🔄 Analyzing portfolio...")
        response = await self.client.get_portfolio_analysis(symbols, weights, period)
        
        if response.success:
            data = response.data
            if 'error' in data:
                print(f"❌ {data['error']}")
            else:
                self.display_portfolio_analysis(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_portfolio_analysis(self, data: Dict[str, Any]):
        """Display portfolio analysis"""
        print(f"\n💼 PORTFOLIO ANALYSIS REPORT")
        print("=" * 50)
        
        # Portfolio metrics
        portfolio_metrics = data.get('portfolio_metrics', {})
        print("PORTFOLIO METRICS:")
        print(f"  Annual Return:     {portfolio_metrics.get('annual_return')}%")
        print(f"  Volatility:        {portfolio_metrics.get('volatility')}%")
        print(f"  Sharpe Ratio:      {portfolio_metrics.get('sharpe_ratio')}")
        print(f"  Max Drawdown:      {portfolio_metrics.get('max_drawdown')}%")
        print()
        
        # Individual holdings
        print("INDIVIDUAL HOLDINGS:")
        symbols = data.get('symbols', [])
        weights = data.get('weights', [])
        individual_metrics = data.get('individual_metrics', {})
        
        for symbol in symbols:
            metrics = individual_metrics.get(symbol, {})
            print(f"  {symbol}:")
            print(f"    Weight:            {metrics.get('weight')}%")
            print(f"    Volatility:        {metrics.get('volatility')}%")
            print(f"    Sharpe Ratio:      {metrics.get('sharpe_ratio')}")
            print(f"    Return Contrib:    {metrics.get('contribution_to_return')}%")
        
        print(f"\nDiversification Ratio: {data.get('diversification_ratio')}")
        print("=" * 50)
    
    async def handle_market_indices(self):
        """Handle market indices request"""
        print("\n🏛️ MARKET INDICES")
        print("-" * 30)
        
        custom_indices = input("Enter custom indices (comma-separated) or press Enter for default: ").strip()
        indices = None
        if custom_indices:
            indices = [s.strip().upper() for s in custom_indices.split(',')]
        
        print(f"\n🔄 Getting market indices...")
        response = await self.client.get_market_indices(indices)
        
        if response.success:
            data = response.data
            self.display_market_indices(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_market_indices(self, data: Dict[str, Any]):
        """Display market indices"""
        print(f"\n🏛️ MARKET INDICES REPORT")
        print("=" * 50)
        
        indices_data = data.get('indices', {})
        for index, info in indices_data.items():
            if 'error' in info:
                print(f"{index}: ❌ {info['error']}")
            else:
                change_emoji = "📈" if info.get('change_percent', 0) >= 0 else "📉"
                print(f"{change_emoji} {info.get('name', index)}")
                print(f"   Value: {info.get('value')}")
                print(f"   Change: {info.get('change')} ({info.get('change_percent'):+.2f}%)")
        
        print(f"\nMarket Sentiment: {data.get('market_sentiment')}")
        print("=" * 50)
    
    async def handle_search_stocks(self):
        """Handle stock search"""
        print("\n🔍 STOCK SEARCH")
        print("-" * 30)
        
        query = input("Enter search query (company name or symbol): ").strip()
        if not query:
            print("❌ Query cannot be empty")
            return
        
        max_results = input("Max results (default: 10): ").strip() or "10"
        try:
            max_results = int(max_results)
        except ValueError:
            max_results = 10
        
        print(f"\n🔄 Searching for '{query}'...")
        response = await self.client.search_stocks(query, max_results)
        
        if response.success:
            data = response.data
            self.display_search_results(data)
        else:
            print(f"❌ Error: {response.error}")
    
    def display_search_results(self, data: Dict[str, Any]):
        """Display search results"""
        print(f"\n🔍 SEARCH RESULTS")
        print("=" * 40)
        print(f"Query: {data.get('query')}")
        print(f"Total Results: {data.get('total_results')}")
        print()
        
        results = data.get('results', [])
        if not results:
            print("No results found.")
        else:
            for result in results:
                print(f"Symbol: {result.get('symbol')}")
                print(f"Name: {result.get('name')}")
                print(f"Sector: {result.get('sector')}")
                if result.get('current_price'):
                    print(f"Price: ${result.get('current_price')}")
                print("-" * 20)
        print("=" * 40)
    
    async def custom_analysis_menu(self):
        """Custom analysis menu"""
        while True:
            print("\n📊 CUSTOM ANALYSIS MENU")
            print("-" * 30)
            print("1. Multi-Stock Risk Comparison")
            print("2. Sector Analysis")
            print("3. Correlation Analysis")
            print("4. Export Data to JSON")
            print("5. Batch Analysis")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                await self.multi_stock_risk_comparison()
            elif choice == "2":
                await self.sector_analysis()
            elif choice == "3":
                await self.correlation_analysis()
            elif choice == "4":
                await self.export_data()
            elif choice == "5":
                await self.batch_analysis()
            else:
                print("❌ Invalid choice")
    
    async def multi_stock_risk_comparison(self):
        """Compare risk metrics for multiple stocks"""
        print("\n⚠️ MULTI-STOCK RISK COMPARISON")
        print("-" * 30)
        
        symbols_input = input("Enter symbols (comma-separated): ").strip()
        if not symbols_input:
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        period = input("Period (default: 1y): ").strip() or "1y"
        
        print("\n🔄 Analyzing risk for all symbols...")
        
        risk_data = {}
        for symbol in symbols:
            response = await self.client.get_risk_analysis(symbol, period)
            if response.success and 'error' not in response.data:
                risk_data[symbol] = response.data
        
        if risk_data:
            print(f"\n⚠️ RISK COMPARISON REPORT")
            print("=" * 60)
            print(f"{'Symbol':<8} {'Volatility':<12} {'Sharpe':<8} {'Beta':<6} {'Risk Rating':<12}")
            print("-" * 60)
            
            for symbol, data in risk_data.items():
                volatility = data.get('volatility_annual', 'N/A')
                sharpe = data.get('sharpe_ratio', 'N/A')
                beta = data.get('beta', 'N/A')
                risk_rating = data.get('risk_rating', 'N/A')
                
                print(f"{symbol:<8} {volatility:<12} {sharpe:<8} {beta:<6} {risk_rating:<12}")
            print("=" * 60)
    
    async def sector_analysis(self):
        """Analyze stocks by sector"""
        print("\n🏭 SECTOR ANALYSIS")
        print("-" * 30)
        print("Enter stocks from the same sector for comparison")
        
        symbols_input = input("Enter symbols (comma-separated): ").strip()
        if not symbols_input:
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        
        print("\n🔄 Getting financial summaries...")
        
        sector_data = {}
        for symbol in symbols:
            response = await self.client.get_financial_summary(symbol)
            if response.success and 'error' not in response.data:
                sector_data[symbol] = response.data
        
        if sector_data:
            print(f"\n🏭 SECTOR ANALYSIS REPORT")
            print("=" * 50)
            
            # Group by sector
            sectors = {}
            for symbol, data in sector_data.items():
                sector = data.get('sector', 'Unknown')
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append((symbol, data))
            
            for sector, companies in sectors.items():
                print(f"\nSector: {sector}")
                print("-" * 30)
                for symbol, data in companies:
                    print(f"{symbol}: {data.get('company_name', 'N/A')}")
                    print(f"  P/E Ratio: {data.get('pe_ratio', 'N/A')}")
                    print(f"  Market Cap: {data.get('market_cap_formatted', 'N/A')}")
                    print(f"  Profit Margin: {data.get('profit_margin', 'N/A')}")
            print("=" * 50)
    
    async def correlation_analysis(self):
        """Analyze correlation between stocks"""
        print("\n📊 CORRELATION ANALYSIS")
        print("-" * 30)
        
        symbols_input = input("Enter symbols (comma-separated): ").strip()
        if not symbols_input:
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        if len(symbols) < 2:
            print("❌ Need at least 2 symbols for correlation analysis")
            return
        
        # Use portfolio analysis to get correlation matrix
        response = await self.client.get_portfolio_analysis(symbols, period="1y")
        
        if response.success and 'error' not in response.data:
            correlation_matrix = response.data.get('correlation_matrix', {})
            
            print(f"\n📊 CORRELATION MATRIX")
            print("=" * 50)
            print("Note: Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation)")
            print()
            
            # Display correlation matrix
            print(f"{'Symbol':<8}", end="")
            for symbol in symbols:
                print(f"{symbol:<8}", end="")
            print()
            print("-" * (8 * (len(symbols) + 1)))
            
            for symbol1 in symbols:
                print(f"{symbol1:<8}", end="")
                for symbol2 in symbols:
                    corr_value = correlation_matrix.get(symbol1, {}).get(symbol2, 0)
                    print(f"{corr_value:<8.3f}", end="")
                print()
            print("=" * 50)
        else:
            print("❌ Error getting correlation data")
    
    async def export_data(self):
        """Export analysis data to JSON"""
        print("\n💾 EXPORT DATA")
        print("-" * 30)
        
        symbol = input("Enter symbol to export: ").strip().upper()
        if not symbol:
            return
        
        export_data = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "analyses": {}
        }
        
        print("🔄 Gathering data...")
        
        # Get all available data
        analyses = [
            ("stock_price", self.client.get_stock_price(symbol)),
            ("volatility", self.client.get_volatility_analysis(symbol)),
            ("trend", self.client.get_trend_analysis(symbol)),
            ("risk", self.client.get_risk_analysis(symbol)),
            ("financial_summary", self.client.get_financial_summary(symbol))
        ]
        
        for analysis_name, coro in analyses:
            try:
                response = await coro
                if response.success:
                    export_data["analyses"][analysis_name] = response.data
            except Exception as e:
                export_data["analyses"][analysis_name] = {"error": str(e)}
        
        # Save to file
        filename = f"{symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Data exported to {filename}")
    
    async def batch_analysis(self):
        """Batch analysis for multiple stocks"""
        print("\n📊 BATCH ANALYSIS")
        print("-" * 30)
        
        symbols_input = input("Enter symbols (comma-separated): ").strip()
        if not symbols_input:
            return
        
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        
        print(f"🔄 Running batch analysis for {len(symbols)} symbols...")
        
        batch_results = {}
        for i, symbol in enumerate(symbols, 1):
            print(f"Processing {symbol} ({i}/{len(symbols)})...")
            
            # Get basic metrics for each symbol
            price_response = await self.client.get_stock_price(symbol)
            vol_response = await self.client.get_volatility_analysis(symbol)
            
            batch_results[symbol] = {
                "price_data": price_response.data if price_response.success else {"error": "Failed"},
                "volatility_data": vol_response.data if vol_response.success else {"error": "Failed"}
            }
        
        # Display summary
        print(f"\n📊 BATCH ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"{'Symbol':<8} {'Price':<10} {'Change%':<10} {'Volatility':<12}")
        print("-" * 60)
        
        for symbol, data in batch_results.items():
            price_data = data.get("price_data", {})
            vol_data = data.get("volatility_data", {})
            
            price = price_data.get("current_price", "N/A")
            change_pct = price_data.get("change_percent", "N/A")
            volatility = vol_data.get("annual_volatility", "N/A")
            
            print(f"{symbol:<8} ${price:<9} {change_pct:<9}% {volatility:<11}%")
        
        print("=" * 60)
    
    def show_help(self):
        """Show help information"""
        print("\n❓ HELP - FINANCE MCP APPLICATION")
        print("=" * 50)
        print("This application provides comprehensive financial analysis tools:")
        print()
        print("📈 Stock Price: Get current and historical price data")
        print("📊 Volatility Analysis: Measure price volatility and risk")
        print("📈 Trend Analysis: Analyze price trends and moving averages")
        print("⚠️  Risk Analysis: Calculate VaR, Sharpe ratio, and Beta")
        print("🔍 Compare Stocks: Side-by-side comparison of multiple stocks")
        print("📋 Financial Summary: Company fundamentals and ratios")
        print("💼 Portfolio Analysis: Analyze portfolio risk and returns")
        print("🏛️  Market Indices: Major market index data")
        print("🔍 Search Stocks: Find stocks by name or symbol")
        print("📊 Custom Analysis: Advanced analysis tools")
        print()
        print("📝 Tips:")
        print("- Use standard ticker symbols (e.g., AAPL, MSFT, GOOGL)")
        print("- Available periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y")
        print("- Separate multiple symbols with commas")
        print("- Portfolio weights must sum to 1.0")
        print("- Press Ctrl+C to exit at any time")
        print("=" * 50)

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Finance MCP Application")
    parser.add_argument("--symbol", help="Stock symbol for quick analysis")
    parser.add_argument("--analysis", choices=["price", "volatility", "trend", "risk"], 
                       help="Type of analysis to run")
    
    args = parser.parse_args()
    
    app = FinanceApp()
    
    try:
        if args.symbol and args.analysis:
            # Command line mode
            await app.client.connect()
            
            if args.analysis == "price":
                response = await app.client.get_stock_price(args.symbol)
            elif args.analysis == "volatility":
                response = await app.client.get_volatility_analysis(args.symbol)
            elif args.analysis == "trend":
                response = await app.client.get_trend_analysis(args.symbol)
            elif args.analysis == "risk":
                response = await app.client.get_risk_analysis(args.symbol)
            
            if response.success:
                print(json.dumps(response.data, indent=2))
            else:
                print(f"Error: {response.error}")
            
            await app.client.disconnect()
        else:
            # Interactive mode
            await app.start()
            
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {str(e)}")
    finally:
        if app.is_running:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
