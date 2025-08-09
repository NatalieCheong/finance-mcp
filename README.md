# Finance MCP - Comprehensive Financial Analysis System

A powerful financial analysis system built using the Model Context Protocol (MCP) with Claude integration. This project provides comprehensive stock analysis, portfolio management, and risk assessment tools through a clean MCP interface.

## 🚀 Features

### Core Financial Tools
- **📈 Stock Price Analysis** - Real-time and historical price data
- **📊 Volatility Analysis** - Comprehensive volatility metrics and trends
- **📈 Trend Analysis** - Moving averages and momentum indicators
- **⚠️ Risk Analysis** - VaR, Sharpe ratio, Beta, and risk ratings
- **🔍 Stock Comparison** - Multi-stock comparative analysis
- **📋 Financial Summary** - Company fundamentals and key ratios
- **💼 Portfolio Analysis** - Portfolio optimization and risk assessment
- **🏛️ Market Indices** - Major market index tracking
- **🔍 Stock Search** - Find stocks by name or symbol
- **📊 Custom Analysis** - Advanced analytical tools

### Technical Features
- **MCP Integration** - Built on Model Context Protocol for Claude
- **Async Architecture** - High-performance async/await implementation
- **Robust Guardrails** - Input validation and rate limiting
- **Error Handling** - Comprehensive error management
- **Data Export** - JSON export capabilities
- **Batch Processing** - Multi-stock analysis
- **Interactive CLI** - User-friendly command-line interface

## 📦 Installation

### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- Claude Desktop (for MCP integration)

### Quick Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd finance-mcp
```

2. **Install dependencies with uv**
```bash
uv sync
```

3. **Configure Claude Desktop**
Update your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "finance-server": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/your/finance-mcp-project"
    }
  }
}
```

4. **Run the system**
```bash
# Start MCP server
uv run python server.py

# Run interactive client (in another terminal)
uv run python main.py

# Or run specific analysis
uv run python main.py --symbol AAPL --analysis price
```

## 🏗️ Project Structure

```
finance-mcp/
├── server.py              # MCP Server with financial tools
├── client.py              # MCP Client for server communication
├── main.py                # Interactive CLI application
├── claude_desktop_config.json  # Claude Desktop configuration
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_client.py
│   └── test_integration.py
├── docs/                  # Documentation
│   ├── api.md
│   ├── usage.md
│   └── examples.md
└── examples/              # Usage examples
    ├── basic_analysis.py
    ├── portfolio_optimization.py
    └── risk_assessment.py
```

## 🛠️ Usage

### MCP Tools Available

#### 1. get_stock_price
```python
# Get current stock price and basic metrics
response = await client.get_stock_price("AAPL", period="1mo")
```

#### 2. get_volatility_analysis
```python
# Analyze stock volatility
response = await client.get_volatility_analysis("AAPL", period="1y")
```

#### 3. get_trend_analysis
```python
# Analyze price trends and moving averages
response = await client.get_trend_analysis("AAPL", period="6mo")
```

#### 4. get_risk_analysis
```python
# Comprehensive risk metrics
response = await client.get_risk_analysis("AAPL", period="1y", benchmark="^GSPC")
```

#### 5. compare_stocks
```python
# Compare multiple stocks
response = await client.compare_stocks(["AAPL", "MSFT", "GOOGL"], period="1y")
```

#### 6. get_financial_summary
```python
# Get company fundamentals
response = await client.get_financial_summary("AAPL")
```

#### 7. get_portfolio_analysis
```python
# Analyze portfolio performance
symbols = ["AAPL", "MSFT", "GOOGL"]
weights = [0.4, 0.35, 0.25]
response = await client.get_portfolio_analysis(symbols, weights, period="1y")
```

#### 8. get_market_indices
```python
# Get major market indices
response = await client.get_market_indices()
```

#### 9. search_stocks
```python
# Search for stocks
response = await client.search_stocks("Apple", max_results=10)
```

### Interactive CLI Usage

Run the interactive application:
```bash
uv run python main.py
```

This provides a menu-driven interface with all available tools and custom analysis options.

### Command Line Usage

For quick analysis:
```bash
# Get stock price
uv run python main.py --symbol AAPL --analysis price

# Volatility analysis
uv run python main.py --symbol MSFT --analysis volatility

# Trend analysis
uv run python main.py --symbol GOOGL --analysis trend

# Risk analysis
uv run python main.py --symbol TSLA --analysis risk
```

## 🔒 Guardrails and Validation

The system includes comprehensive guardrails:

- **Symbol Validation** - Ensures proper ticker format
- **Date Range Validation** - Prevents invalid date ranges
- **Rate Limiting** - Protects against excessive API calls
- **Data Validation** - Validates all input parameters
- **Error Handling** - Graceful error management
- **Input Sanitization** - Prevents malicious inputs

## 📊 Example Outputs

### Stock Price Analysis
```json
{
  "symbol": "AAPL",
  "current_price": 193.42,
  "previous_close": 191.75,
  "change": 1.67,
  "change_percent": 0.87,
  "volume": 45234567,
  "high_52w": 199.62,
  "low_52w": 164.08,
  "currency": "USD"
}
```

### Risk Analysis
```json
{
  "symbol": "AAPL",
  "volatility_annual": 28.45,
  "sharpe_ratio": 1.23,
  "beta": 1.15,
  "var_5_percent": -2.34,
  "max_drawdown": -15.67,
  "
