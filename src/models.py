from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceItem(BaseModel):
    description: str = Field(..., description="Description of the item")
    quantity: Optional[float] = Field(None, description="Quantity of the item")
    unit_price: Optional[float] = Field(None, description="Unit price of the item")
    amount: Optional[float] = Field(None, description="Total amount for this item")

class InvoiceData(BaseModel):
    vendor_name: str = Field(..., description="Name of the vendor or company")
    invoice_id: str = Field(..., description="Invoice number or identifier")
    invoice_date: str = Field(..., description="Date when the invoice was issued")
    due_date: Optional[str] = Field(None, description="Due date for payment")
    total_amount: float = Field(..., description="Total amount of the invoice")
    items: List[InvoiceItem] = Field(..., description="List of items in the invoice") 