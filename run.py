#!/usr/bin/env python3
"""
Finance MCP - Startup Script
Quick launcher for the Finance MCP system
"""

import asyncio
import argparse
import subprocess
import sys
import os
from pathlib import Path

def run_server():
    """Run the MCP server"""
    print("🚀 Starting Finance MCP Server...")
    print("Press Ctrl+C to stop")
    try:
        subprocess.run([sys.executable, "server.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def run_client():
    """Run the client test"""
    print("🔧 Running Finance MCP Client Test...")
    subprocess.run([sys.executable, "client.py"])

def run_client_interactive():
    """Run the client in interactive mode"""
    print("🔧 Running Finance MCP Client (Interactive)...")
    subprocess.run([sys.executable, "client.py", "-i"])

def run_main_app():
    """Run the main application"""
    print("🏦 Starting Finance MCP Application...")
    subprocess.run([sys.executable, "main.py"])

def run_tests():
    """Run integration tests"""
    print("🧪 Running Integration Tests...")
    subprocess.run([sys.executable, "test_integration.py"])

def run_setup():
    """Run setup script"""
    print("⚙️  Running Setup...")
    subprocess.run([sys.executable, "setup.py"])

def run_example(example_name):
    """Run an example script"""
    example_path = f"examples/{example_name}.py"
    if os.path.exists(example_path):
        print(f"📝 Running example: {example_name}")
        subprocess.run([sys.executable, example_path])
    else:
        print(f"❌ Example not found: {example_path}")
        print("Available examples:")
        examples_dir = Path("examples")
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.py"):
                print(f"  - {example_file.stem}")

def quick_analysis(symbol, analysis_type):
    """Run quick analysis"""
    print(f"📊 Quick {analysis_type} analysis for {symbol}...")
    subprocess.run([sys.executable, "main.py", "--symbol", symbol, "--analysis", analysis_type])

def show_status():
    """Show system status"""
    print("📋 Finance MCP System Status")
    print("=" * 40)
    
    # Check if files exist
    files = ["server.py", "client.py", "main.py", "pyproject.toml"]
    for file in files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"{status} {file}")
    
    # Check if uv is available
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv {result.stdout.strip()}")
        else:
            print("❌ uv not available")
    except FileNotFoundError:
        print("❌ uv not installed")
    
    # Check if dependencies are installed
    try:
        result = subprocess.run(["uv", "run", "python", "-c", "import yfinance, pandas, fastmcp"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed")
        else:
            print("❌ Dependencies missing")
    except:
        print("❌ Cannot check dependencies")

def main():
    """Main launcher"""
    parser = argparse.ArgumentParser(description="Finance MCP Launcher", 
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog="""
Examples:
  python run.py server              # Start MCP server
  python run.py client              # Test client
  python run.py app                 # Run main application
  python run.py test                # Run tests
  python run.py quick AAPL price    # Quick price check
  python run.py example basic_usage # Run example
""")
    
    parser.add_argument("command", choices=[
        "server", "client", "client-interactive", "app", "test", "setup", 
        "status", "quick", "example"
    ], help="Command to run")
    
    parser.add_argument("args", nargs="*", help="Additional arguments")
    
    args = parser.parse_args()
    
    if args.command == "server":
        run_server()
    elif args.command == "client":
        run_client()
    elif args.command == "client-interactive":
        run_client_interactive()
    elif args.command == "app":
        run_main_app()
    elif args.command == "test":
        run_tests()
    elif args.command == "setup":
        run_setup()
    elif args.command == "status":
        show_status()
    elif args.command == "quick":
        if len(args.args) >= 2:
            symbol, analysis_type = args.args[0], args.args[1]
            quick_analysis(symbol, analysis_type)
        else:
            print("Usage: python run.py quick <symbol> <analysis_type>")
            print("Analysis types: price, volatility, trend, risk")
    elif args.command == "example":
        if len(args.args) >= 1:
            run_example(args.args[0])
        else:
            print("Usage: python run.py example <example_name>")
            run_example("")  # This will show available examples

if __name__ == "__main__":
    main()
