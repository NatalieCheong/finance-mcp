# Finance MCP - Professional Financial Analysis System

A comprehensive financial analysis system built using the Model Context Protocol (MCP) with Claude Desktop integration. Get real-time stock data, risk analysis, portfolio optimization, and market insights directly through Claude's AI interface.

![Finance MCP Demo](https://img.shields.io/badge/MCP-Compatible-blue) ![Python](https://img.shields.io/badge/Python-3.10+-green) ![FastMCP](https://img.shields.io/badge/FastMCP-2.11+-orange)

## 🚀 Live Demo Results

Here's what the system delivers through Claude Desktop:

### 📈 Real-Time Stock Analysis
![AAPL Stock Price Analysis](./images/aapl-stock-price.png)
- **AAPL Current Price**: $233.33 (+$3.68, +1.6%)
- **Volume**: 69.6 million shares
- **52-Week Range**: $201.27 - $234.99
- **Real-time data** directly from yfinance

### 📊 Multi-Stock Comparison
![Stock Comparison](./images/stock-comparison.png)
- **AAPL vs MSFT vs GOOGL (1-Year Performance)**
- **Google (GOOGL)**: 26.54% return - **Best performer** 🏆
- **Microsoft (MSFT)**: 25.84% return with lowest volatility
- **Apple (AAPL)**: 5.73% return but highest volatility

### ⚠️ Advanced Risk Analysis 
![Tesla Volatility Analysis](./images/tesla-volatility.png)
- **Tesla (TSLA) Volatility Metrics**
- **Annual Volatility**: 71.87% (Very high)
- **30-day Trend**: Decreasing volatility
- **Max Daily Swing**: +29.69% / -18.43%
- **Risk Rating**: Extremely volatile stock

## ✨ Key Features

### 🔧 **9 Professional Financial Tools**
- **`get_stock_price`** - Real-time stock prices and metrics
- **`get_volatility_analysis`** - Risk and volatility calculations
- **`get_trend_analysis`** - Moving averages and momentum
- **`get_risk_analysis`** - VaR, Sharpe ratio, Beta analysis
- **`compare_stocks`** - Multi-stock performance comparison
- **`get_financial_summary`** - Company fundamentals and ratios
- **`get_portfolio_analysis`** - Portfolio optimization metrics
- **`get_market_indices`** - Major market index tracking
- **`search_stocks`** - Stock symbol and company search

### 🎯 **Direct Claude Integration**
- **Zero API Keys Required** - Uses yfinance for free market data
- **Instant Analysis** - Ask Claude natural language questions
- **Professional Reports** - Detailed financial insights
- **Real-Time Data** - Live market prices and calculations

## 📦 Quick Installation

### Prerequisites
- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)** package manager
- **Claude Desktop** application

### 1-Minute Setup
```bash
# Clone and install
git clone https://github.com/NatalieCheong/finance-mcp.git
cd finance-mcp
uv sync

# Run automated setup
uv run python setup.py

# Copy config to Claude Desktop
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Start the MCP server
uv run python server.py
```

### Configure Claude Desktop
1. Copy the generated config to Claude Desktop settings:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Restart Claude Desktop

3. Test: Ask Claude **"What MCP tools are available?"**

## 🎯 Usage Examples

### Natural Language Queries
```
"Get the current price of Apple stock"
"Compare AAPL, MSFT, and GOOGL performance"
"Analyze Tesla's volatility over the past year"
"What's the risk profile of my portfolio: 40% AAPL, 35% MSFT, 25% GOOGL?"
"Show me the current market sentiment based on major indices"
```

### Advanced Analysis
```
"Calculate the Sharpe ratio for NVIDIA over the past 2 years"
"What's the beta of Tesla compared to the S&P 500?"
"Analyze the correlation between Apple and Microsoft stocks"
"Get me a comprehensive financial summary of Amazon"
```

## 🏗️ Project Structure

```
finance-mcp/
├── 📄 server.py              # MCP Server with 9 financial tools
├── 🔧 client.py              # MCP Client for testing
├── 🖥️  main.py               # Interactive CLI application
├── 🚀 run.py                 # Convenient launcher script
├── ⚙️  setup.py              # Automated setup script
├── 🧪 test_integration.py    # Test suite
├── 📋 claude_desktop_config.json  # Claude Desktop configuration
├── 📦 pyproject.toml         # Project configuration
├── 📚 requirements.txt       # Dependencies
├── 📖 README.md             # Documentation
├── examples/                # Usage examples
│   ├── basic_usage.py
│   └── portfolio_analysis.py
└── standalone_app.py # Standalone version (no MCP needed)
└── simple_client.py
```

