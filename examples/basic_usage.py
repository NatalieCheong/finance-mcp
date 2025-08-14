#!/usr/bin/env python3
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

