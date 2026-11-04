"""
Script to generate 4 high-quality structured policy PDFs for SnapStore in the knowledge/ directory.
Combined with the existing Policy.pdf, this provides 5 comprehensive knowledge base documents.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

knowledge_dir = Path("knowledge")
knowledge_dir.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=18,
    leading=22,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontSize=9,
    leading=12,
    fontName='Helvetica-Oblique',
    textColor=colors.HexColor('#64748B'),
    spaceAfter=14
)

h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontSize=13,
    leading=17,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#1E40AF'),
    spaceBefore=10,
    spaceAfter=4
)

h3_style = ParagraphStyle(
    'DocH3',
    parent=styles['Heading3'],
    fontSize=10.5,
    leading=14,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#334155'),
    spaceBefore=6,
    spaceAfter=2
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    fontName='Helvetica',
    textColor=colors.HexColor('#1E293B'),
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'DocBullet',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    fontName='Helvetica',
    textColor=colors.HexColor('#334155'),
    leftIndent=14,
    spaceAfter=2
)

def build_pdf(filepath: Path, title: str, subtitle: str, sections: list):
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    story = [
        Paragraph(title, title_style),
        Paragraph(subtitle, subtitle_style),
        Spacer(1, 4)
    ]
    for sec in sections:
        story.append(Paragraph(sec['h2'], h2_style))
        for item in sec.get('content', []):
            if isinstance(item, tuple):
                # (heading3, body_text_or_list)
                story.append(Paragraph(item[0], h3_style))
                if isinstance(item[1], list):
                    for b in item[1]:
                        story.append(Paragraph(f"&bull; {b}", bullet_style))
                else:
                    story.append(Paragraph(item[1], body_style))
            elif isinstance(item, str):
                story.append(Paragraph(item, body_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    print(f"Built: {filepath}")

# 1. Shipping and Delivery Policy
shipping_sections = [
    {
        'h2': '1. Domestic Delivery Options and Fulfillment Timelines',
        'content': [
            'SnapStore operates regional fulfillment centers across the United States to ensure rapid dispatch and delivery.',
            ('Standard Ground Shipping', [
                'Free delivery on all domestic retail orders exceeding $50.00 USD after discounts.',
                'Orders below $50.00 incur a standard flat shipping fee of $4.99 USD.',
                'Delivery transit window is 3 to 5 business days via FedEx, UPS, or USPS ground networks.',
                'Delivery operates Monday through Saturday, from 8:00 AM to 8:00 PM local time.'
            ]),
            ('Express Air Shipping', [
                'Guaranteed expedited delivery within 1 to 2 business days for a flat surcharge of $14.99 USD.',
                'Same-day fulfillment dispatch cutoff is 2:00 PM EST Monday through Friday.',
                'Weekend delivery is supported in select metropolitan regions at no additional fee.'
            ]),
            ('Same-Day Metro Courier Delivery', [
                'Available in major metro areas including New York, Los Angeles, Chicago, Houston, and Miami.',
                'Orders confirmed prior to 11:00 AM local time arrive by 9:00 PM on the same calendar day.',
                'Fee is $19.99 flat, or discounted to $9.99 for verified SnapStore Prime membership holders.'
            ])
        ]
    },
    {
        'h2': '2. Order Tracking, Dispatch, and Address Modifications',
        'content': [
            ('Tracking Identifier Activation', [
                'Digital tracking codes are activated within 2 to 4 hours of physical barcode scanning at fulfillment hubs.',
                'Customers receive live tracking updates via automated email and push notifications in the SnapStore mobile app.'
            ]),
            ('Address Correction Window', [
                'Shipping destinations can be updated freely through the user portal within 30 minutes of checkout.',
                'Once an order reaches "Fulfillment In Progress" status, address changes require a carrier package intercept with a $12.50 fee.'
            ]),
            ('Multi-Hub Split Shipments', [
                'Items sourced from different regional fulfillment centers may arrive in separate packages with distinct tracking codes at zero extra cost.'
            ])
        ]
    },
    {
        'h2': '3. Lost, Delayed, or Stolen Packages in Transit',
        'content': [
            ('Premature Delivery Scan Buffer', [
                'If a parcel is marked "Delivered" but is not physically present, customers must allow a 24-hour buffer for carrier scan reconciliation.'
            ]),
            ('Claims and Package Theft Protocol', [
                'Formal missing package claims must be filed within 14 calendar days of the estimated delivery date.',
                'SnapStore reviews carrier GPS coordinates at the delivery drop point. For verified porch theft exceeding $250.00 USD, a local police report number is required.'
            ]),
            ('Transit Damage Reporting', [
                'Visible exterior carton damage, crushing, or moisture exposure must be photographed and submitted to support within 48 hours of courier delivery.'
            ])
        ]
    },
    {
        'h2': '4. International Shipping and Customs Import Regulations',
        'content': [
            ('Eligible International Destinations', [
                'SnapStore ships to 65 global countries across the Americas, Europe, and Asia-Pacific.',
                'Standard international delivery takes 7 to 14 business days; Priority global express takes 3 to 5 business days.'
            ]),
            ('Customs Duties: DDP vs DDU Policies', [
                'Shipments to Canada, the United Kingdom, and European Union member states are delivered DDP (Delivered Duty Paid). All applicable tariffs, import taxes, and VAT are calculated and collected at checkout.',
                'Rest-of-world shipments are delivered DDU (Delivered Duty Unpaid); local import clearance fees are the sole responsibility of the customer.'
            ])
        ]
    }
]

# 2. Warranty and Repairs Policy
warranty_sections = [
    {
        'h2': '1. Standard Manufacturer Warranty Terms',
        'content': [
            'All brand-new consumer hardware and electronics purchased through SnapStore include comprehensive factory warranty protection.',
            ('Baseline 12-Month Hardware Protection', [
                'Every new electronic device carries a minimum 365-day limited warranty covering factory defects, internal component failure, and assembly errors.',
                'Refurbished or open-box certified items include a mandatory 90-day SnapStore certified warranty.'
            ]),
            ('Warranty Limitations and Exclusions', [
                'Standard warranties strictly exclude damage resulting from liquid immersion, drops, cracked displays, power surges, or unauthorized third-party teardowns.',
                'Altering firmware, unlocking bootloaders, or installing unauthorized operating systems voids warranty coverage in full.'
            ])
        ]
    },
    {
        'h2': '2. SnapStore Care+ Extended Protection Plans',
        'content': [
            ('Plan Tiers and Coverage Benefits', [
                'Customers may purchase 2-year or 3-year SnapStore Care+ coverage at checkout or within 30 days of hardware delivery.',
                'Care+ includes Accidental Damage from Handling (ADH), drops, cracked glass screens, and liquid spills.'
            ]),
            ('Service Deductibles and Claim Allowances', [
                'Screen repair deductible: $29.00 USD for smartphones, tablets, and smartwatches.',
                'Full unit replacement deductible: $99.00 USD for laptops, cameras, and major appliances.',
                'Subscribers are entitled to up to two (2) accidental damage claims per rolling 12-month period.'
            ])
        ]
    },
    {
        'h2': '3. Repair Submission and Diagnostic Workflows',
        'content': [
            ('Return Merchandise Authorization (RMA)', [
                'Claims must be logged through the Warranty Portal to obtain an official RMA number and prepaid insured shipping label.',
                'Customer hardware is routed to the SnapStore Central Diagnostic Lab in Dallas, TX.'
            ]),
            ('Turnaround Service Level Agreement (SLA)', [
                'Standard hardware diagnosis and repair takes 5 to 7 business days from receipt at the repair facility.',
                'Customers receive live tracking updates at each repair stage: Intake, Diagnostic, Component Replacement, Quality Assurance, and Return Dispatch.'
            ]),
            ('Customer Data Backup Notice', [
                'Technical diagnostics may require full factory firmware restoration. Customers must back up personal files, as SnapStore assumes zero liability for lost local data.'
            ])
        ]
    },
    {
        'h2': '4. Beyond Economical Repair (BER) and Replacements',
        'content': [
            ('Hardware Replacement Policy', [
                'If a defective unit cannot be repaired within 10 business days, SnapStore provides an identical brand-new or certified grade-A replacement unit.',
                'The replacement hardware carries forward the remaining balance of the original warranty or a fresh 90-day warranty, whichever is greater.'
            ]),
            ('Store Credit Buyout Option', [
                'If identical replacement models are out of stock, customers receive 100% of the original purchase amount in store credit or an immediate refund.'
            ])
        ]
    }
]

# 3. Payment and Billing Policy
payment_sections = [
    {
        'h2': '1. Authorized Payment Methods and Encryption Security',
        'content': [
            'SnapStore maintains strict financial compliance standards to protect customer monetary transactions.',
            ('Accepted Payment Options', [
                'Credit and Debit Cards: Visa, MasterCard, American Express, Discover, and JCB.',
                'Digital Wallet Integrations: Apple Pay, Google Pay, and PayPal Express Checkout.',
                'Buy Now Pay Later (BNPL): Klarna, Afterpay, and Affirm (split orders into 4 bi-weekly interest-free installments).'
            ]),
            ('Encryption and Security Standards', [
                'All transactions are processed through Level 1 PCI-DSS compliant tokenized gateways with 256-bit TLS encryption.',
                'Card Verification Values (CVV) are never stored or logged on SnapStore internal systems.'
            ])
        ]
    },
    {
        'h2': '2. Pre-Authorization Holds and Invoicing',
        'content': [
            ('Authorization vs Official Charge', [
                'Placing an order triggers a temporary bank authorization hold for the order amount.',
                'Actual financial capture occurs exclusively when items physically dispatch from the distribution hub.',
                'For canceled orders, authorization holds release within 3 to 5 business days per the issuing bank.'
            ]),
            ('Digital Tax Invoices', [
                'Official tax invoices containing corporate tax numbers and itemized tax breakdowns are generated within 60 minutes of shipment.',
                'Invoices can be downloaded in PDF format directly from Account > Order History.'
            ])
        ]
    },
    {
        'h2': '3. Gift Cards and Store Credit Terms',
        'content': [
            ('Digital Gift Card Guidelines', [
                'Purchased SnapStore gift cards never expire and are free from maintenance or dormancy fees.',
                'Gift cards cannot be redeemed for physical cash, except where required by applicable state law.'
            ]),
            ('Promotional Store Credits and Vouchers', [
                'Goodwill customer compensation credits and promotional discount codes expire exactly 90 calendar days from issuance.'
            ])
        ]
    },
    {
        'h2': '4. Price Matching and Post-Purchase Adjustments',
        'content': [
            ('7-Day Price Match Guarantee', [
                'If a purchased product drops in price on SnapStore within 7 calendar days of delivery, customers may request a refund for the price difference.',
                'Excludes Black Friday, Cyber Monday, flash sales, clearance items, and third-party marketplace listings.'
            ]),
            ('Chargeback and Dispute Policy', [
                'Customers must contact SnapStore Support prior to initiating bank disputes. Unjustified chargebacks while holding merchandise result in permanent account suspension.'
            ])
        ]
    }
]

# 4. Account Security and Privacy Policy
security_sections = [
    {
        'h2': '1. Account Authentication and Credential Requirements',
        'content': [
            'SnapStore prioritizes user identity security, data privacy, and fraud prevention across all touchpoints.',
            ('Password Complexity Standards', [
                'Passwords must be at least 12 characters long and include an uppercase letter, lowercase letter, number, and special symbol.',
                'Passwords cannot match account email addresses or contain easily guessable sequences.'
            ]),
            ('Two-Factor Authentication (2FA)', [
                '2FA is mandatory for accounts storing payment profiles or placing single orders exceeding $500.00 USD.',
                'Supported 2FA methods include TOTP authenticator apps (Google Authenticator, Authy, Microsoft Authenticator) and SMS verification.'
            ])
        ]
    },
    {
        'h2': '2. Suspicious Activity, Account Freezes, and Recovery',
        'content': [
            ('Automated Threat Detection', [
                'Our fraud detection engine locks accounts upon detecting abnormal IP addresses, credential stuffing, or simultaneous multi-location orders.'
            ]),
            ('Identity Verification and Unlocking Protocol', [
                'To recover a frozen account, users must verify identity through secondary recovery channels and upload government-issued photo ID.',
                'Account recovery reviews are completed by the Fraud Prevention Team within 12 to 24 business hours.'
            ]),
            ('Unauthorized Order Cancellation', [
                'If suspicious orders are detected, customers must report them within 2 hours to trigger courier package recall and payment reversal.'
            ])
        ]
    },
    {
        'h2': '3. Customer Data Privacy Rights (GDPR & CCPA Compliance)',
        'content': [
            ('Right to Data Access and Portability', [
                'Customers can request a complete export of their account history, addresses, and order logs via the Privacy Center.',
                'Data packages are compiled and delivered securely within 30 calendar days of verification.'
            ]),
            ('Right to Erasure (Account Deletion)', [
                'Account deletion permanently scrubs personal profiles, address books, and payment tokens.',
                'Financial transaction records required for statutory tax audits are archived in pseudonymized format for 7 years as legally mandated.'
            ])
        ]
    },
    {
        'h2': '4. Phishing Alerts and Customer Security Guidelines',
        'content': [
            ('Legitimate Communication Channels', [
                'All official customer communications originate exclusively from @snapstore.com or @support.snapstore.com domains.'
            ]),
            ('Zero-Trust Customer Protocol', [
                'SnapStore support representatives will NEVER request customer passwords, 2FA codes, or full 16-digit payment card numbers.',
                'Forward all phishing emails and fraudulent SMS messages immediately to security@snapstore.com.'
            ])
        ]
    }
]

if __name__ == '__main__':
    build_pdf(
        knowledge_dir / "Shipping_and_Delivery_Policy.pdf",
        "SnapStore Shipping, Fulfillment, and Delivery Policy",
        "Document ID: POL-SS-LOG-2026-V2 | Effective Date: January 1, 2026 | Logistics Operations Division",
        shipping_sections
    )
    build_pdf(
        knowledge_dir / "Warranty_and_Repairs_Policy.pdf",
        "SnapStore Hardware Warranty, Protection Plans, and Repair Services",
        "Document ID: POL-SS-WAR-2026-V1 | Technical Services & Customer Assurance Division",
        warranty_sections
    )
    build_pdf(
        knowledge_dir / "Payment_and_Billing_Policy.pdf",
        "SnapStore Payment Methods, Invoicing, and Billing Resolution Policy",
        "Document ID: POL-SS-FIN-2026-V3 | Financial Operations & Compliance Division",
        payment_sections
    )
    build_pdf(
        knowledge_dir / "Account_Security_and_Privacy_Policy.pdf",
        "SnapStore Customer Account Security, Authentication, and Privacy Protocols",
        "Document ID: POL-SS-SEC-2026-V1 | Information Security & User Trust Division",
        security_sections
    )
    print("All 4 policy PDFs built successfully!")
