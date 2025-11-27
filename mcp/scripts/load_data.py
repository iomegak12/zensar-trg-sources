"""
Load sample data into the products database.
Generates 50 Indian electronic products with realistic data.
"""

from product_management import ProductsLibrary
import random


def generate_sample_products():
    """Generate 50 sample Indian electronic products."""
    
    products = []
    
    # Indian electronic product names with brands
    product_templates = [
        # Smartphones
        ("Samsung Galaxy S24", "Latest flagship smartphone with advanced camera system", 75999.00),
        ("OnePlus 12", "Premium smartphone with fast charging technology", 64999.00),
        ("Redmi Note 13 Pro", "Mid-range smartphone with excellent value", 24999.00),
        ("Vivo V29", "Camera-focused smartphone with stunning design", 32999.00),
        ("Realme GT 3", "Gaming smartphone with high refresh rate display", 42999.00),
        ("iPhone 15", "Apple's latest smartphone with A17 chip", 89999.00),
        ("OPPO Reno 11", "Feature-rich smartphone with premium build", 29999.00),
        ("Motorola Edge 40", "Clean Android experience with great performance", 28999.00),
        ("Nothing Phone 2", "Unique transparent design smartphone", 44999.00),
        ("Poco X6 Pro", "Budget gaming powerhouse smartphone", 26999.00),
        
        # Laptops
        ("HP Pavilion 15", "Intel Core i5 laptop for everyday computing", 54999.00),
        ("Dell Inspiron 14", "Productivity laptop with sleek design", 48999.00),
        ("Lenovo IdeaPad Slim 3", "Lightweight laptop for students", 38999.00),
        ("Asus VivoBook 15", "Versatile laptop with fingerprint sensor", 42999.00),
        ("Acer Aspire 5", "Affordable laptop with solid performance", 39999.00),
        ("MacBook Air M2", "Apple's thin and light premium laptop", 114900.00),
        ("MSI GF63 Thin", "Gaming laptop with dedicated graphics", 59999.00),
        ("Lenovo ThinkPad E14", "Business laptop with robust build", 62999.00),
        
        # Tablets
        ("Samsung Galaxy Tab S9", "Premium Android tablet with S Pen", 74999.00),
        ("iPad 10th Gen", "Apple's versatile tablet for all", 44900.00),
        ("Lenovo Tab P11", "Entertainment tablet with quad speakers", 22999.00),
        ("OnePlus Pad", "Fast and smooth Android tablet", 37999.00),
        ("Realme Pad 2", "Budget-friendly tablet for media consumption", 18999.00),
        
        # Headphones & Earbuds
        ("Sony WH-1000XM5", "Industry-leading noise cancelling headphones", 29990.00),
        ("JBL Tune 760NC", "Wireless headphones with active noise cancellation", 5999.00),
        ("boAt Airdopes 141", "True wireless earbuds with deep bass", 1299.00),
        ("OnePlus Buds Pro 2", "Premium TWS earbuds with spatial audio", 11999.00),
        ("Noise Buds VS104", "Affordable wireless earbuds", 999.00),
        ("Samsung Galaxy Buds2 Pro", "High-quality TWS with intelligent ANC", 15990.00),
        
        # Smartwatches
        ("Apple Watch Series 9", "Advanced health and fitness smartwatch", 45900.00),
        ("Samsung Galaxy Watch 6", "Premium Android smartwatch", 30999.00),
        ("Noise ColorFit Pro 4", "Budget fitness smartwatch", 2999.00),
        ("Fire-Boltt Phoenix Ultra", "Feature-rich affordable smartwatch", 1799.00),
        ("Amazfit GTR 4", "Long battery life smartwatch", 12999.00),
        ("Boat Wave Call 2", "Smartwatch with Bluetooth calling", 2299.00),
        
        # TVs
        ("Samsung 55-inch Crystal 4K Neo", "Crystal clear 4K smart TV", 54990.00),
        ("LG 43-inch 4K UHD Smart TV", "Vivid colors with WebOS", 36990.00),
        ("Mi 32-inch HD Ready Smart TV", "Affordable smart TV with Android", 13999.00),
        ("Sony Bravia 65-inch 4K", "Premium 4K HDR smart TV", 94990.00),
        ("OnePlus Y1S 43-inch", "Smart TV with bezel-less design", 26999.00),
        
        # Other Electronics
        ("Canon EOS 1500D DSLR", "Entry-level DSLR camera with 24.1MP", 32999.00),
        ("GoPro Hero 11", "Action camera with 5.3K video", 37999.00),
        ("Philips Air Fryer HD9252", "Digital air fryer for healthy cooking", 8999.00),
        ("Dyson V12 Detect Slim", "Cordless vacuum cleaner with laser detection", 49900.00),
        ("Marshall Emberton II", "Portable Bluetooth speaker", 16999.00),
        ("Kindle Paperwhite", "Waterproof e-reader with adjustable light", 13999.00),
        ("Amazon Echo Dot 5th Gen", "Smart speaker with Alexa", 4999.00),
        ("Logitech MX Master 3S", "Wireless performance mouse", 8995.00),
        ("Blue Yeti USB Microphone", "Professional USB microphone", 11999.00),
        ("Seagate 2TB External HDD", "Portable external hard drive", 5499.00),
    ]
    
    warehouses = [
        "Mumbai Central Warehouse",
        "Delhi NCR Hub",
        "Bangalore Tech Park",
        "Hyderabad Distribution Center",
        "Chennai Storage Facility",
        "Pune Logistics Hub",
        "Kolkata Regional Warehouse"
    ]
    
    for i, (title, description, price) in enumerate(product_templates, 1):
        product_id = f"PROD-{i:04d}"
        units_in_stock = random.randint(5, 200)
        item_discount = random.choice([0, 5, 10, 15, 20, 25])
        warehouse_name = random.choice(warehouses)
        active = True if random.random() > 0.1 else False  # 90% active
        
        products.append({
            'product_id': product_id,
            'title': title,
            'description': description,
            'units_in_stock': units_in_stock,
            'unit_price': price,
            'item_discount': item_discount,
            'warehouse_name': warehouse_name,
            'active': active
        })
    
    return products


