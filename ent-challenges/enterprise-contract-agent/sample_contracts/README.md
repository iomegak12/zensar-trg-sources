# Sample Contract Documents

This folder contains sample contract PDFs for testing the Intelligent Contract Analysis Agent.

## Available Contracts

1. **nda_standard.pdf** - Standard Non-Disclosure Agreement
   - Clean, professional NDA
   - No PII, basic confidentiality terms
   - Complexity: Simple

2. **saas_agreement.pdf** - Software as a Service Agreement
   - SaaS subscription terms
   - Pricing, SLAs, termination clauses
   - Complexity: Moderate

3. **employment_contract.pdf** - Employment Agreement
   - Job offer with salary, benefits, non-compete
   - Standard employment terms
   - Complexity: Moderate

4. **nda_with_pii.pdf** - NDA with Personal Information
   - Contains PII for security testing (names, emails, SSN, phone numbers)
   - Used to test PII detection and redaction
   - Complexity: Simple (but sensitive)

5. **partnership_agreement.pdf** - Complex Partnership Agreement
   - Multi-party business partnership
   - Revenue sharing, IP rights, governance
   - Complexity: Advanced

## Note on PDF Generation

Since we're creating these programmatically, you can use the provided Python script to generate actual PDFs:

```bash
python scripts/generate_sample_pdfs.py
```

This will create all 5 PDF files with realistic contract content formatted professionally.
