#!/usr/bin/env python3
"""
Finance MCP Client
Client for connecting to the Finance MCP Server using proper MCP protocol
"""

import asyncio
import json
import logging
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os
from pathlib import Path

# MCP imports
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPResponse:
    """Data class for MCP responses"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class FinanceMCPClient:
    """Client for Finance MCP Server using proper MCP protocol"""
    
    def __init__(self, server_path: str = "server.py", server_dir: Optional[str] = None):
        self.server_path = server_path
        self.server_dir = server_dir or os.getcwd()
        self.session: Optional[ClientSession] = None
        self.is_connected = False
        
        # Setup server parameters
        self.server_params = StdioServerParameters(
            command="uv",
            args=["--directory", str(Path(self.server_dir).absolute()), "run", self.server_path],
            env=dict(os.environ)
        )
        
    async def connect(self) -> bool:
        """Connect to the MCP server"""
        try:
            # Create stdio client session
            self.session = await stdio_client(self.server_params)
            
            # Initialize the session
            await self.session.initialize()
            
            self.is_connected = True
            logger.info("Connected to Finance MCP Server")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to server: {str(e)}")
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.close()
            self.session = None
        self.is_connected = False
        logger.info("Disconnected from Finance MCP Server")
    
    async def list_tools(self) -> List[types.Tool]:
        """List available tools from the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        response = await self.session.list_tools()
        return response.tools
    
    async def call_tool(self, tool_name: str, **kwargs) -> MCPResponse:
        """Call a tool on the MCP server"""
        if not self.session:
            return MCPResponse(False, {}, "Not connected to server")
        
        try:
            # Create MCP tool call request
            request = types.CallToolRequest(
                name=tool_name,
                arguments=kwargs
            )
            
            # Call the tool
            response = await self.session.call_tool(request)
            
            # Process response
            if response.content:
                # Extract data from response content
                if len(response.content) > 0:
                    content = response.content[0]
                    if hasattr(content, 'text'):
                        # Try to parse as JSON
                        try:
                            data = json.loads(content.text)
                            return MCPResponse(True, data)
                        except json.JSONDecodeError:
                            # If not JSON, return as text
                            return MCPResponse(True, {"result": content.text})
                    else:
                        return MCPResponse(True, {"content": str(content)})
            
            return MCPResponse(True, {"result": "Success"})
            
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {str(e)}")
            return MCPResponse(False, {}, str(e))
    
    async def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        if not self.session:
            return {"error": "Not connected to server"}
        
        try:
            # Get server capabilities
            info = {
                "connected": self.is_connected,
                "server_params": {
                    "command": self.server_params.command,
                    "args": self.server_params.args,
                }
            }
            
            # List available tools
            try:
                tools = await self.list_tools()
                info["available_tools"] = [tool.name for tool in tools]
                info["tool_count"] = len(tools)
            except Exception as e:
                info["tools_error"] = str(e)
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    # Convenience methods for each tool
    async def get_stock_price(self, symbol: str, period: str = "1mo") -> MCPResponse:
        """Get stock price data"""
        return await self.call_tool("get_stock_price", symbol=symbol, period=period)
    
    async def get_volatility_analysis(self, symbol: str, period: str = "1y") -> MCPResponse:
        """Get volatility analysis"""
        return await self.call_tool("get_volatility_analysis", symbol=symbol, period=period)
    
    async def get_trend_analysis(self, symbol: str, period: str = "6mo") -> MCPResponse:
        """Get trend analysis"""
        return await self.call_tool("get_trend_analysis", symbol=symbol, period=period)
    
    async def get_risk_analysis(self, symbol: str, period: str = "1y", benchmark: str = "^GSPC") -> MCPResponse:
        """Get risk analysis"""
        return await self.call_tool("get_risk_analysis", symbol=symbol, period=period, benchmark=benchmark)
    
    async def compare_stocks(self, symbols: List[str], period: str = "1y", metrics: List[str] = None) -> MCPResponse:
        """Compare multiple stocks"""
        return await self.call_tool("compare_stocks", symbols=symbols, period=period, metrics=metrics)
    
    async def get_financial_summary(self, symbol: str) -> MCPResponse:
        """Get financial summary"""
        return await self.call_tool("get_financial_summary", symbol=symbol)
    
    async def get_portfolio_analysis(self, symbols: List[str], weights: List[float] = None, period: str = "1y") -> MCPResponse:
        """Get portfolio analysis"""
        return await self.call_tool("get_portfolio_analysis", symbols=symbols, weights=weights, period=period)
    
    async def get_market_indices(self, indices: List[str] = None) -> MCPResponse:
        """Get market indices data"""
        return await self.call_tool("get_market_indices", indices=indices)
    
    async def search_stocks(self, query: str, max_results: int = 10) -> MCPResponse:
        """Search for stocks"""
        return await self.call_tool("search_stocks", query=query, max_results=max_results)

