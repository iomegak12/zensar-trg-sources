# Products Library

A Python library for managing product information with SQLite backend.

## Project Structure

```
product_management/
├── __init__.py          # Package initialization
├── config.py            # Configuration management
├── models.py            # Product data models
├── database.py          # Database operations
└── products_library.py  # Main library interface
```

## Features

- Complete CRUD operations for products
- SQLite database backend
- Product information management including:
  - Product ID (format: PROD-XXXX)
  - Title and Description
  - Stock management (units in stock)
  - Pricing (unit price, item discount)
  - Warehouse assignment
  - Active status tracking

## Requirements

- Python 3.11+
- python-dotenv

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create your `.env` file from the example:
   ```bash
   copy .env.example .env
   ```

## Configuration

Edit the `.env` file to configure:
- `DATABASE_PATH`: Path to SQLite database file
- `ENVIRONMENT`: Development/Production environment
- `API_NAME`: Name of the API
- `API_DESCRIPTION`: Description of the API

## Usage

```python
from product_management import ProductsLibrary

# Initialize the library
products = ProductsLibrary()

# Add a new product
products.add_product(
    product_id="PROD-0001",
    title="Samsung Galaxy S24",
    description="Latest flagship smartphone",
    units_in_stock=100,
    unit_price=79999.00,
    item_discount=10.0,
    warehouse_name="Mumbai Warehouse",
    active=True
)

# Get a product
product = products.get_product("PROD-0001")

# Update a product
products.update_product("PROD-0001", units_in_stock=95)

# List all products
all_products = products.list_products()

# Search products
results = products.search_products(query="Samsung")

# Delete a product
products.delete_product("PROD-0001")
```

## Advanced Usage

```python
from product_management import ProductsLibrary
from product_management.models import Product
from product_management.config import config

# Check configuration
print(f"Environment: {config.environment}")
print(f"Database: {config.database_path}")

# Initialize with custom database path
products = ProductsLibrary(db_path="custom/path/products.db")

# Get products by warehouse
warehouse_products = products.get_products_by_warehouse("Mumbai Warehouse")

# Get low stock items
low_stock = products.get_low_stock_products(threshold=20)
```

## Sample Data

Load sample data with 50 Indian electronic products:

```bash
python load_data.py
```

## MCP Server

This library includes a FastMCP server implementation for Model Context Protocol integration.

### Starting the MCP Server

```bash
python run_mcp_server.py
```

The server will start on `http://0.0.0.0:50000/mcp/` using Streamable HTTP transport.

### MCP Server Features

**Resources:**
- `product://sample` - Sample product data
- `product://database/schema` - Database schema information
- `product://warehouses` - List of available warehouses

**Prompts:**
- `add-product` - Template for adding products
- `search-products` - Template for searching products
- `low-stock-alert` - Template for checking low stock

**Tools:**
- `add_product` - Add a new product
- `get_product` - Get product by ID
- `get_all_products` - List all products
- `search_products` - Search products by title/description
- `update_product` - Update product information
- `delete_product` - Delete a product
- `get_products_by_warehouse` - Get products by warehouse
- `get_low_stock_products` - Get low stock products
- `get_product_statistics` - Get database statistics

### MCP Server Configuration

Configure the server in `.env`:
```
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=50000
LOAD_SAMPLE_DATA=false
```

Or use command-line arguments:
```bash
python run_mcp_server.py --host 127.0.0.1 --port 50000
```

## Docker Deployment

### Using Docker Compose (Recommended)

Build and start the server:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop the server:
```bash
docker-compose down
```

Stop and remove volumes:
```bash
docker-compose down -v
```

### Using Docker

Build the image:
```bash
docker build -t products-mcp-server .
```

Run the container:
```bash
docker run -d \
  --name products-mcp-server \
  -p 50000:50000 \
  -v products-data:/app/dbs \
  products-mcp-server
```

View logs:
```bash
docker logs -f products-mcp-server
```

Stop the container:
```bash
docker stop products-mcp-server
docker rm products-mcp-server
```

### Docker Features

- ✅ **Multi-stage build** for smaller image size
- ✅ **Alpine Linux** base (minimal footprint)
- ✅ **Non-root user** for security
- ✅ **Health checks** for monitoring
- ✅ **Persistent volumes** for database
- ✅ **Optimized layers** for faster builds

## License

MIT License - see LICENSE file for details
