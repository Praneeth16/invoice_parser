from pydantic import BaseModel, Field
from typing import List, Optional

class MerchantDetails(BaseModel):
    name: str = Field(..., description="Name of the merchant/vendor/seller company issuing the invoice. This is typically found at the top of the invoice, in the header section, or labeled as 'From:', 'Vendor:', 'Seller:', 'Service Provider:', or 'Company Name:'")
    business_unit: Optional[str] = Field(None, description="Business unit or division of the merchant company issuing the invoice")
    tax_reg_number: Optional[str] = Field(None, description="Tax registration number of the merchant/vendor issuing the invoice. Often labeled as 'Tax Reg No:', 'VAT Registration:', 'Tax ID:', or 'GST No:'")
    tax_payer_id: Optional[str] = Field(None, description="Tax payer identification number of the merchant/vendor. May be labeled as 'TIN:', 'Tax Payer ID:', or 'Federal Tax ID:'")
    bank_account_number: Optional[str] = Field(None, description="Bank account number of the merchant/vendor for payment purposes. Usually found in payment details section")
    iban_number: Optional[str] = Field(None, description="International Bank Account Number (IBAN) of the merchant/vendor for international payments")
    address_line_1: Optional[str] = Field(None, description="Primary address line of the merchant/vendor company issuing the invoice. This is the seller's business address")
    city: Optional[str] = Field(None, description="City where the merchant/vendor company is located")
    country: Optional[str] = Field(None, description="Country where the merchant/vendor company is registered or operating from")
    post_code: Optional[str] = Field(None, description="Postal/ZIP code of the merchant/vendor company's address")
    email: Optional[str] = Field(None, description="Email address of the merchant/vendor company for business correspondence")

class BillToDetails(BaseModel):
    name: Optional[str] = Field(None, description="Name of the customer/client/buyer who is being billed. This is typically found in sections labeled 'Bill To:', 'Customer:', 'Client:', 'Buyer:', or 'Invoice To:' on the invoice")
    business_unit: Optional[str] = Field(None, description="Business unit or department of the customer company being billed")
    tax_reg_number: Optional[str] = Field(None, description="Tax registration number of the customer/client being billed. This is the buyer's tax identification")
    tax_payer_id: Optional[str] = Field(None, description="Tax payer identification number of the customer/client being billed")
    address_line_1: Optional[str] = Field(None, description="Primary address line of the customer/client being billed. This is where the invoice should be sent or where the buyer is located")
    city: Optional[str] = Field(None, description="City of the customer/client being billed")
    country: Optional[str] = Field(None, description="Country of the customer/client being billed")
    post_code: Optional[str] = Field(None, description="Postal/ZIP code of the customer/client's billing address")
    email: Optional[str] = Field(None, description="Email address of the customer/client being billed for invoice correspondence")

class InvoiceItem(BaseModel):
    description: str = Field(..., description="Description of the item, product, or service being invoiced. This appears in the line items section of the invoice")
    business_line: Optional[str] = Field(None, description="Business line, category, department, or product line that this item belongs to. May be labeled as 'Category:', 'Business Line:', 'Department:', or 'Product Type:'")
    quantity: Optional[float] = Field(None, description="Quantity or number of units of the item being billed")
    unit_price: Optional[float] = Field(None, description="Price per unit of the item before taxes and discounts")
    tax_rate: Optional[float] = Field(None, description="Tax or VAT rate percentage applicable for this specific item")
    tax_amount: Optional[float] = Field(None, description="Tax or VAT amount calculated for this specific item")
    gross_amount: Optional[float] = Field(None, description="Total amount for this item including taxes (gross = net + tax)")
    net_amount: Optional[float] = Field(None, description="Net amount for this item before taxes (quantity × unit_price - discount)")
    discount: Optional[float] = Field(None, description="Discount amount, promotional savings, or voucher reduction applied to this item")
    description_country_language: Optional[str] = Field(None, description="Item description translated into the local country language if different from the main description")

class TaxLineSummary(BaseModel):
    tax_rate: Optional[float] = Field(None, description="Tax or VAT rate percentage for this tax summary line, typically found in tax breakdown section")
    tax_amount: Optional[float] = Field(None, description="Total tax or VAT amount for this rate category, found in tax summary or totals section")
    gross_amount: Optional[float] = Field(None, description="Total gross amount for this tax rate category (taxable amount + tax)")
    net_amount: Optional[float] = Field(None, description="Total net amount (taxable base) for this tax rate category before tax")

class InvoiceData(BaseModel):
    merchant: MerchantDetails = Field(..., description="Complete details of the merchant/vendor/seller issuing the invoice. This is the company or entity providing goods/services and requesting payment")
    bill_to: Optional[BillToDetails] = Field(None, description="Complete details of the customer/client/buyer being billed. This is the entity that will receive the invoice and is responsible for payment. May be labeled as 'Bill To:', 'Customer Details:', or 'Invoice To:' on the document")
    invoice_id: str = Field(..., description="Unique invoice number or identifier, typically labeled as 'Invoice #:', 'Invoice No:', 'Bill No:', or 'Reference No:'")
    invoice_date: str = Field(..., description="Date when the invoice was issued in YYYY-MM-DD format, usually labeled as 'Invoice Date:', 'Issue Date:', or 'Bill Date:'")
    due_date: Optional[str] = Field(None, description="Payment due date in YYYY-MM-DD format, often labeled as 'Due Date:', 'Payment Due:', or 'Pay By:'")
    total_amount: float = Field(..., description="Final total amount to be paid including all taxes, fees, and charges. This is the bottom-line amount on the invoice")
    net_amount: Optional[float] = Field(None, description="Total net amount before taxes across all items and charges")
    tax_amount: Optional[float] = Field(None, description="Total tax amount across all items, usually shown in tax summary section")
    roundoff_amount: Optional[float] = Field(None, description="Rounding adjustment amount to arrive at the final total, may be positive or negative")
    gross_amount: Optional[float] = Field(None, description="Total gross amount including taxes but before any rounding adjustments")
    currency: Optional[str] = Field(None, description="Currency code (e.g., USD, EUR, GBP) or symbol used for all amounts on the invoice")
    payment_terms: Optional[str] = Field(None, description="Payment terms and conditions, such as 'Net 30', 'Due on Receipt', 'Payment within 15 days', etc.")
    items: List[InvoiceItem] = Field(..., description="List of all line items, products, services, or charges detailed in the invoice")
    tax_line_summaries: Optional[List[TaxLineSummary]] = Field(None, description="Summary breakdown of taxes by rate, typically found in a tax summary section showing different tax rates and their totals") 