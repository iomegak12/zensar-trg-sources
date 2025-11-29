"""
Script to generate sample contract PDFs for testing the Contract Analysis Agent.
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime, timedelta
import os


def create_nda_standard():
    """Generate a standard NDA without PII"""
    filename = "nda_standard.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("NON-DISCLOSURE AGREEMENT", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Agreement text
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    content = [
        f"This Non-Disclosure Agreement (the \"Agreement\") is entered into as of {datetime.now().strftime('%B %d, %Y')}, by and between:",
        "",
        "<b>TechCorp Solutions Inc.</b> (\"Disclosing Party\"), a corporation organized under the laws of Delaware, and",
        "",
        "<b>InnovateLabs LLC</b> (\"Receiving Party\"), a limited liability company organized under the laws of California.",
        "",
        "<b>WHEREAS,</b> the Disclosing Party possesses certain confidential and proprietary information relating to its business operations, technology, and trade secrets;",
        "",
        "<b>WHEREAS,</b> the Receiving Party desires to receive such confidential information for the purpose of evaluating a potential business relationship;",
        "",
        "<b>NOW, THEREFORE,</b> in consideration of the mutual covenants and agreements herein contained, the parties agree as follows:",
        "",
        "<b>1. DEFINITION OF CONFIDENTIAL INFORMATION</b>",
        "",
        "\"Confidential Information\" means any data or information that is proprietary to the Disclosing Party and not generally known to the public, including but not limited to:",
        "",
        "• Technical data, trade secrets, know-how, research, product plans, products, developments, inventions, processes, formulas, techniques, designs, drawings, engineering, hardware configuration information",
        "• Software, source code, object code, algorithms, and documentation",
        "• Business information including customer lists, supplier lists, financial information, marketing plans, business strategies",
        "",
        "<b>2. OBLIGATIONS OF RECEIVING PARTY</b>",
        "",
        "The Receiving Party agrees to:",
        "",
        "a) Hold and maintain the Confidential Information in strict confidence;",
        "b) Not disclose the Confidential Information to third parties without prior written consent;",
        "c) Not use the Confidential Information except for the Purpose stated above;",
        "d) Protect the Confidential Information with the same degree of care used to protect its own confidential information, but in no case less than reasonable care.",
        "",
        "<b>3. TERM</b>",
        "",
        "This Agreement shall remain in effect for a period of three (3) years from the Effective Date, unless earlier terminated by either party with thirty (30) days written notice.",
        "",
        "<b>4. RETURN OF MATERIALS</b>",
        "",
        "Upon termination or upon request by the Disclosing Party, the Receiving Party shall promptly return all Confidential Information and any copies thereof.",
        "",
        "<b>5. GOVERNING LAW</b>",
        "",
        "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law provisions.",
        "",
        "<b>6. ENTIRE AGREEMENT</b>",
        "",
        "This Agreement constitutes the entire agreement between the parties concerning the subject matter hereof and supersedes all prior agreements and understandings.",
        "",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        "",
        "",
        "<b>DISCLOSING PARTY:</b> TechCorp Solutions Inc.",
        "",
        "By: _______________________",
        "Name: Chief Legal Officer",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>RECEIVING PARTY:</b> InnovateLabs LLC",
        "",
        "By: _______________________",
        "Name: General Counsel",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
    ]
    
    for line in content:
        if line:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Spacer(1, 0.15 * inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")


def create_saas_agreement():
    """Generate a SaaS subscription agreement"""
    filename = "saas_agreement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("SOFTWARE AS A SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    content = [
        f"This Software as a Service Agreement (\"Agreement\") is entered into as of {datetime.now().strftime('%B %d, %Y')}, between:",
        "",
        "<b>CloudServe Technologies Inc.</b> (\"Provider\"), and",
        "<b>Enterprise Solutions Corp.</b> (\"Customer\")",
        "",
        "<b>1. SERVICES PROVIDED</b>",
        "",
        "Provider agrees to provide Customer with access to its cloud-based enterprise resource planning software (the \"Service\") according to the terms of this Agreement.",
        "",
        "<b>2. SUBSCRIPTION PLANS AND PRICING</b>",
        "",
        "<b>2.1 Professional Plan:</b> $499/month per organization",
        "• Up to 100 users",
        "• 500 GB cloud storage",
        "• Standard support (24-hour response time)",
        "• Monthly data backup",
        "",
        "<b>2.2 Enterprise Plan:</b> $1,499/month per organization",
        "• Unlimited users",
        "• 5 TB cloud storage",
        "• Priority support (4-hour response time)",
        "• Daily data backup",
        "• Dedicated account manager",
        "• Custom integrations (up to 5)",
        "",
        "<b>2.3 Payment Terms:</b>",
        "• Invoices due within 30 days of issue date",
        "• Late payments subject to 1.5% monthly interest",
        "• Annual prepayment receives 15% discount",
        "",
        "<b>3. SERVICE LEVEL AGREEMENT (SLA)</b>",
        "",
        "<b>3.1 Uptime Guarantee:</b> Provider guarantees 99.9% uptime, measured monthly.",
        "",
        "<b>3.2 SLA Credits:</b>",
        "• 99.9% - 99.0% uptime: 10% monthly fee credit",
        "• 99.0% - 95.0% uptime: 25% monthly fee credit",
        "• Below 95.0% uptime: 50% monthly fee credit",
        "",
        "<b>3.3 Exclusions:</b> Downtime due to scheduled maintenance, force majeure, or Customer's actions is excluded from SLA calculations.",
        "",
        "<b>4. DATA SECURITY AND PRIVACY</b>",
        "",
        "Provider shall:",
        "• Encrypt all data in transit (TLS 1.3) and at rest (AES-256)",
        "• Maintain SOC 2 Type II certification",
        "• Comply with GDPR and CCPA requirements",
        "• Perform annual third-party security audits",
        "• Notify Customer of security breaches within 24 hours",
        "",
        "<b>5. INTELLECTUAL PROPERTY</b>",
        "",
        "All software, documentation, and related materials remain the exclusive property of Provider. Customer receives a non-exclusive, non-transferable license to use the Service during the subscription term.",
        "",
        "<b>6. TERM AND TERMINATION</b>",
        "",
        "<b>6.1 Initial Term:</b> 12 months from the Effective Date",
        "",
        "<b>6.2 Renewal:</b> Automatically renews for successive 12-month periods unless either party provides 60 days written notice of non-renewal.",
        "",
        "<b>6.3 Termination for Cause:</b> Either party may terminate immediately if the other party:",
        "• Materially breaches this Agreement and fails to cure within 30 days",
        "• Becomes insolvent or files for bankruptcy",
        "",
        "<b>6.4 Effect of Termination:</b>",
        "• Customer access to Service terminates immediately",
        "• Customer has 30 days to export data",
        "• Provider may delete Customer data after 90 days",
        "• No refunds for prepaid unused subscription periods",
        "",
        "<b>7. LIMITATION OF LIABILITY</b>",
        "",
        "Provider's total liability under this Agreement shall not exceed the fees paid by Customer in the 12 months preceding the claim. Provider is not liable for indirect, incidental, or consequential damages.",
        "",
        "<b>8. MODIFICATIONS</b>",
        "",
        "Provider may modify the Service with 30 days notice. Material adverse changes allow Customer to terminate without penalty within 30 days of notice.",
        "",
        "<b>9. GOVERNING LAW</b>",
        "",
        "This Agreement is governed by the laws of the State of New York, excluding conflict of law principles.",
        "",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement.",
        "",
        "",
        "<b>PROVIDER:</b> CloudServe Technologies Inc.",
        "By: _______________________",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>CUSTOMER:</b> Enterprise Solutions Corp.",
        "By: _______________________",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
    ]
    
    for line in content:
        if line:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Spacer(1, 0.15 * inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")


def create_employment_contract():
    """Generate an employment agreement"""
    filename = "employment_contract.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("EMPLOYMENT AGREEMENT", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    start_date = (datetime.now() + timedelta(days=30)).strftime('%B %d, %Y')
    
    content = [
        f"This Employment Agreement (\"Agreement\") is made as of {datetime.now().strftime('%B %d, %Y')}, between:",
        "",
        "<b>DataDrive Analytics Inc.</b> (\"Company\"), and",
        "<b>The Employee</b> (\"Employee\")",
        "",
        "<b>1. POSITION AND DUTIES</b>",
        "",
        f"The Company hereby employs Employee as <b>Senior Machine Learning Engineer</b>, commencing on {start_date}.",
        "",
        "Employee shall:",
        "• Lead development of ML models and data pipelines",
        "• Mentor junior engineers and contribute to technical architecture",
        "• Collaborate with product and engineering teams",
        "• Report to the VP of Engineering",
        "",
        "<b>2. COMPENSATION</b>",
        "",
        "<b>2.1 Base Salary:</b> $165,000 per year, paid bi-weekly",
        "",
        "<b>2.2 Annual Bonus:</b> Target 15% of base salary, based on individual and company performance",
        "",
        "<b>2.3 Equity:</b> 20,000 stock options with 4-year vesting (25% after year 1, then monthly)",
        "",
        "<b>2.4 Sign-On Bonus:</b> $15,000, payable with first paycheck. Must be repaid if Employee leaves within 12 months.",
        "",
        "<b>3. BENEFITS</b>",
        "",
        "Employee is eligible for:",
        "• Health, dental, and vision insurance (Company pays 90% of premiums)",
        "• 401(k) with 4% company match",
        "• 20 days PTO (increases to 25 days after 3 years)",
        "• 10 paid holidays",
        "• $2,000 annual professional development budget",
        "• Remote work flexibility (2 days/week)",
        "",
        "<b>4. CONFIDENTIALITY</b>",
        "",
        "Employee agrees to maintain confidentiality of all Company proprietary information, including but not limited to:",
        "• Technical algorithms, source code, and system architectures",
        "• Customer data, business strategies, and financial information",
        "• Product roadmaps and development plans",
        "",
        "This obligation survives termination of employment.",
        "",
        "<b>5. INTELLECTUAL PROPERTY</b>",
        "",
        "All inventions, discoveries, and works created by Employee during employment and relating to Company's business belong exclusively to the Company.",
        "",
        "<b>6. NON-COMPETE AND NON-SOLICITATION</b>",
        "",
        "<b>6.1 Non-Compete:</b> For 12 months after termination, Employee shall not:",
        "• Work for direct competitors in a similar role",
        "• Start a competing business in the same market segment",
        "",
        "<b>Geographic Scope:</b> United States and Canada",
        "",
        "<b>6.2 Non-Solicitation:</b> For 18 months after termination, Employee shall not:",
        "• Solicit Company employees to leave",
        "• Solicit Company customers for competing services",
        "",
        "<b>7. AT-WILL EMPLOYMENT</b>",
        "",
        "This is an at-will employment relationship. Either party may terminate employment at any time, with or without cause, upon 2 weeks written notice.",
        "",
        "<b>8. SEVERANCE</b>",
        "",
        "If Company terminates Employee without cause:",
        "• 3 months base salary severance",
        "• Extended health benefits for 3 months",
        "• Accelerated vesting of 25% unvested stock options",
        "",
        "No severance if termination is for cause or Employee resigns.",
        "",
        "<b>9. DISPUTE RESOLUTION</b>",
        "",
        "Any disputes shall be resolved through binding arbitration under AAA rules, in San Francisco, California.",
        "",
        "<b>10. ENTIRE AGREEMENT</b>",
        "",
        "This Agreement supersedes all prior understandings and constitutes the entire agreement between the parties.",
        "",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement.",
        "",
        "",
        "<b>COMPANY:</b> DataDrive Analytics Inc.",
        "By: _______________________",
        "Name: Chief Human Resources Officer",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>EMPLOYEE:</b>",
        "Signature: _______________________",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
    ]
    
    for line in content:
        if line:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Spacer(1, 0.15 * inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")


def create_nda_with_pii():
    """Generate an NDA with PII for security testing"""
    filename = "nda_with_pii.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("NON-DISCLOSURE AGREEMENT", title_style))
    story.append(Paragraph("⚠️ CONTAINS PII FOR TESTING PURPOSES", styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))
    
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    content = [
        f"This Non-Disclosure Agreement is entered into on {datetime.now().strftime('%B %d, %Y')}, between:",
        "",
        "<b>Personal Information:</b>",
        "• Full Name: Jennifer Marie Thompson",
        "• Social Security Number: 123-45-6789",
        "• Date of Birth: March 15, 1985",
        "• Email: jennifer.thompson@personalemail.com",
        "• Phone: +1 (415) 555-0123",
        "• Address: 742 Evergreen Terrace, San Francisco, CA 94102",
        "",
        "AND",
        "",
        "• Full Name: Michael Robert Chen",
        "• Social Security Number: 987-65-4321",
        "• Date of Birth: July 22, 1978",
        "• Email: michael.chen@corporateemail.com",
        "• Phone: +1 (408) 555-9876",
        "• Address: 1234 Innovation Drive, Palo Alto, CA 94301",
        "",
        "<b>WHEREAS,</b> Jennifer Thompson (\"Disclosing Party\") possesses confidential information related to a proprietary software algorithm for healthcare data analysis;",
        "",
        "<b>WHEREAS,</b> Michael Chen (\"Receiving Party\") wishes to evaluate this technology for potential acquisition;",
        "",
        "<b>1. CONFIDENTIAL INFORMATION</b>",
        "",
        "Confidential Information includes the following sensitive data:",
        "• Patient healthcare records (HIPAA protected)",
        "• Credit card information: 4532-1234-5678-9010 (exp. 12/25, CVV: 123)",
        "• Bank account: Wells Fargo #9876543210, Routing #121000248",
        "• Passport Number: 123456789 (USA)",
        "• Driver's License: CA D1234567",
        "",
        "<b>2. EMERGENCY CONTACTS</b>",
        "",
        "In case of breach notification:",
        "• Jennifer Thompson: jennifer.thompson@personalemail.com, (415) 555-0123",
        "• Legal Counsel: Sarah Martinez, sarah.martinez@lawfirm.com, (650) 555-7890",
        "• Compliance Officer: David Kim, SSN: 456-78-9012, david.kim@compliance.com",
        "",
        "<b>3. OBLIGATIONS</b>",
        "",
        "The Receiving Party shall protect all PII and PHI in accordance with:",
        "• GDPR (EU General Data Protection Regulation)",
        "• HIPAA (Health Insurance Portability and Accountability Act)",
        "• CCPA (California Consumer Privacy Act)",
        "",
        "<b>4. DATA BREACH PROTOCOL</b>",
        "",
        "Any unauthorized disclosure must be reported within 72 hours to:",
        "• Jennifer Thompson: (415) 555-0123",
        "• Data Protection Officer: privacy@company.com",
        "• Affected individuals whose SSN, credit cards, or health data was exposed",
        "",
        "<b>5. GOVERNING LAW</b>",
        "",
        "This Agreement is governed by California law and is subject to federal privacy regulations.",
        "",
        "",
        "EXECUTED as of the date first written above.",
        "",
        "",
        "<b>DISCLOSING PARTY:</b>",
        "Signature: _______________________",
        "Name: Jennifer Marie Thompson",
        "SSN: 123-45-6789",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>RECEIVING PARTY:</b>",
        "Signature: _______________________",
        "Name: Michael Robert Chen",
        "SSN: 987-65-4321",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
    ]
    
    for line in content:
        if line:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.1 * inch))
        else:
            story.append(Spacer(1, 0.15 * inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")


def create_partnership_agreement():
    """Generate a complex partnership agreement"""
    filename = "partnership_agreement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("STRATEGIC PARTNERSHIP AGREEMENT", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    content = [
        f"This Strategic Partnership Agreement is entered into as of {datetime.now().strftime('%B %d, %Y')}, among:",
        "",
        "<b>Party A:</b> QuantumLeap AI Technologies Inc. (\"QuantumLeap\")",
        "<b>Party B:</b> GlobalData Solutions Corp. (\"GlobalData\")",
        "<b>Party C:</b> Enterprise Cloud Systems LLC (\"ECS\")",
        "",
        "Collectively referred to as the \"Partners\" or \"Alliance\".",
        "",
        "<b>RECITALS</b>",
        "",
        "WHEREAS, QuantumLeap specializes in advanced machine learning algorithms and AI model development;",
        "",
        "WHEREAS, GlobalData operates extensive data infrastructure and has relationships with Fortune 500 customers;",
        "",
        "WHEREAS, ECS provides enterprise cloud deployment platforms and security frameworks;",
        "",
        "WHEREAS, the Partners desire to combine their complementary capabilities to create an integrated AI-powered analytics platform for enterprise customers;",
        "",
        "NOW, THEREFORE, in consideration of the mutual covenants herein, the Partners agree:",
        "",
        "<b>1. PARTNERSHIP STRUCTURE AND GOVERNANCE</b>",
        "",
        "<b>1.1 Joint Venture Entity:</b> Partners shall form \"AI Analytics Alliance LLC\" (the \"JV\") under Delaware law.",
        "",
        "<b>1.2 Ownership:</b>",
        "• QuantumLeap: 40% equity interest",
        "• GlobalData: 35% equity interest",
        "• ECS: 25% equity interest",
        "",
        "<b>1.3 Governance Board:</b>",
        "• 6-member board: 2 from QuantumLeap, 2 from GlobalData, 2 from ECS",
        "• Decisions require 4/6 supermajority for: capital raises >$5M, M&A, dissolution",
        "• Simple majority (3/6) for operational decisions",
        "• Quarterly board meetings mandatory",
        "",
        "<b>1.4 Management:</b>",
        "• CEO appointed by QuantumLeap (subject to board approval)",
        "• CFO appointed by GlobalData",
        "• CTO appointed by ECS",
        "",
        "<b>2. CAPITAL CONTRIBUTIONS</b>",
        "",
        "<b>2.1 Initial Contributions (within 30 days of execution):</b>",
        "• QuantumLeap: $8,000,000 cash + AI technology IP (valued at $12,000,000)",
        "• GlobalData: $7,000,000 cash + customer relationships and data assets (valued at $7,000,000)",
        "• ECS: $5,000,000 cash + cloud infrastructure licenses (valued at $5,000,000)",
        "",
        "Total JV capitalization: $44,000,000",
        "",
        "<b>2.2 Future Funding:</b> Additional capital calls pro-rata to ownership, or dilution occurs.",
        "",
        "<b>3. REVENUE SHARING AND FINANCIALS</b>",
        "",
        "<b>3.1 Revenue Distribution Model:</b>",
        "",
        "Year 1-2 (Growth Phase):",
        "• All revenue reinvested in JV operations",
        "• No distributions to Partners",
        "",
        "Year 3+ (Profit Sharing Phase):",
        "• 60% of net profits distributed quarterly, pro-rata to ownership",
        "• 40% retained for R&D and expansion",
        "",
        "<b>3.2 Revenue Attribution:</b>",
        "• Direct sales by JV: 100% to JV",
        "• Sales through Partner channels: JV receives 70%, Partner receives 30% commission",
        "• Existing customer upsells: Revenue split 50/50 between JV and Partner who owns customer relationship",
        "",
        "<b>3.3 Pricing Authority:</b>",
        "• Standard pricing: JV management decides",
        "• Discounts >20%: Requires board approval",
        "• Custom deals >$1M annually: Requires unanimous board approval",
        "",
        "<b>4. INTELLECTUAL PROPERTY RIGHTS</b>",
        "",
        "<b>4.1 Background IP:</b>",
        "• Each Partner retains ownership of IP contributed to JV",
        "• JV receives perpetual, royalty-free, exclusive license to use Background IP",
        "",
        "<b>4.2 Foreground IP:</b>",
        "• All new IP created by JV belongs to JV",
        "• Partners have non-exclusive right to use Foreground IP in their other businesses, subject to:",
        "  - Cannot compete directly with JV offerings",
        "  - Must pay 5% royalty on revenue from Foreground IP usage",
        "",
        "<b>4.3 Patents and Trade Secrets:</b>",
        "• Patent applications filed in JV's name",
        "• Partners jointly own patents, proportional to ownership stakes",
        "• Trade secrets remain confidential, shared only on need-to-know basis",
        "",
        "<b>5. EXCLUSIVITY AND COMPETITIVE RESTRICTIONS</b>",
        "",
        "<b>5.1 Non-Compete:</b> During partnership and for 2 years after, Partners shall not:",
        "• Develop or market products that directly compete with JV offerings",
        "• Partner with competitors to create similar solutions",
        "",
        "<b>5.2 Exceptions:</b>",
        "• Products in development before this Agreement (listed in Schedule A)",
        "• Acquisitions where target has competing products (board approval required)",
        "",
        "<b>5.3 Customer Exclusivity:</b>",
        "• Enterprise customers (>5,000 employees): JV has exclusive rights to AI analytics offerings",
        "• SMB customers (<5,000 employees): Partners may offer competing products",
        "",
        "<b>6. RESPONSIBILITIES AND OBLIGATIONS</b>",
        "",
        "<b>6.1 QuantumLeap shall:</b>",
        "• Provide 15 ML engineers for JV projects",
        "• Deliver quarterly AI model updates and improvements",
        "• Conduct 2 training sessions per year for JV sales teams",
        "",
        "<b>6.2 GlobalData shall:</b>",
        "• Grant JV access to anonymized training data (10PB minimum)",
        "• Introduce JV to 50 enterprise prospects within first year",
        "• Provide data engineering support (5 FTEs)",
        "",
        "<b>6.3 ECS shall:</b>",
        "• Host JV platform on its infrastructure at cost (no markup)",
        "• Provide 24/7 DevOps support and security monitoring",
        "• Maintain SOC 2 and ISO 27001 compliance",
        "",
        "<b>7. TERMINATION AND EXIT</b>",
        "",
        "<b>7.1 Term:</b> Initial term of 5 years, auto-renewing for successive 2-year periods.",
        "",
        "<b>7.2 Voluntary Exit:</b>",
        "• Any Partner may exit with 12 months written notice",
        "• Remaining Partners have right of first refusal to purchase exiting Partner's stake",
        "• Valuation: Independent appraisal by Big 4 accounting firm",
        "• Payment: 30% cash at closing, 70% in equal installments over 3 years",
        "",
        "<b>7.3 Forced Exit (for cause):</b>",
        "• Material breach not cured within 90 days",
        "• Bankruptcy or insolvency",
        "• Criminal indictment of Partner's executives",
        "• Remaining Partners can force buyout at 20% discount to fair market value",
        "",
        "<b>7.4 Dissolution:</b>",
        "• Requires unanimous consent or 2/3 vote if JV fails to achieve $10M revenue by end of Year 3",
        "• Assets distributed pro-rata after paying liabilities",
        "• IP rights revert to contributing Partners (Foreground IP jointly owned)",
        "",
        "<b>8. CONFIDENTIALITY AND DATA PROTECTION</b>",
        "",
        "• All Partner and JV confidential information protected for 5 years post-termination",
        "• Customer data handled per GDPR, CCPA, and SOC 2 requirements",
        "• Annual third-party security audits mandatory",
        "• Data breach notification within 48 hours to all Partners and affected customers",
        "",
        "<b>9. DISPUTE RESOLUTION</b>",
        "",
        "• Good faith negotiation (30 days)",
        "• Mediation (30 days)",
        "• Binding arbitration (AAA Commercial Rules, San Francisco, CA)",
        "• Governing Law: Delaware",
        "",
        "<b>10. REPRESENTATIONS AND WARRANTIES</b>",
        "",
        "Each Partner represents:",
        "• Full authority to enter this Agreement",
        "• No conflicts with existing obligations",
        "• Contributed IP is free of third-party claims",
        "• Financial statements provided are accurate",
        "",
        "",
        "IN WITNESS WHEREOF, the Partners have executed this Agreement.",
        "",
        "",
        "<b>QUANTUMLEAP AI TECHNOLOGIES INC.</b>",
        "By: _______________________",
        "Name: Chief Executive Officer",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>GLOBALDATA SOLUTIONS CORP.</b>",
        "By: _______________________",
        "Name: Chief Strategy Officer",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "",
        "<b>ENTERPRISE CLOUD SYSTEMS LLC</b>",
        "By: _______________________",
        "Name: Managing Director",
        f"Date: {datetime.now().strftime('%B %d, %Y')}",
    ]
    
    for line in content:
        if line:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 0.08 * inch))
        else:
            story.append(Spacer(1, 0.12 * inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")


if __name__ == "__main__":
    print("Generating sample contract PDFs...")
    print("-" * 50)
    
    create_nda_standard()
    create_saas_agreement()
    create_employment_contract()
    create_nda_with_pii()
    create_partnership_agreement()
    
    print("-" * 50)
    print("✅ All sample contracts generated successfully!")
    print("\nGenerated files:")
    print("  1. nda_standard.pdf")
    print("  2. saas_agreement.pdf")
    print("  3. employment_contract.pdf")
    print("  4. nda_with_pii.pdf (⚠️  Contains PII for testing)")
    print("  5. partnership_agreement.pdf")
