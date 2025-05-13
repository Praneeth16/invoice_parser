from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceItem(BaseModel):
    description: str = Field(..., description="Description of the item")
    quantity: Optional[float] = Field(None, description="Quantity of the item")
    unit_price: Optional[float] = Field(None, description="Unit price of the item")
    tax_rate: Optional[float] = Field(None, description="Tax or VAT rate applicable for this item")
    tax_amount: Optional[float] = Field(None, description="Tax or VAT amount for this item")
    gross_amount: Optional[float] = Field(None, description="Gross amount for this item")
    net_amount: Optional[float] = Field(None, description="Net amount for this item")
    discount: Optional[float] = Field(None, description="Discount or birthday voucher or saved amount on this item")
    description_country_language: Optional[str] = Field(None, description="Description in country language")

class TaxLineSummary(BaseModel):
    tax_rate: Optional[float] = Field(None, description="Tax or VAT rate for the summary line")
    tax_amount: Optional[float] = Field(None, description="Tax or VAT amount for the summary line")
    gross_amount: Optional[float] = Field(None, description="Gross amount for the summary line")
    net_amount: Optional[float] = Field(None, description="Net amount for the summary line")

class InvoiceData(BaseModel):
    vendor_name: str = Field(..., description="Name of the vendor or company")
    business_unit: Optional[str] = Field(None, description="Business Unit")
    tax_reg_number: Optional[str] = Field(None, description="Tax Registration Number")
    tax_payer_id: Optional[str] = Field(None, description="Tax Payer ID")
    bank_account_number: Optional[str] = Field(None, description="Bank Account Number")
    iban_number: Optional[str] = Field(None, description="IBAN Number")
    address_line_1: Optional[str] = Field(None, description="Address Line 1")
    city: Optional[str] = Field(None, description="City")
    country: Optional[str] = Field(None, description="Country")
    post_code: Optional[str] = Field(None, description="Post Code")
    email: Optional[str] = Field(None, description="Email")
    invoice_id: str = Field(..., description="Invoice number or identifier")
    invoice_date: str = Field(..., description="Date when the invoice was issued")
    due_date: Optional[str] = Field(None, description="Due date for payment")
    total_amount: float = Field(..., description="Total amount of the invoice")
    net_amount: Optional[float] = Field(None, description="Net amount of the invoice")
    tax_amount: Optional[float] = Field(None, description="Tax amount of the invoice")
    roundoff_amount: Optional[float] = Field(None, description="Roundoff amount of the invoice")
    gross_amount: Optional[float] = Field(None, description="Gross amount of the invoice")
    currency: Optional[str] = Field(None, description="Currency of the invoice")
    payment_terms: Optional[str] = Field(None, description="Payment terms")
    items: List[InvoiceItem] = Field(..., description="List of items in the invoice")
    tax_line_summaries: Optional[List[TaxLineSummary]] = Field(None, description="Tax line summaries") 