"""
MCP Server for Products Management System using FastMCP.

This module implements an MCP server with Streamable HTTP transport,
exposing product management tools and resources.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP
from product_management import ProductsLibrary

# Load environment variables
load_dotenv()
DB_PATH = os.getenv('DATABASE_PATH', 'dbs/products.db')

# Initialize FastMCP server
mcp = FastMCP("Products Management")

# Initialize Products Library
def get_library():
    """Get products library instance."""
    return ProductsLibrary()


# MCP Resources - Sample Data
@mcp.resource("product://sample")
def get_sample_product() -> str:
    """Sample product data for demonstration."""
    return """
    {
        "product_id": "PROD-0001",
        "title": "Samsung Galaxy S24",
        "description": "Latest flagship smartphone with advanced camera system and powerful processor",
        "units_in_stock": 150,
        "unit_price": 79999.00,
        "item_discount": 10.0,
        "warehouse_name": "Mumbai Central Warehouse",
        "active": true
    }
    """


@mcp.resource("product://database/schema")
def get_database_schema() -> str:
    """Database schema information."""
    return """
    Products Database Schema (SQLAlchemy ORM):
    
    Table: products
    - product_id (String, PRIMARY KEY): Unique product identifier (format: PROD-XXXX)
    - title (String, NOT NULL): Product title/name
    - description (String): Detailed product description
    - units_in_stock (Integer, NOT NULL, default=0): Number of units available
    - unit_price (Float, NOT NULL): Price per unit in INR
    - item_discount (Float, default=0.0): Discount percentage (0-100)
    - warehouse_name (String, NOT NULL): Name of warehouse where product is stored
    - active (Boolean, NOT NULL, default=True): Product activation status
    - created_at (DateTime): Timestamp when product was created
    - updated_at (DateTime): Timestamp when product was last updated
    """


@mcp.resource("product://warehouses")
def get_warehouse_list() -> str:
    """List of available warehouses."""
    return """
    Available Warehouses:
    
    1. Mumbai Central Warehouse
    2. Delhi NCR Hub
    3. Bangalore Tech Park
    4. Hyderabad Distribution Center
    5. Chennai Storage Facility
    6. Pune Logistics Hub
    7. Kolkata Regional Warehouse
    """


# MCP Prompts
@mcp.prompt("add-product")
def add_product_prompt() -> str:
    """Prompt template for adding a new product."""
    return """
    To add a new product, use the add_product tool with the following information:
    
    Required fields:
    - product_id: Unique identifier in format PROD-XXXX (e.g., PROD-0001)
    - title: Product title/name
    - description: Detailed product description
    - units_in_stock: Number of units available (≥ 0)
    - unit_price: Price per unit in INR (> 0)
    - warehouse_name: Name of warehouse
    
    Optional fields:
    - item_discount: Discount percentage 0-100 (default: 0.0)
    - active: Active status (default: true)
    
    Example:
    product_id: "PROD-0051"
    title: "OnePlus 12"
    description: "Premium flagship smartphone with Snapdragon 8 Gen 3"
    units_in_stock: 75
    unit_price: 64999.00
    item_discount: 5.0
    warehouse_name: "Delhi NCR Hub"
    active: true
    """


@mcp.prompt("search-products")
def search_products_prompt() -> str:
    """Prompt template for searching products."""
    return """
    To search for products, use the search_products tool with a search query.
    
    The search will look for matches in:
    - Product titles
    - Product descriptions
    
    Search is case-insensitive and uses partial matching.
    
    Example search queries:
    - "Samsung" - finds all Samsung products
    - "smartphone" - finds all products with smartphone in title/description
    - "laptop" - finds all laptop products
    - "wireless" - finds wireless products
    """


@mcp.prompt("low-stock-alert")
def low_stock_prompt() -> str:
    """Prompt template for checking low stock products."""
    return """
    To check for low stock products, use the get_low_stock_products tool.
    
    You can specify a custom threshold (default is 10 units).
    This will return only ACTIVE products with stock at or below the threshold,
    sorted from lowest to highest stock levels.
    
    Example:
    - get_low_stock_products() - uses default threshold of 10 units
    - get_low_stock_products(threshold=20) - checks for products with ≤20 units
    """


# MCP Tools - Product Management

@mcp.tool()
def add_product(
    product_id: str,
    title: str,
    description: str,
    units_in_stock: int,
    unit_price: float,
    warehouse_name: str,
    item_discount: float = 0.0,
    active: bool = True
) -> str:
    """
    Add a new product to the database.
    
    Args:
        product_id: Unique product identifier (format: PROD-XXXX)
        title: Product title/name
        description: Detailed product description
        units_in_stock: Number of units available (≥ 0)
        unit_price: Price per unit in INR (> 0)
        warehouse_name: Name of warehouse
        item_discount: Discount percentage 0-100 (default: 0.0)
        active: Active status (default: True)
        
    Returns:
        Success or error message
    """
    try:
        library = get_library()
        success = library.add_product(
            product_id=product_id,
            title=title,
            description=description,
            units_in_stock=units_in_stock,
            unit_price=unit_price,
            item_discount=item_discount,
            warehouse_name=warehouse_name,
            active=active
        )
        
        if success:
            return f"✓ Successfully added product: {product_id} - {title}"
        else:
            return f"✗ Failed to add product. Validation failed or product ID {product_id} already exists"
    except Exception as e:
        return f"✗ Error adding product: {str(e)}"


@mcp.tool()
def get_product(product_id: str) -> str:
    """
    Retrieve a product by its ID.
    
    Args:
        product_id: Product ID to retrieve (format: PROD-XXXX)
        
    Returns:
        Product information or error message
    """
    try:
        library = get_library()
        product = library.get_product(product_id)
        
        if product is None:
            return f"✗ Product with ID {product_id} not found"
        
        discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
        total_value = discounted_price * product['units_in_stock']
        
        return f"""
