"""
Database operations for the Product Management Library using SQLAlchemy ORM.
"""

from typing import Optional, List
from pathlib import Path
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .models import Product, Base


class DatabaseManager:
    """Handles all database operations for products using SQLAlchemy ORM."""
    
    def __init__(self, db_path: str):
        """
        Initialize the Database Manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_directory()
        
        # Create SQLAlchemy engine
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        
        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        
        # Create tables
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Create database directory if it doesn't exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_database(self):
        """Create products table if it doesn't exist."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def add_product(self, product: Product) -> bool:
        """
        Add a new product to the database.
        
        Args:
            product: Product instance to add
        
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            session.add(product)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID to retrieve
        
        Returns:
            Product instance or None if not found
        """
        session = self.get_session()
        try:
            product = session.query(Product).filter(Product.product_id == product_id).first()
            if product:
                # Detach from session to avoid lazy loading issues
                session.expunge(product)
            return product
        finally:
            session.close()
    
    def update_product(self, product_id: str, **kwargs) -> bool:
        """
        Update a product's information.
        
        Args:
            product_id: Product ID to update
            **kwargs: Fields to update
        
        Returns:
            True if successful, False otherwise
        """
        allowed_fields = ['title', 'description', 'units_in_stock', 'unit_price',
                         'item_discount', 'warehouse_name', 'active']
        
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        session = self.get_session()
        try:
            result = session.query(Product).filter(Product.product_id == product_id).update(updates)
            session.commit()
            return result > 0
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product from the database.
        
        Args:
            product_id: Product ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            result = session.query(Product).filter(Product.product_id == product_id).delete()
            session.commit()
            return result > 0
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()
    
    def list_products(self, active_only: bool = False) -> List[Product]:
        """
        List all products.
        
        Args:
            active_only: If True, only return active products
        
        Returns:
            List of Product instances
        """
        session = self.get_session()
        try:
            query = session.query(Product)
            if active_only:
                query = query.filter(Product.active == True)
            products = query.order_by(Product.product_id).all()
            
            # Detach from session
            for product in products:
                session.expunge(product)
            
            return products
        finally:
            session.close()
    
    def search_products(self, query: str) -> List[Product]:
        """
        Search products by title or description.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching Product instances
        """
        session = self.get_session()
        try:
            search_term = f'%{query}%'
            products = session.query(Product).filter(
                or_(
                    Product.title.like(search_term),
                    Product.description.like(search_term)
                )
            ).order_by(Product.product_id).all()
            
            # Detach from session
            for product in products:
                session.expunge(product)
            
            return products
        finally:
            session.close()
    
    def get_products_by_warehouse(self, warehouse_name: str) -> List[Product]:
        """
        Get all products in a specific warehouse.
        
        Args:
            warehouse_name: Name of the warehouse
        
        Returns:
            List of Product instances
        """
        session = self.get_session()
        try:
            products = session.query(Product).filter(
                Product.warehouse_name == warehouse_name
            ).order_by(Product.product_id).all()
            
            # Detach from session
            for product in products:
                session.expunge(product)
            
            return products
        finally:
            session.close()
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Get products with stock below a threshold.
        
        Args:
            threshold: Stock threshold (default: 10)
        
        Returns:
            List of Product instances
        """
        session = self.get_session()
        try:
            products = session.query(Product).filter(
                Product.units_in_stock <= threshold,
                Product.active == True
            ).order_by(Product.units_in_stock).all()
            
            # Detach from session
            for product in products:
                session.expunge(product)
            
            return products
        finally:
            session.close()
