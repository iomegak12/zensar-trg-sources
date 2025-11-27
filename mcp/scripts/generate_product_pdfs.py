"""
Generate marketing PDF documents for products
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from product_management.products_library import ProductsLibrary

# Initialize the products library
products_lib = ProductsLibrary()

# Product IDs from the file
PRODUCT_IDS = [
    "PROD-0021", "PROD-0022", "PROD-0023", "PROD-0024", "PROD-0025",
    "PROD-0026", "PROD-0027", "PROD-0028", "PROD-0029", "PROD-0030",
    "PROD-0031", "PROD-0032", "PROD-0033", "PROD-0034", "PROD-0035",
    "PROD-0036", "PROD-0037", "PROD-0038", "PROD-0039", "PROD-0040",
    "PROD-0041", "PROD-0042", "PROD-0043", "PROD-0044", "PROD-0045",
    "PROD-0046", "PROD-0047", "PROD-0048", "PROD-0049", "PROD-0050"
]

def generate_marketing_content(product):
    """Generate marketing paragraphs and key points for a product"""
    
    title = product.get('title', 'Product')
    description = product.get('description', '')
    price = product.get('unit_price', 0)
    discount = product.get('item_discount', 0)
    discounted_price = price * (1 - discount / 100)
    
    # Marketing paragraphs
    paragraphs = [
        f"Introducing the {title} - a revolutionary product that redefines excellence in its category. "
        f"{description}. This exceptional product combines cutting-edge technology with superior craftsmanship "
        f"to deliver an unparalleled user experience. Whether you're a professional seeking top-tier performance "
        f"or an enthusiast looking for the best value, the {title} stands out as the perfect choice for discerning customers.",
        
        f"Experience premium quality without compromising on affordability. Originally priced at ₹{price:,.2f}, "
        f"we're offering an exclusive {discount}% discount, bringing the price down to just ₹{discounted_price:,.2f}. "
        f"This limited-time offer represents exceptional value for money, making premium technology accessible to everyone. "
        f"Don't miss this opportunity to own a product that delivers superior performance, reliability, and style "
        f"at an unbeatable price point.",
        
        f"Join thousands of satisfied customers who have already discovered the excellence of {title}. "
        f"Our commitment to quality, customer satisfaction, and innovation ensures that every purchase is backed by "
        f"comprehensive warranty coverage and dedicated customer support. With fast delivery from our strategically "
        f"located warehouses and hassle-free returns, your shopping experience is guaranteed to be smooth and satisfying. "
        f"Invest in quality, invest in {title} - where innovation meets reliability."
    ]
    
    # Key selling points
    key_points = [
        f"Premium Quality: {title} represents the pinnacle of engineering and design excellence",
        f"Unbeatable Value: Save {discount}% with our exclusive promotional pricing",
        f"Superior Performance: Engineered to exceed expectations in every aspect",
        f"Trusted Brand: Backed by manufacturer warranty and quality assurance",
        f"Customer Satisfaction: Join thousands of happy customers worldwide",
        f"Fast Delivery: Quick shipping from our efficient warehouse network",
        f"Secure Shopping: Safe and encrypted payment processing for your peace of mind",
        f"Expert Support: Dedicated customer service team ready to assist you",
        f"Latest Technology: Features cutting-edge innovations and modern design",
        f"Best Price Guaranteed: Competitive pricing with exceptional value proposition"
    ]
    
    return paragraphs, key_points


def create_product_pdf(product_id, output_dir):
    """Create a marketing PDF for a specific product"""
    
    try:
        # Get product details
        product = products_lib.get_product(product_id)
        if not product:
            print(f"❌ Product {product_id} not found")
            return False
        
        # Create PDF
        pdf_path = output_dir / f"{product_id}.pdf"
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#1a5490'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        )
        
        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=styles['BodyText'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=8,
            leading=14
        )
        
        price_style = ParagraphStyle(
            'PriceStyle',
            parent=styles['Normal'],
            fontSize=18,
            textColor=HexColor('#27ae60'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=20
        )
        
        # Add title
        elements.append(Paragraph(product['title'], title_style))
        elements.append(Paragraph(f"Product ID: {product_id}", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add pricing information
        if product.get('item_discount', 0) > 0:
            discounted_price = product['unit_price'] * (1 - product['item_discount'] / 100)
            price_text = f"<strike>₹{product['unit_price']:,.2f}</strike> &nbsp; ₹{discounted_price:,.2f} ({product['item_discount']}% OFF)"
        else:
            price_text = f"₹{product['unit_price']:,.2f}"
        elements.append(Paragraph(price_text, price_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Generate marketing content
        paragraphs, key_points = generate_marketing_content(product)
        
        # Add marketing paragraphs
        elements.append(Paragraph("Product Overview", heading_style))
        for para in paragraphs:
            elements.append(Paragraph(para, body_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Add key selling points
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Key Features & Benefits", heading_style))
        for i, point in enumerate(key_points, 1):
            elements.append(Paragraph(f"• {point}", bullet_style))
        
        # Add product specifications
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Product Specifications", heading_style))
        
        specs = [
            f"<b>Product ID:</b> {product['product_id']}",
            f"<b>Description:</b> {product['description']}",
            f"<b>Available Stock:</b> {product['units_in_stock']} units",
            f"<b>Warehouse Location:</b> {product.get('warehouse_name', 'N/A')}",
            f"<b>Status:</b> {'Active' if product.get('active') else 'Inactive'}"
        ]
        
        for spec in specs:
            elements.append(Paragraph(spec, bullet_style))
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=HexColor('#7f8c8d'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Generated on: {product.get('created_at', 'N/A')} | All prices are inclusive of applicable taxes",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        print(f"✓ Created PDF: {pdf_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating PDF for {product_id}: {str(e)}")
        return False


def main():
    """Main function to generate all product PDFs"""
    
    # Define output directory
    output_dir = Path(__file__).parent.parent / "product-docs"
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating marketing PDFs for {len(PRODUCT_IDS)} products...")
    print(f"Output directory: {output_dir}\n")
    
    success_count = 0
    failed_count = 0
    
    for product_id in PRODUCT_IDS:
        if create_product_pdf(product_id, output_dir):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"PDF Generation Complete!")
    print(f"✓ Successfully created: {success_count} PDFs")
    if failed_count > 0:
        print(f"❌ Failed: {failed_count} PDFs")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