## 💼 Professional Financial Calculations

### Risk Metrics
- **Value at Risk (VaR)** - 1% and 5% confidence levels
- **Sharpe Ratio** - Risk-adjusted returns
- **Beta Analysis** - Market correlation and sensitivity
- **Maximum Drawdown** - Worst-case scenario analysis
- **Volatility Analysis** - Daily, monthly, and annual volatility

### Portfolio Analytics
- **Modern Portfolio Theory** - Efficient frontier calculations
- **Correlation Analysis** - Asset correlation matrices
- **Diversification Metrics** - Portfolio diversification ratios
- **Performance Attribution** - Individual asset contributions
- **Risk-Return Optimization** - Optimal weight calculations

### Market Analysis
- **Technical Indicators** - Moving averages, momentum, trends
- **Fundamental Ratios** - P/E, P/B, debt-to-equity, ROE
- **Market Indices** - S&P 500, Dow Jones, NASDAQ tracking
- **Sector Analysis** - Industry-specific comparisons

## 🛠️ Development & Testing

### Run Tests
```bash
# Integration tests
uv run python test_integration.py

# Simple functionality tests
uv run python simple_client.py

# Test specific tools
uv run python run.py test
```

### Standalone Usage (No Claude Desktop)
```bash
# Interactive financial analysis app
uv run python standalone_app.py

# Command-line quick analysis
uv run python main.py --symbol AAPL --analysis price
```

### Development Mode
```bash
# Start server in development
uv run python server.py

# Interactive client testing
uv run python client.py -i

# Check system status
uv run python run.py status
```

## 📊 Data Sources & Reliability

- **Market Data**: Yahoo Finance via yfinance library
- **Update Frequency**: Real-time during market hours
- **Historical Data**: Up to 10+ years of historical prices
- **Global Markets**: US, European, and Asian stock exchanges
- **Data Quality**: Professional-grade financial data used by millions

## 🔒 Security & Compliance

- **No API Keys Required** - Uses public market data
- **Local Processing** - All calculations performed locally
- **No Data Storage** - Real-time analysis without data persistence
- **Privacy First** - No user data collection or tracking
- **Open Source** - Full transparency and auditability

## 🚀 Advanced Features

### Custom Analysis Workflows
- Multi-timeframe analysis (1D to 10Y)
- Sector-based comparisons
- Custom portfolio weightings
- Batch processing multiple stocks
- Export results to JSON

### Integration Options
- **Claude Desktop** - Natural language interface
- **CLI Application** - Command-line usage
- **Python API** - Direct programmatic access
- **Standalone App** - No dependencies required

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Add tests for new financial tools
- Follow existing code patterns
- Update documentation for new features
- Ensure all tests pass before submitting

## 📈 Performance Benchmarks

- **Response Time**: < 2 seconds for most queries
- **Concurrent Users**: Supports multiple Claude Desktop instances
- **Memory Usage**: < 100MB typical operation
- **Data Accuracy**: Professional-grade financial calculations
- **Uptime**: 99.9%+ reliability with proper setup

## 🆘 Troubleshooting

### Common Issues

**"MCP server not detected"**
```bash
# Check config location and restart Claude Desktop
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**"No data found for symbol"**
- Verify stock symbol is correct (use search_stocks tool)
- Check market hours and trading status
- Ensure internet connection is stable

**"Server connection failed"**
```bash
# Test server manually
uv run python server.py

# Check system status
uv run python run.py status
```

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/NatalieCheong/finance-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NatalieCheong/finance-mcp/discussions)
- **Documentation**: [MCP Documentation](https://modelcontextprotocol.io/)
- **GitHub**: [MCP GitHub](https://github.com/modelcontextprotocol)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[FastMCP](https://github.com/jlowin/fastmcp)** - Excellent MCP framework
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Reliable financial data
- **[Anthropic](https://anthropic.com)** - Model Context Protocol and Claude
- **[uv](https://github.com/astral-sh/uv)** - Modern Python package management

---

## 🎯 Live Results

*Screenshots above show real Claude Desktop integration with live financial data - no mock data or simulations!*

**Ready to analyze the markets? Start with:** `"Get me the current price and risk analysis for Tesla"`

🏦 **Finance MCP** - Professional financial analysis.
  "
