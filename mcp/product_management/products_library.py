"""
Main Products Library interface.
"""

from typing import Optional, List, Dict, Any
from .config import config
from .database import DatabaseManager
from .models import Product


class ProductsLibrary:
    """Main class for managing products in SQLite database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the Products Library.
        
        Args:
            db_path: Path to SQLite database. If None, uses DATABASE_PATH from .env
        """
        if db_path is None:
            db_path = config.get_database_path()
        
        self.db_path = db_path
        self.db_manager = DatabaseManager(db_path)
    
    def add_product(self, product_id: str, title: str, description: str,
                   units_in_stock: int, unit_price: float, item_discount: float = 0.0,
                   warehouse_name: str = '', active: bool = True) -> bool:
        """
        Add a new product to the database.
        
        Args:
            product_id: Product ID (format: PROD-XXXX)
            title: Product title
            description: Product description
            units_in_stock: Number of units available
            unit_price: Price per unit
            item_discount: Discount percentage (0-100)
            warehouse_name: Name of warehouse
            active: Active status (default: True)
        
        Returns:
            True if successful, False otherwise
        """
        product = Product(
            product_id=product_id,
            title=title,
            description=description,
            units_in_stock=units_in_stock,
            unit_price=unit_price,
            item_discount=item_discount,
            warehouse_name=warehouse_name,
            active=active
        )
        
        if not product.validate():
            return False
        
        return self.db_manager.add_product(product)
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID to retrieve
        
        Returns:
            Product dictionary or None if not found
        """
        product = self.db_manager.get_product(product_id)
        return product.to_dict() if product else None
    
    def update_product(self, product_id: str, **kwargs) -> bool:
        """
        Update a product's information.
        
        Args:
            product_id: Product ID to update
            **kwargs: Fields to update (title, description, units_in_stock, 
                     unit_price, item_discount, warehouse_name, active)
        
        Returns:
            True if successful, False otherwise
        """
        return self.db_manager.update_product(product_id, **kwargs)
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product from the database.
        
        Args:
            product_id: Product ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        return self.db_manager.delete_product(product_id)
    
    def list_products(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        List all products.
        
        Args:
            active_only: If True, only return active products
        
        Returns:
            List of product dictionaries
        """
        products = self.db_manager.list_products(active_only)
        return [product.to_dict() for product in products]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search products by title or description.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching product dictionaries
        """
        products = self.db_manager.search_products(query)
        return [product.to_dict() for product in products]
    
    def get_products_by_warehouse(self, warehouse_name: str) -> List[Dict[str, Any]]:
        """
        Get all products in a specific warehouse.
        
        Args:
            warehouse_name: Name of the warehouse
        
        Returns:
            List of product dictionaries
        """
        products = self.db_manager.get_products_by_warehouse(warehouse_name)
        return [product.to_dict() for product in products]
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """
        Get products with stock below a threshold.
        
        Args:
            threshold: Stock threshold (default: 10)
        
        Returns:
            List of product dictionaries
        """
        products = self.db_manager.get_low_stock_products(threshold)
        return [product.to_dict() for product in products]
