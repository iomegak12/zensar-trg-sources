"""
Products Library - A Python library for managing product information with SQLite backend.
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ProductsLibrary:
    """Main class for managing products in SQLite database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the Products Library.
        
        Args:
            db_path: Path to SQLite database. If None, uses DATABASE_PATH from .env
        """
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', 'dbs/products.db')
        
        self.db_path = db_path
        self._ensure_db_directory()
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Create database directory if it doesn't exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_database(self):
        """Create products table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    units_in_stock INTEGER NOT NULL DEFAULT 0,
                    unit_price REAL NOT NULL,
                    item_discount REAL DEFAULT 0.0,
                    warehouse_name TEXT NOT NULL,
                    active BOOLEAN NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _dict_from_row(self, row: tuple) -> Dict[str, Any]:
        """Convert database row to dictionary."""
        if row is None:
            return None
        return {
            'product_id': row[0],
            'title': row[1],
            'description': row[2],
            'units_in_stock': row[3],
            'unit_price': row[4],
            'item_discount': row[5],
            'warehouse_name': row[6],
            'active': bool(row[7]),
            'created_at': row[8],
            'updated_at': row[9]
        }
    
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
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products 
                    (product_id, title, description, units_in_stock, unit_price, 
                     item_discount, warehouse_name, active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (product_id, title, description, units_in_stock, unit_price,
                      item_discount, warehouse_name, active))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID to retrieve
        
        Returns:
            Product dictionary or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            row = cursor.fetchone()
            return self._dict_from_row(row)
    
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
        allowed_fields = ['title', 'description', 'units_in_stock', 'unit_price',
                         'item_discount', 'warehouse_name', 'active']
        
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        set_clause += ', updated_at = CURRENT_TIMESTAMP'
        values = list(updates.values()) + [product_id]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'UPDATE products SET {set_clause} WHERE product_id = ?', values)
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product from the database.
        
        Args:
            product_id: Product ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def list_products(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        List all products.
        
        Args:
            active_only: If True, only return active products
        
        Returns:
            List of product dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if active_only:
                cursor.execute('SELECT * FROM products WHERE active = 1 ORDER BY product_id')
            else:
                cursor.execute('SELECT * FROM products ORDER BY product_id')
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search products by title or description.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching product dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_term = f'%{query}%'
            cursor.execute('''
                SELECT * FROM products 
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY product_id
            ''', (search_term, search_term))
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
    
    def get_products_by_warehouse(self, warehouse_name: str) -> List[Dict[str, Any]]:
        """
        Get all products in a specific warehouse.
        
        Args:
            warehouse_name: Name of the warehouse
        
        Returns:
            List of product dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM products 
                WHERE warehouse_name = ?
                ORDER BY product_id
            ''', (warehouse_name,))
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """
        Get products with stock below a threshold.
        
        Args:
            threshold: Stock threshold (default: 10)
        
        Returns:
            List of product dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM products 
                WHERE units_in_stock <= ? AND active = 1
                ORDER BY units_in_stock
            ''', (threshold,))
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