# Example usage and testing
async def test_client():
    """Test the MCP client functionality"""
    # Adjust paths as needed for your setup
    server_dir = os.getcwd()  # Current directory
    client = FinanceMCPClient(server_path="server.py", server_dir=server_dir)
    
    try:
        # Connect to server
        print("🔄 Connecting to Finance MCP Server...")
        if not await client.connect():
            print("❌ Failed to connect to server")
            print("   Make sure server.py is in the current directory")
            print("   and uv is installed")
            return
        
        print("✅ Connected successfully!")
        print("\n=== Finance MCP Client Test ===\n")
        
        # Get server info
        print("📋 Server Information:")
        server_info = await client.get_server_info()
        for key, value in server_info.items():
            print(f"   {key}: {value}")
        print()
        
        # List available tools
        try:
            tools = await client.list_tools()
            print(f"🛠️  Available Tools ({len(tools)}):")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            print()
        except Exception as e:
            print(f"❌ Error listing tools: {e}")
        
        # Test stock price
        print("1. Testing get_stock_price for AAPL...")
        response = await client.get_stock_price("AAPL", "1mo")
        if response.success:
            data = response.data
            if 'error' not in data:
                print(f"   ✅ Symbol: {data.get('symbol')}")
                print(f"   ✅ Current Price: ${data.get('current_price')}")
                print(f"   ✅ Change: {data.get('change')} ({data.get('change_percent', 0):.2f}%)")
            else:
                print(f"   ⚠️  {data['error']}")
        else:
            print(f"   ❌ Error: {response.error}")
        
        print()
        
        # Test stock comparison
        print("2. Testing compare_stocks for AAPL and MSFT...")
        response = await client.compare_stocks(["AAPL", "MSFT"], "6mo")
        if response.success:
            data = response.data
            if 'error' not in data:
                comparison = data.get('comparison', {})
                for symbol, metrics in comparison.items():
                    if 'error' not in metrics:
                        print(f"   ✅ {symbol}: ${metrics.get('current_price')} (Return: {metrics.get('total_return')}%)")
                    else:
                        print(f"   ⚠️  {symbol}: {metrics['error']}")
            else:
                print(f"   ⚠️  {data['error']}")
        else:
            print(f"   ❌ Error: {response.error}")
        
        print()
        
        # Test market indices
        print("3. Testing get_market_indices...")
        response = await client.get_market_indices()
        if response.success:
            data = response.data
            if 'error' not in data:
                indices = data.get('indices', {})
                for index, info in list(indices.items())[:3]:  # Show first 3
                    if 'error' not in info:
                        print(f"   ✅ {info.get('name', index)}: {info.get('value')} ({info.get('change_percent', 0):+.2f}%)")
            else:
                print(f"   ⚠️  {data['error']}")
        else:
            print(f"   ❌ Error: {response.error}")
        
        print()
        print("🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🔄 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected")

async def interactive_test():
    """Interactive test mode"""
    server_dir = input("Enter server directory (or press Enter for current): ").strip() or os.getcwd()
    client = FinanceMCPClient(server_path="server.py", server_dir=server_dir)
    
    try:
        if not await client.connect():
            print("Failed to connect")
            return
        
        print("Connected! Available commands:")
        print("- price <symbol> [period]")
        print("- compare <symbol1,symbol2,...> [period]")
        print("- indices")
        print("- tools")
        print("- quit")
        
        while True:
            try:
                cmd = input("\n> ").strip().split()
                if not cmd:
                    continue
                
                if cmd[0] == "quit":
                    break
                elif cmd[0] == "price":
                    if len(cmd) < 2:
                        print("Usage: price <symbol> [period]")
                        continue
                    symbol = cmd[1].upper()
                    period = cmd[2] if len(cmd) > 2 else "1mo"
                    
                    response = await client.get_stock_price(symbol, period)
                    if response.success:
                        print(json.dumps(response.data, indent=2))
                    else:
                        print(f"Error: {response.error}")
                
                elif cmd[0] == "compare":
                    if len(cmd) < 2:
                        print("Usage: compare <symbol1,symbol2,...> [period]")
                        continue
                    symbols = [s.strip().upper() for s in cmd[1].split(',')]
                    period = cmd[2] if len(cmd) > 2 else "1y"
                    
                    response = await client.compare_stocks(symbols, period)
                    if response.success:
                        print(json.dumps(response.data, indent=2))
                    else:
                        print(f"Error: {response.error}")
                
                elif cmd[0] == "indices":
                    response = await client.get_market_indices()
                    if response.success:
                        print(json.dumps(response.data, indent=2))
                    else:
                        print(f"Error: {response.error}")
                
                elif cmd[0] == "tools":
                    tools = await client.list_tools()
                    for tool in tools:
                        print(f"- {tool.name}: {tool.description}")
                
                else:
                    print("Unknown command")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    finally:
        await client.disconnect()

def main():
    """Main function for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Finance MCP Client")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--server-dir", help="Server directory path")
    
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_test())
    else:
        asyncio.run(test_client())

if __name__ == "__main__":
    main()
