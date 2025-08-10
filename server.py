"""
Finance MCP Server
A comprehensive financial analysis server using MCP (Model Context Protocol)
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import traceback

import yfinance as yf
import pandas as pd
import numpy as np
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Stock Price Server")

# Guardrails and validation
ALLOWED_SYMBOLS = set()  # Empty means allow all, populate to restrict
MAX_PERIOD_DAYS = 5 * 365  # 5 years max
MIN_PERIOD_DAYS = 1
RATE_LIMIT = {}  # Simple rate limiting per function

def validate_symbol(symbol: str) -> str:
    """Validate and sanitize stock symbol"""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    symbol = symbol.upper().strip()
    if not symbol.replace('.', '').replace('-', '').isalnum():
        raise ValueError("Invalid symbol format")
    
    if ALLOWED_SYMBOLS and symbol not in ALLOWED_SYMBOLS:
        raise ValueError(f"Symbol {symbol} not in allowed list")
    
    return symbol

def validate_period(period: str) -> str:
    """Validate time period"""
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if period not in valid_periods:
        raise ValueError(f"Period must be one of: {', '.join(valid_periods)}")
    return period

def validate_date_range(start_date: str, end_date: str) -> tuple:
    """Validate date range"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            raise ValueError("Start date must be before end date")
        
        if (end - start).days > MAX_PERIOD_DAYS:
            raise ValueError(f"Date range cannot exceed {MAX_PERIOD_DAYS} days")
            
        if end > datetime.now():
            raise ValueError("End date cannot be in the future")
            
        return start, end
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Dates must be in YYYY-MM-DD format")
        raise

def safe_divide(a, b):
    """Safe division to avoid division by zero"""
    return a / b if b != 0 else 0

def calculate_returns(prices: pd.Series) -> pd.Series:
    """Calculate daily returns"""
    return prices.pct_change().dropna()