Product Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {product['product_id']}
Title: {product['title']}
Description: {product['description']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stock: {product['units_in_stock']} units
Unit Price: ₹{product['unit_price']:,.2f}
Discount: {product['item_discount']}%
Discounted Price: ₹{discounted_price:,.2f}
Total Inventory Value: ₹{total_value:,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Warehouse: {product['warehouse_name']}
Active: {'Yes' if product['active'] else 'No'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created: {product['created_at']}
Updated: {product['updated_at']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    except Exception as e:
        return f"✗ Error retrieving product: {str(e)}"


@mcp.tool()
def get_all_products(
    active_only: bool = False,
    limit: Optional[int] = None
) -> str:
    """
    Get all products with optional filters.
    
    Args:
        active_only: Only return active products (default: False)
        limit: Maximum number of results (optional)
        
    Returns:
        List of products or error message
    """
    try:
        library = get_library()
        products = library.list_products(active_only=active_only)
        
        if not products:
            return "No products found matching the criteria"
        
        # Apply limit if specified
        if limit:
            products = products[:limit]
        
        result = f"Found {len(products)} product(s):\n\n"
        for product in products:
            discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
            status = "🟢 Active" if product['active'] else "🔴 Inactive"
            
            result += f"• {product['product_id']}: {product['title']}\n"
            result += f"  {product['description']}\n"
            result += f"  Stock: {product['units_in_stock']} units | Price: ₹{discounted_price:,.2f} | {status}\n"
            result += f"  Warehouse: {product['warehouse_name']}\n\n"
        
        return result
    except Exception as e:
        return f"✗ Error listing products: {str(e)}"


@mcp.tool()
def search_products(query: str) -> str:
    """
    Search products by title or description.
    
    Args:
        query: Search term to match (case-insensitive, partial match)
        
    Returns:
        List of matching products or error message
    """
    try:
        library = get_library()
        products = library.search_products(query)
        
        if not products:
            return f"No products found matching '{query}'"
        
        result = f"Found {len(products)} product(s) matching '{query}':\n\n"
        for product in products:
            discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
            status = "🟢 Active" if product['active'] else "🔴 Inactive"
            
            result += f"• {product['product_id']}: {product['title']}\n"
            result += f"  {product['description']}\n"
            result += f"  Stock: {product['units_in_stock']} units | Price: ₹{discounted_price:,.2f} | {status}\n"
            result += f"  Warehouse: {product['warehouse_name']}\n\n"
        
        return result
    except Exception as e:
        return f"✗ Error searching products: {str(e)}"


@mcp.tool()
def update_product(
    product_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    units_in_stock: Optional[int] = None,
    unit_price: Optional[float] = None,
    item_discount: Optional[float] = None,
    warehouse_name: Optional[str] = None,
    active: Optional[bool] = None
) -> str:
    """
    Update a product's information. Only provided fields will be updated.
    
    Args:
        product_id: Product ID to update
        title: New product title (optional)
        description: New description (optional)
        units_in_stock: New stock quantity (optional)
        unit_price: New unit price (optional)
        item_discount: New discount percentage (optional)
        warehouse_name: New warehouse name (optional)
        active: New active status (optional)
        
    Returns:
        Success or error message
    """
    try:
        library = get_library()
        
        # Build update dictionary
        updates = {}
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description
        if units_in_stock is not None:
            updates['units_in_stock'] = units_in_stock
        if unit_price is not None:
            updates['unit_price'] = unit_price
        if item_discount is not None:
            updates['item_discount'] = item_discount
        if warehouse_name is not None:
            updates['warehouse_name'] = warehouse_name
        if active is not None:
            updates['active'] = active
        
        if not updates:
            return "✗ No fields provided to update"
        
        success = library.update_product(product_id, **updates)
        
        if success:
            fields_updated = ", ".join(updates.keys())
            return f"✓ Successfully updated product {product_id}: {fields_updated}"
        else:
            return f"✗ Product with ID {product_id} not found"
    except Exception as e:
        return f"✗ Error updating product: {str(e)}"


@mcp.tool()
def delete_product(product_id: str) -> str:
    """
    Permanently delete a product from the database.
    
    Args:
        product_id: Product ID to delete
        
    Returns:
        Success or error message
    """
    try:
        library = get_library()
        success = library.delete_product(product_id)
        
        if success:
            return f"✓ Successfully deleted product: {product_id}"
        else:
            return f"✗ Product with ID {product_id} not found"
    except Exception as e:
        return f"✗ Error deleting product: {str(e)}"


@mcp.tool()
def get_products_by_warehouse(warehouse_name: str) -> str:
    """
    Get all products in a specific warehouse.
    
    Args:
        warehouse_name: Name of the warehouse
        
    Returns:
        List of products in the warehouse or error message
    """
    try:
        library = get_library()
        products = library.get_products_by_warehouse(warehouse_name)
        
        if not products:
            return f"No products found in warehouse: {warehouse_name}"
        
        result = f"Found {len(products)} product(s) in {warehouse_name}:\n\n"
        for product in products:
            discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
            status = "🟢 Active" if product['active'] else "🔴 Inactive"
            
            result += f"• {product['product_id']}: {product['title']}\n"
            result += f"  Stock: {product['units_in_stock']} units | Price: ₹{discounted_price:,.2f} | {status}\n\n"
        
        return result
    except Exception as e:
        return f"✗ Error getting warehouse products: {str(e)}"


@mcp.tool()
def get_low_stock_products(threshold: int = 10) -> str:
    """
    Get products with stock below or at a threshold (active products only).
    
    Args:
        threshold: Stock threshold (default: 10)
        
    Returns:
        List of low stock products sorted by stock level
    """
    try:
        library = get_library()
        products = library.get_low_stock_products(threshold=threshold)
        
        if not products:
            return f"No active products found with stock ≤ {threshold} units"
        
        result = f"⚠️ Found {len(products)} active product(s) with stock ≤ {threshold} units:\n\n"
        for product in products:
            discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
            
            result += f"• {product['product_id']}: {product['title']}\n"
            result += f"  Stock: {product['units_in_stock']} units (LOW STOCK) | Price: ₹{discounted_price:,.2f}\n"
            result += f"  Warehouse: {product['warehouse_name']}\n\n"
        
        return result
    except Exception as e:
        return f"✗ Error getting low stock products: {str(e)}"


@mcp.tool()
def get_product_statistics() -> str:
    """
    Get statistics about the product database.
    
    Returns:
        Product database statistics
    """
    try:
        library = get_library()
        all_products = library.list_products()
        active_products = library.list_products(active_only=True)
        
        if not all_products:
            return "No products in the database"
        
        total_stock = sum(p['units_in_stock'] for p in all_products)
        prices = [p['unit_price'] for p in all_products]
        
        # Calculate total inventory value (with discounts)
        total_value = sum(
            p['units_in_stock'] * p['unit_price'] * (1 - p['item_discount'] / 100)
            for p in all_products
        )
        
        # Get warehouse distribution
        warehouses = {}
        for p in all_products:
            wh = p['warehouse_name']
            warehouses[wh] = warehouses.get(wh, 0) + 1
        
        warehouse_info = "\n".join([f"  • {wh}: {count} products" for wh, count in sorted(warehouses.items())])
        
        return f"""
Product Database Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Products: {len(all_products)}
Active Products: {len(active_products)}
Inactive Products: {len(all_products) - len(active_products)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Stock Units: {total_stock:,}
Total Inventory Value: ₹{total_value:,.2f}
Average Unit Price: ₹{sum(prices) / len(prices):,.2f}
Min Unit Price: ₹{min(prices):,.2f}
Max Unit Price: ₹{max(prices):,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Warehouses ({len(warehouses)}):
{warehouse_info}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    except Exception as e:
        return f"✗ Error getting statistics: {str(e)}"


# Export MCP instance
__all__ = ["mcp"]
