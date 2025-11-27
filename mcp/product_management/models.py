"""
Data models for the Product Management Library.
"""

from typing import Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Product(Base):
    """Product data model using SQLAlchemy ORM."""
    
    __tablename__ = 'products'
    
    product_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    units_in_stock = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float, nullable=False)
    item_discount = Column(Float, default=0.0)
    warehouse_name = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary."""
        return {
            'product_id': self.product_id,
            'title': self.title,
            'description': self.description,
            'units_in_stock': self.units_in_stock,
            'unit_price': self.unit_price,
            'item_discount': self.item_discount,
            'warehouse_name': self.warehouse_name,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create Product instance from dictionary."""
        # Filter out timestamp fields if present
        filtered_data = {k: v for k, v in data.items() 
                        if k not in ['created_at', 'updated_at']}
        return cls(**filtered_data)
    
    def validate(self) -> bool:
        """Validate product data."""
        if not self.product_id or not self.product_id.startswith('PROD-'):
            return False
        if not self.title or len(self.title.strip()) == 0:
            return False
        if self.units_in_stock < 0:
            return False
        if self.unit_price < 0:
            return False
        if self.item_discount < 0 or self.item_discount > 100:
            return False
        if not self.warehouse_name or len(self.warehouse_name.strip()) == 0:
            return False
        return True
    
    def get_discounted_price(self) -> float:
        """Calculate price after discount."""
        return self.unit_price * (1 - self.item_discount / 100)
    
    def get_total_value(self) -> float:
        """Calculate total inventory value for this product."""
        return self.get_discounted_price() * self.units_in_stock
    
    def __repr__(self) -> str:
        """String representation of Product."""
        return f"<Product(product_id='{self.product_id}', title='{self.title}')>"