def main():
    """Main function to load sample data."""
    print("Initializing Products Library...")
    library = ProductsLibrary()
    
    print("Generating 50 sample Indian electronic products...")
    products = generate_sample_products()
    
    print("Loading products into database...")
    success_count = 0
    for product in products:
        if library.add_product(**product):
            success_count += 1
            print(f"✓ Added {product['product_id']}: {product['title']}")
        else:
            print(f"✗ Failed to add {product['product_id']}: {product['title']}")
    
    print(f"\n{'='*60}")
    print(f"Data loading complete!")
    print(f"Successfully added {success_count} out of {len(products)} products")
    print(f"{'='*60}")
    
    # Display summary statistics
    all_products = library.list_products()
    active_products = library.list_products(active_only=True)
    
    print(f"\nDatabase Summary:")
    print(f"  Total products: {len(all_products)}")
    print(f"  Active products: {len(active_products)}")
    print(f"  Inactive products: {len(all_products) - len(active_products)}")
    
    # Show low stock items
    low_stock = library.get_low_stock_products(threshold=20)
    if low_stock:
        print(f"\n  Products with low stock (≤20 units): {len(low_stock)}")
        for product in low_stock[:5]:
            print(f"    - {product['product_id']}: {product['title']} ({product['units_in_stock']} units)")
    
    # Show warehouse distribution
    warehouses = {}
    for product in all_products:
        wh = product['warehouse_name']
        warehouses[wh] = warehouses.get(wh, 0) + 1
    
    print(f"\n  Products by warehouse:")
    for wh, count in sorted(warehouses.items()):
        print(f"    - {wh}: {count} products")


if __name__ == "__main__":
    main()
