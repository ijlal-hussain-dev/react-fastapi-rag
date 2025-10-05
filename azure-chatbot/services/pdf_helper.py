from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import random

# Sample customer data
CUSTOMERS = [
    # US
    {"name": "John Doe", "location": "New York, NY, USA", "phone": "+1-555-1010"},
    {"name": "Jane Smith", "location": "Los Angeles, CA, USA", "phone": "+1-555-2020"},
    {"name": "Alice Johnson", "location": "Chicago, IL, USA", "phone": "+1-555-3030"},

    # UK
    {"name": "William Brown", "location": "London, UK", "phone": "+44-20-7946-0011"},
    {"name": "Emma Wilson", "location": "Manchester, UK", "phone": "+44-161-496-0022"},
    {"name": "Oliver Taylor", "location": "Birmingham, UK", "phone": "+44-121-496-0033"},

    # Germany
    {"name": "Sophie Müller", "location": "Berlin, Germany", "phone": "+49-30-123-4567"},
    {"name": "Maximilian Schmidt", "location": "Munich, Germany", "phone": "+49-89-987-6543"},
    {"name": "Lena Fischer", "location": "Hamburg, Germany", "phone": "+49-40-456-7890"},

    # Pakistan
    {"name": "Imran Khan", "location": "Islamabad, Pakistan", "phone": "+92-51-555-0133"},
    {"name": "Nasir Ali", "location": "Karachi, Pakistan", "phone": "+92-21-555-4204"},
    {"name": "Sana Mirza", "location": "Lahore, Pakistan", "phone": "+92-42-555-0102"},

    # India
    {"name": "Philip John Kumar", "location": "Delhi, India", "phone": "+91-11-555-1010"},
    {"name": "Priya Sharma", "location": "Mumbai, India", "phone": "+91-22-555-2020"},
    {"name": "Amit Singh", "location": "Bangalore, India", "phone": "+91-80-555-3030"},

    # Estonia
    {"name": "Mart Tamm", "location": "Tallinn, Estonia", "phone": "+372-555-0101"},
    {"name": "Katrin Saar", "location": "Tartu, Estonia", "phone": "+372-555-0102"},

    # Canada
    {"name": "Lucas Martin", "location": "Toronto, ON, Canada", "phone": "+1-416-555-0101"},
    {"name": "Olivia Thompson", "location": "Vancouver, BC, Canada", "phone": "+1-604-555-0202"},

    # Australia
    {"name": "Liam O’Connor", "location": "Sydney, Australia", "phone": "+61-2-5550-1010"},
    {"name": "Chloe Smith", "location": "Melbourne, Australia", "phone": "+61-3-5550-2020"}
]


DESCRIPTIONS = [
    "Payment due for consulting services in September.",
    "Invoice for software subscription and support.",
    "Payment for office supplies and equipment.",
    "Invoice for website design and maintenance.",
    "Consulting fee for financial advisory services."
]

EXTRA_CONTENT = [
    """
    Terms and Conditions:
    1. Payment is due within 30 days of invoice date.
    2. Late payments may incur additional charges.
    3. Services provided are subject to client agreement.
    4. This document serves as both an invoice and a receipt once paid.
    """,
    """
    Detailed Items:
    - Consulting service: 20 hours @ $100/hour
    - Travel expenses: $500
    - Miscellaneous charges: $200
    """,
    """
    Notes:
    Thank you for your business. Please contact accounts@company.com for inquiries.
    """,
    """
    Company Policy:
    All invoices are generated electronically and no signature is required.
    Refunds are processed within 14 working days if applicable.
    """
]

async def generate_pdf_bytes(invoice_id: str, customer_index: int) -> bytes:
    """
    Generates a random multi-page invoice PDF as bytes.
    """
    if customer_index < len(CUSTOMERS):
        customer = CUSTOMERS[customer_index]  # sequential
    else:
        customer = random.choice(CUSTOMERS)  # random after first 20
    description = random.choice(DESCRIPTIONS)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Page 1: Invoice summary
    c.drawString(50, 750, f"Invoice ID: {invoice_id}")
    c.drawString(50, 730, f"Customer: {customer['name']}")
    c.drawString(50, 710, f"Location: {customer['location']}")
    c.drawString(50, 690, f"Phone: {customer['phone']}")
    c.drawString(50, 670, f"Description: {description}")
    c.showPage()

    # Page 2+: Add extra random content (to make document bigger)
    random.shuffle(EXTRA_CONTENT)
    for section in EXTRA_CONTENT:
        text_object = c.beginText(50, 750)
        text_object.setFont("Helvetica", 11)
        for line in section.strip().splitlines():
            text_object.textLine(line.strip())
        c.drawText(text_object)
        c.showPage()

    c.save()

    buffer.seek(0)
    return buffer.read()

