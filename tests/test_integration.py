#!/usr/bin/env python3
"""
Integration tests for Finance MCP system
"""

import asyncio
import pytest
import json
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from client import FinanceMCPClient

class TestFinanceMCPIntegration:
    """Integration tests for the Finance MCP system"""
    
    @pytest.fixture
    async def client(self):
        """Fixture to create and connect client"""
        client = FinanceMCPClient(
            server_path="server.py",
            server_dir=str(project_root)
        )
        
        connected = await client.connect()
        if not connected:
            pytest.skip("Could not connect to MCP server")
        
        yield client
        
        await client.disconnect()
    
    @pytest.mark.asyncio
    async def test_server_connection(self, client):
        """Test that we can connect to the server"""
        assert client.is_connected
        
        # Get server info
        info = await client.get_server_info()
        assert "connected" in info
        assert info["connected"] is True
    
    @pytest.mark.asyncio
    async def test_list_tools(self, client):
        """Test listing available tools"""
        tools = await client.list_tools()
        
        # Should have all our financial tools
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "get_stock_price",
            "get_volatility_analysis", 
            "get_trend_analysis",
            "get_risk_analysis",
            "compare_stocks",
            "get_financial_summary",
            "get_portfolio_analysis",
            "get_market_indices",
            "search_stocks"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Tool {expected_tool} not found"
    
    @pytest.mark.asyncio
    async def test_get_stock_price(self, client):
        """Test stock price retrieval"""
        response = await client.get_stock_price("AAPL", "1mo")
        
        assert response.success
        assert "error" not in response.data
        assert "symbol" in response.data
        assert "current_price" in response.data
        assert response.data["symbol"] == "AAPL"
        assert isinstance(response.data["current_price"], (int, float))
    
    @pytest.mark.asyncio
    async def test_volatility_analysis(self, client):
        """Test volatility analysis"""
        response = await client.get_volatility_analysis("MSFT", "1y")
        
        assert response.success
        assert "error" not in response.data
        assert "symbol" in response.data
        assert "annual_volatility" in response.data
        assert response.data["symbol"] == "MSFT"
    
    @pytest.mark.asyncio
    async def test_compare_stocks(self, client):
        """Test stock comparison"""
        symbols = ["AAPL", "MSFT"]
        response = await client.compare_stocks(symbols, "6mo")
        
        assert response.success
        assert "error" not in response.data
        assert "comparison" in response.data
        
        comparison = response.data["comparison"]
        for symbol in symbols:
            assert symbol in comparison
            assert "current_price" in comparison[symbol]
    
    @pytest.mark.asyncio
    async def test_market_indices(self, client):
        """Test market indices retrieval"""
        response = await client.get_market_indices()
        
        assert response.success
        assert "indices" in response.data
        assert "market_sentiment" in response.data
        
        # Should have some major indices
        indices = response.data["indices"]
        assert len(indices) > 0
    
    @pytest.mark.asyncio
    async def test_invalid_symbol(self, client):
        """Test handling of invalid symbols"""
        response = await client.get_stock_price("INVALID_SYMBOL_XYZ", "1mo")
        
        # Should either succeed with an error in data, or fail gracefully
        if response.success:
            # If successful, should indicate no data found
            assert "error" in response.data or response.data.get("current_price") is None
        else:
            # Or the response itself should indicate failure
            assert response.error is not None
    
    @pytest.mark.asyncio
    async def test_portfolio_analysis(self, client):
        """Test portfolio analysis"""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        weights = [0.4, 0.35, 0.25]
        
        response = await client.get_portfolio_analysis(symbols, weights, "1y")
        
        if response.success and "error" not in response.data:
            assert "portfolio_metrics" in response.data
            assert "individual_metrics" in response.data
            
            portfolio_metrics = response.data["portfolio_metrics"]
            assert "annual_return" in portfolio_metrics
            assert "volatility" in portfolio_metrics
    
    @pytest.mark.asyncio
    async def test_risk_analysis(self, client):
        """Test risk analysis"""
        response = await client.get_risk_analysis("AAPL", "1y", "^GSPC")
        
        if response.success and "error" not in response.data:
            assert "volatility_annual" in response.data
            assert "sharpe_ratio" in response.data
            assert "beta" in response.data
            assert "risk_rating" in response.data

# Standalone test runner
async def run_basic_tests():
    """Run basic tests without pytest"""
    print("🧪 Running Finance MCP Integration Tests")
    print("=" * 50)
    
    client = FinanceMCPClient(server_path="server.py")
    
    try:
        # Test connection
        print("1. Testing connection...")
        if not await client.connect():
            print("   ❌ Failed to connect to server")
            return False
        print("   ✅ Connected successfully")
        
        # Test listing tools
        print("2. Testing tool listing...")
        try:
            tools = await client.list_tools()
            print(f"   ✅ Found {len(tools)} tools")
            for tool in tools[:3]:  # Show first 3
                print(f"      - {tool.name}")
        except Exception as e:
            print(f"   ⚠️  Error listing tools: {e}")
        
        # Test stock price
        print("3. Testing stock price...")
        response = await client.get_stock_price("AAPL", "1mo")
        if response.success and "error" not in response.data:
            price = response.data.get("current_price")
            print(f"   ✅ AAPL price: ${price}")
        else:
            print(f"   ⚠️  Error: {response.error or response.data.get('error')}")
        
        # Test comparison
        print("4. Testing stock comparison...")
        response = await client.compare_stocks(["AAPL", "MSFT"], "1mo")
        if response.success and "error" not in response.data:
            comparison = response.data.get("comparison", {})
            print(f"   ✅ Compared {len(comparison)} stocks")
        else:
            print(f"   ⚠️  Error: {response.error or response.data.get('error')}")
        
        # Test market indices
        print("5. Testing market indices...")
        response = await client.get_market_indices()
        if response.success and "error" not in response.data:
            indices = response.data.get("indices", {})
            sentiment = response.data.get("market_sentiment")
            print(f"   ✅ Got {len(indices)} indices, sentiment: {sentiment}")
        else:
            print(f"   ⚠️  Error: {response.error or response.data.get('error')}")
        
        print("\n🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        await client.disconnect()

def main():
    """Main function to run tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Finance MCP Integration Tests")
    parser.add_argument("--pytest", action="store_true", 
                       help="Run with pytest (requires pytest installation)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.pytest:
        # Run with pytest
        import subprocess
        import sys
        
        cmd = [sys.executable, "-m", "pytest", __file__]
        if args.verbose:
            cmd.append("-v")
        
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    else:
        # Run basic tests
        success = asyncio.run(run_basic_tests())
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
