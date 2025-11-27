"""
MCP Server startup script using Streamable HTTP transport.

Run this script to start the Products Management MCP Server with Streamable HTTP.
"""

import os
import sys
import signal
import argparse
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Flag to track if shutdown has been initiated
shutdown_initiated = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_initiated
    
    if shutdown_initiated:
        print(f"\n{Fore.RED}Force shutdown initiated...{Style.RESET_ALL}")
        sys.exit(1)
    
    shutdown_initiated = True
    signal_name = signal.Signals(signum).name
    print(f"\n\n{Fore.YELLOW}{'=' * 70}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}Received {signal_name} signal - Shutting down gracefully...")
    print(f"{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Cleaning up resources...")
    print(f"{Fore.GREEN}✓ MCP server shutdown complete")
    print(f"{Fore.CYAN}Thank you for using Products Management MCP Server!{Style.RESET_ALL}\n")
    sys.exit(0)

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    from dotenv import load_dotenv
    from mcp_server import mcp
    
    # Register signal handlers for graceful shutdown
    # SIGINT: Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    # SIGTERM: Termination signal
    signal.signal(signal.SIGTERM, signal_handler)
    # SIGBREAK: Ctrl+Break on Windows
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, signal_handler)
    
    # Load environment variables
    load_dotenv()
    
    # Load sample data if configured
    load_sample_data = os.getenv("LOAD_SAMPLE_DATA", "false").lower() == "true"
    if load_sample_data:
        print(f"{Fore.YELLOW}Loading sample data...{Style.RESET_ALL}")
        try:
            # Import and run load_data
            from scripts.load_data import main as load_sample_data_main
            load_sample_data_main()
            print(f"{Fore.GREEN}✓ Sample data loaded successfully{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not load sample data: {e}{Style.RESET_ALL}\n")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Products Management MCP Server")
    parser.add_argument("--host", type=str, default=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
                       help="Host to bind to")
    parser.add_argument("--port", type=int, default=int(os.getenv("MCP_SERVER_PORT", "50000")),
                       help="Port to bind to")
    args = parser.parse_args()
    
    print(f"{Style.BRIGHT}{Fore.MAGENTA}{'=' * 70}")
    print(f"{Style.BRIGHT}{Fore.CYAN}Products Management MCP Server")
    print(f"{Style.BRIGHT}{Fore.MAGENTA}{'=' * 70}")
    print(f"{Fore.GREEN}Server starting on http://{args.host}:{args.port}")
    print(f"\n{Style.BRIGHT}Transport:{Style.RESET_ALL} {Fore.CYAN}Streamable HTTP")
    print(f"{Style.BRIGHT}MCP Endpoint:{Style.RESET_ALL} {Fore.YELLOW}http://{args.host}:{args.port}/mcp/")
    print(f"{Style.BRIGHT}CORS:{Style.RESET_ALL} {Fore.GREEN}Enabled (all origins)")
    print(f"{Fore.MAGENTA}{'=' * 70}")
    
    print(f"\n{Style.BRIGHT}{Fore.BLUE}Available MCP Resources:")
    print(f"  {Fore.CYAN}• product://sample")
    print(f"  {Fore.CYAN}• product://database/schema")
    print(f"  {Fore.CYAN}• product://warehouses")
    
    print(f"\n{Style.BRIGHT}{Fore.BLUE}Available MCP Prompts:")
    print(f"  {Fore.CYAN}• add-product")
    print(f"  {Fore.CYAN}• search-products")
    print(f"  {Fore.CYAN}• low-stock-alert")
    
    print(f"\n{Style.BRIGHT}{Fore.BLUE}Available MCP Tools:")
    tools = [
        "add_product", "get_product", "get_all_products",
        "search_products", "update_product", "delete_product",
        "get_products_by_warehouse", "get_low_stock_products",
        "get_product_statistics"
    ]
    for tool in tools:
        print(f"  {Fore.GREEN}✓ {tool}")
    
    print(f"{Fore.MAGENTA}{'=' * 70}")
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}Transport Details:")
    print(f"  {Style.BRIGHT}Streamable HTTP:")
    print(f"    {Fore.CYAN}• Server-Sent Events (SSE) over HTTP")
    print(f"    {Fore.CYAN}• Stateful sessions with mcp-session-id header")
    print(f"    {Fore.CYAN}• Connect to: {Fore.YELLOW}http://{args.host}:{args.port}/mcp/")
    print(f"    {Style.BRIGHT}• Required headers:")
    print(f"      {Fore.GREEN}* Content-Type: application/json")
    print(f"      {Fore.GREEN}* Accept: application/json, text/event-stream")
    print(f"{Fore.MAGENTA}{'=' * 70}")
    print(f"\n{Style.BRIGHT}{Fore.GREEN}🚀 Starting server...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to shutdown gracefully{Style.RESET_ALL}\n")
    
    try:
        # Run server using FastMCP's run method with streamable-http transport
        # Note: path="/mcp/" with trailing slash is important for proper routing
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            path="/mcp/"
        )
    except KeyboardInterrupt:
        # This will be caught by the signal handler
        pass
    except Exception as e:
        print(f"\n{Fore.RED}Error starting server: {e}{Style.RESET_ALL}")
        sys.exit(1)
