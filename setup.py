#!/usr/bin/env python3
"""
Setup script for Finance MCP project
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a shell command with description"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True, result.stdout
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False, str(e)

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print(f"❌ Python 3.9+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check if uv is installed
    success, _ = run_command("uv --version", "Checking uv installation", check=False)
    if not success:
        print("❌ uv not found. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    return True

def setup_project():
    """Set up the project"""
    print("\n🚀 Setting up Finance MCP project...")
    
    # Install dependencies
    success, _ = run_command("uv sync", "Installing dependencies")
    if not success:
        return False
    
    # Create necessary directories
    dirs = ["tests", "docs", "examples", "data"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 Created directory: {dir_name}")
    
    return True

def create_claude_config():
    """Create Claude Desktop configuration"""
    print("\n⚙️  Setting up Claude Desktop configuration...")
    
    current_dir = os.getcwd()
    
    config = {
        "mcpServers": {
            "finance-server": {
                "command": "uv",
                "args": [
                    "--directory", current_dir,
                    "run", "python", "server.py"
                ],
                "env": {
                    "PYTHONPATH": current_dir,
                    "LOG_LEVEL": "INFO"
                }
            }
        },
        "allowedMCPServers": ["finance-server"],
        "mcpSettings": {
            "finance-server": {
                "enabled": True,
                "timeout": 30000,
                "maxRetries": 3,
                "retryDelay": 1000
            }
        }
    }
    
    # Write config file
    config_file = "claude_desktop_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created {config_file}")
    print(f"📝 Copy this configuration to your Claude Desktop settings")
    print(f"   Location varies by OS:")
    print(f"   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print(f"   - Windows: %APPDATA%/Claude/claude_desktop_config.json")
    print(f"   - Linux: ~/.config/Claude/claude_desktop_config.json")
    
    return True

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running tests...")
    
    success, output = run_command("uv run python test_integration.py", "Running integration tests")
    if success:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed - this might be normal if you don't have internet connection")
    
    return True

def create_example_scripts():
    """Create example scripts"""
    print("\n📝 Creating example scripts...")
    
    # Basic usage example
    basic_example = '''#!/usr/bin/env python3
"""
Basic usage example for Finance MCP
"""

import asyncio
from client import FinanceMCPClient

async def main():
    """Basic example"""
    client = FinanceMCPClient()
    
    try:
        # Connect
        if not await client.connect():
            print("Failed to connect")
            return
        
        # Get stock price
        response = await client.get_stock_price("AAPL")
        if response.success:
            data = response.data
            print(f"AAPL: ${data.get('current_price')} ({data.get('change_percent'):+.2f}%)")
        
        # Compare stocks
        response = await client.compare_stocks(["AAPL", "MSFT", "GOOGL"])
        if response.success:
            for symbol, metrics in response.data.get("comparison", {}).items():
                if "error" not in metrics:
                    print(f"{symbol}: {metrics.get('total_return'):+.2f}% return")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open("examples/basic_usage.py", "w") as f:
        f.write(basic_example)
    print("✅ Created examples/basic_usage.py")
    
    # Portfolio analysis example
    portfolio_example = '''#!/usr/bin/env python3
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
            
            print("\\nPortfolio Metrics:")
            print(f"  Annual Return: {portfolio_metrics.get('annual_return')}%")
            print(f"  Volatility: {portfolio_metrics.get('volatility')}%")
            print(f"  Sharpe Ratio: {portfolio_metrics.get('sharpe_ratio')}")
            print(f"  Max Drawdown: {portfolio_metrics.get('max_drawdown')}%")
            
            print("\\nIndividual Holdings:")
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
'''
    
    with open("examples/portfolio_analysis.py", "w") as f:
        f.write(portfolio_example)
    print("✅ Created examples/portfolio_analysis.py")
    
    return True

def main():
    """Main setup function"""
    print("🏦 Finance MCP Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup project
    if not setup_project():
        print("❌ Project setup failed")
        sys.exit(1)
    
    # Create Claude config
    if not create_claude_config():
        print("❌ Claude config creation failed")
        sys.exit(1)
    
    # Create examples
    if not create_example_scripts():
        print("❌ Example creation failed")
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy claude_desktop_config.json to your Claude Desktop settings")
    print("2. Restart Claude Desktop")
    print("3. Test the server: uv run python server.py")
    print("4. Test the client: uv run python client.py")
    print("5. Run the main app: uv run python main.py")
    print("6. Try examples: uv run python examples/basic_usage.py")
    
    print("\nUseful commands:")
    print("- uv run python server.py          # Start MCP server")
    print("- uv run python client.py          # Test client")
    print("- uv run python client.py -i       # Interactive client")
    print("- uv run python main.py            # Full application")
    print("- uv run python test_integration.py # Run tests")

if __name__ == "__main__":
    main()