def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
    """Calculate volatility (standard deviation of returns)"""
    vol = returns.std()
    if annualize:
        vol *= np.sqrt(252)  # Annualize assuming 252 trading days
    return vol

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio"""
    excess_returns = returns.mean() * 252 - risk_free_rate
    volatility = calculate_volatility(returns, annualize=True)
    return safe_divide(excess_returns, volatility)

@mcp.tool()
async def get_stock_price(
    symbol: str,
    period: str = "1mo"
) -> Dict[str, Any]:
    """
    Get current and historical stock price data
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        Dict containing current price, historical data, and basic statistics
    """
    try:
        symbol = validate_symbol(symbol)
        period = validate_period(period)
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return {"error": f"No data found for symbol {symbol}"}
        
        info = ticker.info
        current_price = hist['Close'].iloc[-1]
        
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "currency": info.get('currency', 'USD'),
            "previous_close": round(hist['Close'].iloc[-2] if len(hist) > 1 else current_price, 2),
            "change": round(current_price - hist['Close'].iloc[-2] if len(hist) > 1 else 0, 2),
            "change_percent": round(((current_price / hist['Close'].iloc[-2] - 1) * 100) if len(hist) > 1 else 0, 2),
            "volume": int(hist['Volume'].iloc[-1]),
            "high_52w": round(hist['High'].max(), 2),
            "low_52w": round(hist['Low'].min(), 2),
            "period": period,
            "data_points": len(hist),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stock price for {symbol}: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_volatility_analysis(
    symbol: str,
    period: str = "1y"
) -> Dict[str, Any]:
    """
    Calculate volatility metrics for a stock
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for analysis
        
    Returns:
        Dict containing various volatility metrics
    """
    try:
        symbol = validate_symbol(symbol)
        period = validate_period(period)
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty or len(hist) < 2:
            return {"error": f"Insufficient data for volatility analysis of {symbol}"}
        
        returns = calculate_returns(hist['Close'])
        
        # Calculate various volatility metrics
        daily_vol = calculate_volatility(returns, annualize=False)
        annual_vol = calculate_volatility(returns, annualize=True)
        
        # Rolling volatilities
        rolling_30 = returns.rolling(30).std() * np.sqrt(252)
        rolling_60 = returns.rolling(60).std() * np.sqrt(252)
        
        return {
            "symbol": symbol,
            "period": period,
            "daily_volatility": round(daily_vol * 100, 2),
            "annual_volatility": round(annual_vol * 100, 2),
            "current_30d_volatility": round(rolling_30.iloc[-1] * 100, 2) if not pd.isna(rolling_30.iloc[-1]) else None,
            "current_60d_volatility": round(rolling_60.iloc[-1] * 100, 2) if not pd.isna(rolling_60.iloc[-1]) else None,
            "volatility_trend": "increasing" if rolling_30.iloc[-1] > rolling_60.iloc[-1] else "decreasing",
            "max_daily_return": round(returns.max() * 100, 2),
            "min_daily_return": round(returns.min() * 100, 2),
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating volatility for {symbol}: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_trend_analysis(
    symbol: str,
    period: str = "6mo"
) -> Dict[str, Any]:
    """
    Analyze price trends using moving averages and momentum indicators
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for analysis
        
    Returns:
        Dict containing trend analysis results
    """
    try:
        symbol = validate_symbol(symbol)
        period = validate_period(period)
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty or len(hist) < 50:
            return {"error": f"Insufficient data for trend analysis of {symbol}"}
        
        close_prices = hist['Close']
        
        # Moving averages
        ma_20 = close_prices.rolling(20).mean()
        ma_50 = close_prices.rolling(50).mean()
        ma_200 = close_prices.rolling(200).mean() if len(close_prices) >= 200 else None
        
        current_price = close_prices.iloc[-1]
        
        # Trend determination
        short_trend = "bullish" if current_price > ma_20.iloc[-1] else "bearish"
        medium_trend = "bullish" if current_price > ma_50.iloc[-1] else "bearish"
        long_trend = "bullish" if ma_200 is not None and current_price > ma_200.iloc[-1] else "neutral"
        
        # Golden/Death cross detection
        golden_cross = ma_50.iloc[-1] > ma_200.iloc[-1] if ma_200 is not None else None
        
        # Price momentum (rate of change)
        momentum_10d = (current_price / close_prices.iloc[-11] - 1) * 100 if len(close_prices) > 10 else None
        momentum_30d = (current_price / close_prices.iloc[-31] - 1) * 100 if len(close_prices) > 30 else None
        
        return {
            "symbol": symbol,
            "period": period,
            "current_price": round(current_price, 2),
            "ma_20": round(ma_20.iloc[-1], 2),
            "ma_50": round(ma_50.iloc[-1], 2),
            "ma_200": round(ma_200.iloc[-1], 2) if ma_200 is not None else None,
            "short_term_trend": short_trend,
            "medium_term_trend": medium_trend,
            "long_term_trend": long_trend,
            "golden_cross": golden_cross,
            "momentum_10d": round(momentum_10d, 2) if momentum_10d else None,
            "momentum_30d": round(momentum_30d, 2) if momentum_30d else None,
            "overall_trend": "bullish" if [short_trend, medium_trend, long_trend].count("bullish") >= 2 else "bearish",
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing trend for {symbol}: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_risk_analysis(
    symbol: str,
    period: str = "1y",
    benchmark: str = "^GSPC"
) -> Dict[str, Any]:
    """
    Comprehensive risk analysis including VaR, Sharpe ratio, and Beta
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for analysis
        benchmark: Benchmark index (default: S&P 500)
        
    Returns:
        Dict containing risk metrics
    """
    try:
        symbol = validate_symbol(symbol)
        benchmark = validate_symbol(benchmark)
        period = validate_period(period)
        
        # Get stock data
        stock = yf.Ticker(symbol)
        stock_hist = stock.history(period=period)
        
        # Get benchmark data
        bench = yf.Ticker(benchmark)
        bench_hist = bench.history(period=period)
        
        if stock_hist.empty or bench_hist.empty:
            return {"error": f"Insufficient data for risk analysis"}
        
        # Calculate returns
        stock_returns = calculate_returns(stock_hist['Close'])
        bench_returns = calculate_returns(bench_hist['Close'])
        
        # Align data
        aligned_data = pd.concat([stock_returns, bench_returns], axis=1, join='inner')
        aligned_data.columns = ['stock', 'benchmark']
        aligned_data = aligned_data.dropna()
        
        if len(aligned_data) < 30:
            return {"error": "Insufficient overlapping data for analysis"}
        
        stock_aligned = aligned_data['stock']
        bench_aligned = aligned_data['benchmark']
        
        # Risk metrics
        volatility = calculate_volatility(stock_aligned)
        sharpe_ratio = calculate_sharpe_ratio(stock_aligned)
        
        # Beta calculation
        covariance = np.cov(stock_aligned, bench_aligned)[0][1]
        benchmark_variance = np.var(bench_aligned)
        beta = safe_divide(covariance, benchmark_variance)
        
        # Value at Risk (VaR) - 5% confidence level
        var_5 = np.percentile(stock_aligned, 5) * 100
        var_1 = np.percentile(stock_aligned, 1) * 100
        
        # Maximum drawdown
        cumulative_returns = (1 + stock_aligned).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min() * 100
        
        # Downside deviation
        downside_returns = stock_aligned[stock_aligned < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        return {
            "symbol": symbol,
            "period": period,
            "benchmark": benchmark,
            "volatility_annual": round(volatility * 100, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "beta": round(beta, 2),
            "var_5_percent": round(var_5, 2),
            "var_1_percent": round(var_1, 2),
            "max_drawdown": round(max_drawdown, 2),
            "downside_deviation": round(downside_deviation * 100, 2),
            "risk_rating": "Low" if volatility < 0.15 else "Medium" if volatility < 0.25 else "High",
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating risk metrics for {symbol}: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def compare_stocks(
    symbols: List[str],
    period: str = "1y",
    metrics: List[str] = None
) -> Dict[str, Any]:
    """
    Compare multiple stocks across various metrics
    
    Args:
        symbols: List of stock ticker symbols
        period: Time period for comparison
        metrics: List of metrics to compare ['returns', 'volatility', 'sharpe', 'beta']
        
    Returns:
        Dict containing comparison results
    """
    try:
        if not symbols or len(symbols) < 2:
            return {"error": "At least 2 symbols required for comparison"}
        
        if len(symbols) > 10:
            return {"error": "Maximum 10 symbols allowed for comparison"}
        
        symbols = [validate_symbol(s) for s in symbols]
        period = validate_period(period)
        
        if metrics is None:
            metrics = ['returns', 'volatility', 'sharpe']
        
        comparison_data = {}
        benchmark = yf.Ticker("^GSPC").history(period=period)
        bench_returns = calculate_returns(benchmark['Close']) if not benchmark.empty else None
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                
                if hist.empty:
                    comparison_data[symbol] = {"error": "No data available"}
                    continue
                
                returns = calculate_returns(hist['Close'])
                
                metrics_data = {
                    "current_price": round(hist['Close'].iloc[-1], 2),
                    "total_return": round((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100, 2),
                    "data_points": len(hist)
                }
                
                if 'returns' in metrics:
                    metrics_data['annual_return'] = round(returns.mean() * 252 * 100, 2)
                
                if 'volatility' in metrics:
                    metrics_data['volatility'] = round(calculate_volatility(returns) * 100, 2)
                
                if 'sharpe' in metrics:
                    metrics_data['sharpe_ratio'] = round(calculate_sharpe_ratio(returns), 2)
                
                if 'beta' in metrics and bench_returns is not None:
                    aligned_data = pd.concat([returns, bench_returns], axis=1, join='inner').dropna()
                    if len(aligned_data) > 30:
                        covariance = np.cov(aligned_data.iloc[:, 0], aligned_data.iloc[:, 1])[0][1]
                        benchmark_var = np.var(aligned_data.iloc[:, 1])
                        metrics_data['beta'] = round(safe_divide(covariance, benchmark_var), 2)
                
                comparison_data[symbol] = metrics_data
                
            except Exception as e:
                comparison_data[symbol] = {"error": str(e)}
        
        # Find best performers
        best_return = max([v.get('total_return', -999) for v in comparison_data.values() if isinstance(v, dict) and 'total_return' in v], default=None)
        best_sharpe = max([v.get('sharpe_ratio', -999) for v in comparison_data.values() if isinstance(v, dict) and 'sharpe_ratio' in v], default=None)
        lowest_vol = min([v.get('volatility', 999) for v in comparison_data.values() if isinstance(v, dict) and 'volatility' in v], default=None)
        
        return {
            "comparison": comparison_data,
            "period": period,
            "symbols_analyzed": len(symbols),
            "best_return_symbol": [k for k, v in comparison_data.items() if v.get('total_return') == best_return][0] if best_return else None,
            "best_sharpe_symbol": [k for k, v in comparison_data.items() if v.get('sharpe_ratio') == best_sharpe][0] if best_sharpe else None,
            "lowest_volatility_symbol": [k for k, v in comparison_data.items() if v.get('volatility') == lowest_vol][0] if lowest_vol else None,
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error comparing stocks: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_financial_summary(
    symbol: str
) -> Dict[str, Any]:
    """
    Get comprehensive financial summary including key ratios and company info
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dict containing financial summary
    """
    try:
        symbol = validate_symbol(symbol)
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info:
            return {"error": f"No financial data available for {symbol}"}
        
        # Extract key financial metrics
        summary = {
            "symbol": symbol,
            "company_name": info.get('longName', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap'),
            "enterprise_value": info.get('enterpriseValue'),
            "pe_ratio": info.get('trailingPE'),
            "forward_pe": info.get('forwardPE'),
            "price_to_book": info.get('priceToBook'),
            "price_to_sales": info.get('priceToSalesTrailing12Months'),
            "debt_to_equity": info.get('debtToEquity'),
            "roe": info.get('returnOnEquity'),
            "profit_margin": info.get('profitMargins'),
            "dividend_yield": info.get('dividendYield'),
            "beta": info.get('beta'),
            "52_week_high": info.get('fiftyTwoWeekHigh'),
            "52_week_low": info.get('fiftyTwoWeekLow'),
            "average_volume": info.get('averageVolume'),
            "description": info.get('longBusinessSummary', 'N/A')[:500] + '...' if info.get('longBusinessSummary') else 'N/A'
        }
        
        # Format large numbers
        if summary['market_cap']:
            summary['market_cap_formatted'] = f"${summary['market_cap']:,.0f}"
        
        # Add valuation assessment
        pe_ratio = summary.get('pe_ratio')
        if pe_ratio:
            if pe_ratio < 15:
                summary['valuation'] = 'Undervalued'
            elif pe_ratio > 25:
                summary['valuation'] = 'Overvalued'
            else:
                summary['valuation'] = 'Fairly Valued'
        
        summary['last_updated'] = datetime.now().isoformat()
        
        return summary
        
    except Exception as e:
        logger.error(f"Error getting financial summary for {symbol}: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_portfolio_analysis(
    symbols: List[str],
    weights: List[float] = None,
    period: str = "1y"
) -> Dict[str, Any]:
    """
    Analyze a portfolio of stocks
    
    Args:
        symbols: List of stock ticker symbols
        weights: List of portfolio weights (must sum to 1.0)
        period: Time period for analysis
        
    Returns:
        Dict containing portfolio analysis
    """
    try:
        if not symbols:
            return {"error": "No symbols provided"}
        
        if len(symbols) > 20:
            return {"error": "Maximum 20 symbols allowed in portfolio"}
        
        symbols = [validate_symbol(s) for s in symbols]
        
        if weights:
            if len(weights) != len(symbols):
                return {"error": "Number of weights must match number of symbols"}
            if abs(sum(weights) - 1.0) > 0.01:
                return {"error": "Weights must sum to 1.0"}
        else:
            weights = [1.0 / len(symbols)] * len(symbols)  # Equal weighting
        
        period = validate_period(period)
        
        # Get data for all symbols
        returns_data = {}
        prices_data = {}
        
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": f"No data available for {symbol}"}
            
            returns_data[symbol] = calculate_returns(hist['Close'])
            prices_data[symbol] = hist['Close']
        
        # Create aligned returns dataframe
        returns_df = pd.DataFrame(returns_data).dropna()
        
        if returns_df.empty:
            return {"error": "No overlapping data found for portfolio analysis"}
        
        # Calculate portfolio returns
        portfolio_returns = (returns_df * weights).sum(axis=1)
        
        # Portfolio metrics
        portfolio_vol = calculate_volatility(portfolio_returns)
        portfolio_sharpe = calculate_sharpe_ratio(portfolio_returns)
        
        # Individual stock metrics
        individual_metrics = {}
        for i, symbol in enumerate(symbols):
            stock_returns = returns_df[symbol]
            individual_metrics[symbol] = {
                "weight": round(weights[i] * 100, 2),
                "volatility": round(calculate_volatility(stock_returns) * 100, 2),
                "sharpe_ratio": round(calculate_sharpe_ratio(stock_returns), 2),
                "contribution_to_return": round(stock_returns.mean() * weights[i] * 252 * 100, 2)
            }
        
        # Correlation matrix
        correlation_matrix = returns_df.corr().round(3).to_dict()
        
        return {
            "symbols": symbols,
            "weights": [round(w * 100, 2) for w in weights],
            "period": period,
            "portfolio_metrics": {
                "annual_return": round(portfolio_returns.mean() * 252 * 100, 2),
                "volatility": round(portfolio_vol * 100, 2),
                "sharpe_ratio": round(portfolio_sharpe, 2),
                "max_drawdown": round((portfolio_returns.cumsum().expanding().max() - portfolio_returns.cumsum()).max() * 100, 2)
            },
            "individual_metrics": individual_metrics,
            "correlation_matrix": correlation_matrix,
            "diversification_ratio": round(1 / np.sqrt(np.dot(weights, np.dot(returns_df.cov().values, weights))) * np.sqrt(np.dot(weights**2, np.diag(returns_df.cov()))), 2),
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_market_indices(
    indices: List[str] = None
) -> Dict[str, Any]:
    """
    Get current data for major market indices
    
    Args:
        indices: List of index symbols (default: major US indices)
        
    Returns:
        Dict containing market indices data
    """
    try:
        if indices is None:
            indices = ['^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX']  # S&P 500, Dow, NASDAQ, Russell 2000, VIX
        
        indices_data = {}
        
        for index in indices:
            try:
                ticker = yf.Ticker(index)
                hist = ticker.history(period='5d')  # Last 5 days
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change = current_price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close != 0 else 0
                    
                    indices_data[index] = {
                        "name": {
                            '^GSPC': 'S&P 500',
                            '^DJI': 'Dow Jones',
                            '^IXIC': 'NASDAQ',
                            '^RUT': 'Russell 2000',
                            '^VIX': 'VIX'
                        }.get(index, index),
                        "value": round(current_price, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_pct, 2),
                        "last_updated": datetime.now().isoformat()
                    }
                else:
                    indices_data[index] = {"error": "No data available"}
                    
            except Exception as e:
                indices_data[index] = {"error": str(e)}
        
        # Market sentiment based on indices
        market_sentiment = "Neutral"
        positive_count = sum(1 for data in indices_data.values() 
                           if isinstance(data, dict) and data.get('change_percent', 0) > 0)
        
        if positive_count >= len(indices_data) * 0.7:
            market_sentiment = "Positive"
        elif positive_count <= len(indices_data) * 0.3:
            market_sentiment = "Negative"
        
        return {
            "indices": indices_data,
            "market_sentiment": market_sentiment,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting market indices: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def search_stocks(
    query: str,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search for stocks by company name or symbol
    
    Args:
        query: Search query (company name or partial symbol)
        max_results: Maximum number of results to return
        
    Returns:
        Dict containing search results
    """
    try:
        if not query or len(query) < 2:
            return {"error": "Query must be at least 2 characters long"}
        
        if max_results > 50:
            max_results = 50
        
        # This is a simplified search - in a real implementation,
        # you might want to integrate with a proper stock search API
        # For now, we'll try to get info for the query as a symbol
        
        query_upper = query.upper()
        results = []
        
        # Try exact symbol match first
        try:
            ticker = yf.Ticker(query_upper)
            info = ticker.info
            
            if info and info.get('symbol'):
                results.append({
                    "symbol": info.get('symbol', query_upper),
                    "name": info.get('longName', 'N/A'),
                    "sector": info.get('sector', 'N/A'),
                    "market_cap": info.get('marketCap'),
                    "current_price": info.get('currentPrice'),
                    "match_type": "exact_symbol"
                })
        except:
            pass
        
        # For a more comprehensive search, you would integrate with:
        # - Yahoo Finance search API
        # - Alpha Vantage symbol search
        # - IEX Cloud symbol search
        # - Or maintain your own symbol database
        
        return {
            "query": query,
            "results": results[:max_results],
            "total_results": len(results),
            "search_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching stocks: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        logger.info("Starting Finance MCP Server...")
        logger.info("Press Ctrl+C to stop")
        mcp.run()  # ✅ Direct FastMCP run
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
