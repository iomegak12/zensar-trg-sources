"""
Comprehensive test suite for Product Management Library.
Tests all functionalities including CRUD operations, search, and validations.
"""

import unittest
import os
import sys
from pathlib import Path

# Add parent directory to path to import product_management
sys.path.insert(0, str(Path(__file__).parent.parent))

from product_management import ProductsLibrary


class TestProductManagement(unittest.TestCase):
    """Test suite for Product Management Library."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests."""
        cls.test_db_path = 'tests/test_products.db'
        # Remove test database if it exists
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
    
    def setUp(self):
        """Set up fresh library instance for each test."""
        self.library = ProductsLibrary(db_path=self.test_db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        # Delete all products
        products = self.library.list_products()
        for product in products:
            self.library.delete_product(product['product_id'])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database after all tests."""
        # Give time for database connections to close
        import time
        time.sleep(0.1)
        
        try:
            if os.path.exists(cls.test_db_path):
                os.remove(cls.test_db_path)
        except PermissionError:
            # File is still locked, skip cleanup
            print(f"\nWarning: Could not remove test database {cls.test_db_path}")
            pass
    
    # ==================== ADD PRODUCT TESTS ====================
    
    def test_add_product_success(self):
        """Test adding a valid product."""
        result = self.library.add_product(
            product_id="PROD-0001",
            title="Test Product",
            description="Test Description",
            units_in_stock=100,
            unit_price=999.99,
            item_discount=10.0,
            warehouse_name="Test Warehouse",
            active=True
        )
        self.assertTrue(result)
        
        # Verify product was added
        product = self.library.get_product("PROD-0001")
        self.assertIsNotNone(product)
        self.assertEqual(product['title'], "Test Product")
    
    def test_add_product_duplicate_id(self):
        """Test adding product with duplicate ID."""
        self.library.add_product(
            product_id="PROD-0001",
            title="First Product",
            description="First",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse A"
        )
        
        # Try to add duplicate
        result = self.library.add_product(
            product_id="PROD-0001",
            title="Duplicate Product",
            description="Duplicate",
            units_in_stock=20,
            unit_price=200.0,
            warehouse_name="Warehouse B"
        )
        self.assertFalse(result)
    
    def test_add_product_with_defaults(self):
        """Test adding product with default values."""
        result = self.library.add_product(
            product_id="PROD-0002",
            title="Product with Defaults",
            description="Testing defaults",
            units_in_stock=50,
            unit_price=500.0,
            warehouse_name="Default Warehouse"
        )
        self.assertTrue(result)
        
        product = self.library.get_product("PROD-0002")
        self.assertEqual(product['item_discount'], 0.0)
        self.assertTrue(product['active'])
    
    def test_add_product_invalid_id_format(self):
        """Test adding product with invalid ID format."""
        result = self.library.add_product(
            product_id="INVALID-001",
            title="Invalid Product",
            description="Invalid ID",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse"
        )
        self.assertFalse(result)
    
    def test_add_product_invalid_discount(self):
        """Test adding product with invalid discount."""
        result = self.library.add_product(
            product_id="PROD-0003",
            title="Invalid Discount",
            description="Discount > 100",
            units_in_stock=10,
            unit_price=100.0,
            item_discount=150.0,
            warehouse_name="Warehouse"
        )
        self.assertFalse(result)
    
    # ==================== GET PRODUCT TESTS ====================
    
    def test_get_product_exists(self):
        """Test getting an existing product."""
        self.library.add_product(
            product_id="PROD-0010",
            title="Existing Product",
            description="This product exists",
            units_in_stock=25,
            unit_price=250.0,
            item_discount=5.0,
            warehouse_name="Main Warehouse"
        )
        
        product = self.library.get_product("PROD-0010")
        self.assertIsNotNone(product)
        self.assertEqual(product['product_id'], "PROD-0010")
        self.assertEqual(product['title'], "Existing Product")
        self.assertEqual(product['units_in_stock'], 25)
        self.assertEqual(product['unit_price'], 250.0)
        self.assertEqual(product['item_discount'], 5.0)
    
    def test_get_product_not_exists(self):
        """Test getting a non-existent product."""
        product = self.library.get_product("PROD-9999")
        self.assertIsNone(product)
    
    # ==================== UPDATE PRODUCT TESTS ====================
    
    def test_update_product_single_field(self):
        """Test updating a single field."""
        self.library.add_product(
            product_id="PROD-0020",
            title="Update Test",
            description="Before update",
            units_in_stock=100,
            unit_price=1000.0,
            warehouse_name="Warehouse A"
        )
        
        result = self.library.update_product("PROD-0020", units_in_stock=50)
        self.assertTrue(result)
        
        product = self.library.get_product("PROD-0020")
        self.assertEqual(product['units_in_stock'], 50)
        self.assertEqual(product['title'], "Update Test")  # Other fields unchanged
    
    def test_update_product_multiple_fields(self):
        """Test updating multiple fields."""
        self.library.add_product(
            product_id="PROD-0021",
            title="Multi Update",
            description="Original",
            units_in_stock=100,
            unit_price=500.0,
            item_discount=0.0,
            warehouse_name="Warehouse A"
        )
        
        result = self.library.update_product(
            "PROD-0021",
            units_in_stock=75,
            unit_price=450.0,
            item_discount=15.0,
            warehouse_name="Warehouse B"
        )
        self.assertTrue(result)
        
        product = self.library.get_product("PROD-0021")
        self.assertEqual(product['units_in_stock'], 75)
        self.assertEqual(product['unit_price'], 450.0)
        self.assertEqual(product['item_discount'], 15.0)
        self.assertEqual(product['warehouse_name'], "Warehouse B")
    
    def test_update_product_not_exists(self):
        """Test updating a non-existent product."""
        result = self.library.update_product("PROD-9999", units_in_stock=100)
        self.assertFalse(result)
    
    def test_update_product_no_fields(self):
        """Test updating with no valid fields."""
        self.library.add_product(
            product_id="PROD-0022",
            title="No Update",
            description="Test",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse"
        )
        
        result = self.library.update_product("PROD-0022")
        self.assertFalse(result)
    
    def test_update_product_active_status(self):
        """Test updating active status."""
        self.library.add_product(
            product_id="PROD-0023",
            title="Active Test",
            description="Test",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        
        result = self.library.update_product("PROD-0023", active=False)
        self.assertTrue(result)
        
        product = self.library.get_product("PROD-0023")
        self.assertFalse(product['active'])
    
    # ==================== DELETE PRODUCT TESTS ====================
    
    def test_delete_product_exists(self):
        """Test deleting an existing product."""
        self.library.add_product(
            product_id="PROD-0030",
            title="To Delete",
            description="Will be deleted",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse"
        )
        
        result = self.library.delete_product("PROD-0030")
        self.assertTrue(result)
        
        product = self.library.get_product("PROD-0030")
        self.assertIsNone(product)
    
    def test_delete_product_not_exists(self):
        """Test deleting a non-existent product."""
        result = self.library.delete_product("PROD-9999")
        self.assertFalse(result)
    
    # ==================== LIST PRODUCTS TESTS ====================
    
    def test_list_products_all(self):
        """Test listing all products."""
        # Add multiple products
        for i in range(1, 6):
            self.library.add_product(
                product_id=f"PROD-00{i}0",
                title=f"Product {i}",
                description=f"Description {i}",
                units_in_stock=i * 10,
                unit_price=i * 100.0,
                warehouse_name="Warehouse A",
                active=(i % 2 == 0)  # Alternate active/inactive
            )
        
        products = self.library.list_products()
        self.assertEqual(len(products), 5)
    
    def test_list_products_active_only(self):
        """Test listing only active products."""
        # Add active and inactive products
        self.library.add_product(
            product_id="PROD-0041",
            title="Active 1",
            description="Active",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        self.library.add_product(
            product_id="PROD-0042",
            title="Inactive 1",
            description="Inactive",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=False
        )
        self.library.add_product(
            product_id="PROD-0043",
            title="Active 2",
            description="Active",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        
        active_products = self.library.list_products(active_only=True)
        self.assertEqual(len(active_products), 2)
        
        for product in active_products:
            self.assertTrue(product['active'])
    
    def test_list_products_empty(self):
        """Test listing products when none exist."""
        products = self.library.list_products()
        self.assertEqual(len(products), 0)
    
    # ==================== SEARCH PRODUCTS TESTS ====================
    
    def test_search_products_by_title(self):
        """Test searching products by title."""
        self.library.add_product(
            product_id="PROD-0050",
            title="Samsung Galaxy S24",
            description="Flagship phone",
            units_in_stock=50,
            unit_price=75000.0,
            warehouse_name="Mumbai"
        )
        self.library.add_product(
            product_id="PROD-0051",
            title="iPhone 15",
            description="Apple phone",
            units_in_stock=30,
            unit_price=80000.0,
            warehouse_name="Delhi"
        )
        
        results = self.library.search_products("Samsung")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['product_id'], "PROD-0050")
    
    def test_search_products_by_description(self):
        """Test searching products by description."""
        self.library.add_product(
            product_id="PROD-0052",
            title="Product A",
            description="Gaming laptop with RTX 4090",
            units_in_stock=10,
            unit_price=150000.0,
            warehouse_name="Bangalore"
        )
        self.library.add_product(
            product_id="PROD-0053",
            title="Product B",
            description="Office laptop",
            units_in_stock=20,
            unit_price=50000.0,
            warehouse_name="Pune"
        )
        
        results = self.library.search_products("Gaming")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['product_id'], "PROD-0052")
    
    def test_search_products_multiple_results(self):
        """Test search returning multiple results."""
        for i in range(3):
            self.library.add_product(
                product_id=f"PROD-006{i}",
                title=f"Laptop Model {i}",
                description="High performance laptop",
                units_in_stock=10 + i,
                unit_price=50000.0 + (i * 10000),
                warehouse_name="Warehouse"
            )
        
        results = self.library.search_products("Laptop")
        self.assertEqual(len(results), 3)
    
    def test_search_products_no_results(self):
        """Test search with no matching results."""
        self.library.add_product(
            product_id="PROD-0070",
            title="Test Product",
            description="Test Description",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse"
        )
        
        results = self.library.search_products("NonExistent")
        self.assertEqual(len(results), 0)
    
    def test_search_products_case_insensitive(self):
        """Test that search is case-insensitive."""
        self.library.add_product(
            product_id="PROD-0071",
            title="UPPERCASE TITLE",
            description="Lowercase description",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse"
        )
        
        # SQLite LIKE is case-insensitive by default
        results = self.library.search_products("uppercase")
        self.assertEqual(len(results), 1)
    
    # ==================== WAREHOUSE TESTS ====================
    
    def test_get_products_by_warehouse(self):
        """Test getting products by warehouse."""
        self.library.add_product(
            product_id="PROD-0080",
            title="Mumbai Product 1",
            description="Product 1",
            units_in_stock=10,
            unit_price=1000.0,
            warehouse_name="Mumbai Warehouse"
        )
        self.library.add_product(
            product_id="PROD-0081",
            title="Delhi Product 1",
            description="Product 2",
            units_in_stock=20,
            unit_price=2000.0,
            warehouse_name="Delhi Warehouse"
        )
        self.library.add_product(
            product_id="PROD-0082",
            title="Mumbai Product 2",
            description="Product 3",
            units_in_stock=30,
            unit_price=3000.0,
            warehouse_name="Mumbai Warehouse"
        )
        
        mumbai_products = self.library.get_products_by_warehouse("Mumbai Warehouse")
        self.assertEqual(len(mumbai_products), 2)
        
        for product in mumbai_products:
            self.assertEqual(product['warehouse_name'], "Mumbai Warehouse")
    
    def test_get_products_by_warehouse_empty(self):
        """Test getting products from warehouse with no products."""
        self.library.add_product(
            product_id="PROD-0083",
            title="Test",
            description="Test",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse A"
        )
        
        results = self.library.get_products_by_warehouse("Warehouse B")
        self.assertEqual(len(results), 0)
    
    # ==================== LOW STOCK TESTS ====================
    
    def test_get_low_stock_products_default_threshold(self):
        """Test getting low stock products with default threshold."""
        self.library.add_product(
            product_id="PROD-0090",
            title="Low Stock",
            description="Only 5 units",
            units_in_stock=5,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        self.library.add_product(
            product_id="PROD-0091",
            title="High Stock",
            description="100 units",
            units_in_stock=100,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        self.library.add_product(
            product_id="PROD-0092",
            title="Medium Stock",
            description="10 units",
            units_in_stock=10,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        
        low_stock = self.library.get_low_stock_products()
        self.assertEqual(len(low_stock), 2)  # 5 and 10 units (≤ 10)
    
    def test_get_low_stock_products_custom_threshold(self):
        """Test getting low stock products with custom threshold."""
        self.library.add_product(
            product_id="PROD-0093",
            title="Stock 15",
            description="15 units",
            units_in_stock=15,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        self.library.add_product(
            product_id="PROD-0094",
            title="Stock 25",
            description="25 units",
            units_in_stock=25,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        
        low_stock = self.library.get_low_stock_products(threshold=20)
        self.assertEqual(len(low_stock), 1)
        self.assertEqual(low_stock[0]['units_in_stock'], 15)
    
    def test_get_low_stock_products_active_only(self):
        """Test that low stock only returns active products."""
        self.library.add_product(
            product_id="PROD-0095",
            title="Low Stock Active",
            description="Active low stock",
            units_in_stock=5,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=True
        )
        self.library.add_product(
            product_id="PROD-0096",
            title="Low Stock Inactive",
            description="Inactive low stock",
            units_in_stock=3,
            unit_price=100.0,
            warehouse_name="Warehouse",
            active=False
        )
        
        low_stock = self.library.get_low_stock_products()
        self.assertEqual(len(low_stock), 1)
        self.assertTrue(low_stock[0]['active'])
    
    def test_get_low_stock_products_sorted(self):
        """Test that low stock products are sorted by stock level."""
        stocks = [8, 3, 10, 1, 7]
        for i, stock in enumerate(stocks):
            self.library.add_product(
                product_id=f"PROD-01{i:02d}",
                title=f"Stock {stock}",
                description=f"{stock} units",
                units_in_stock=stock,
                unit_price=100.0,
                warehouse_name="Warehouse",
                active=True
            )
        
        low_stock = self.library.get_low_stock_products()
        
        # Verify sorted in ascending order
        for i in range(len(low_stock) - 1):
            self.assertLessEqual(
                low_stock[i]['units_in_stock'],
                low_stock[i + 1]['units_in_stock']
            )


def run_tests():
    """Run all tests and display results."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestProductManagement)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
