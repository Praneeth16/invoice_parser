import pandas as pd
from datetime import datetime
import io
import json

def convert_to_csv_data(extracted_data):
    """Convert extracted data to CSV-ready format"""
    csv_data = []
    
    # Add merchant details
    merchant = extracted_data.get("Merchant Details", {})
    if merchant:
        csv_data.append({
            "Section": "Merchant Details",
            "Field": "Name",
            "Value": merchant.get("Name", "")
        })
        for field, value in merchant.items():
            if field != "Name":
                csv_data.append({
                    "Section": "Merchant Details",
                    "Field": field,
                    "Value": value
                })
    
    # Add bill to details
    bill_to = extracted_data.get("Bill To Details")
    if bill_to:
        for field, value in bill_to.items():
            csv_data.append({
                "Section": "Bill To Details",
                "Field": field,
                "Value": value
            })
    
    # Add invoice details
    invoice_details = extracted_data.get("Invoice Details", {})
    for field, value in invoice_details.items():
        csv_data.append({
            "Section": "Invoice Details",
            "Field": field,
            "Value": value
        })
    
    # Add financial summary
    financial = extracted_data.get("Financial Summary", {})
    for field, value in financial.items():
        csv_data.append({
            "Section": "Financial Summary",
            "Field": field,
            "Value": value
        })
    
    # Add items
    items = extracted_data.get("Items", [])
    for i, item in enumerate(items):
        for field, value in item.items():
            csv_data.append({
                "Section": f"Item {i+1}",
                "Field": field,
                "Value": value
            })
    
    # Add tax summaries
    tax_summaries = extracted_data.get("Tax Line Summaries", [])
    for i, tax in enumerate(tax_summaries):
        for field, value in tax.items():
            csv_data.append({
                "Section": f"Tax Summary {i+1}",
                "Field": field,
                "Value": value
            })
    
    return pd.DataFrame(csv_data)

def create_summary_tables(extracted_data):
    """Create summary tables for better visualization"""
    tables = {}
    
    # Merchant Details Table
    merchant = extracted_data.get("Merchant Details", {})
    if merchant:
        merchant_df = pd.DataFrame([
            {"Field": field, "Value": value} 
            for field, value in merchant.items() if value
        ])
        tables["Merchant Details"] = merchant_df
    
    # Bill To Details Table
    bill_to = extracted_data.get("Bill To Details")
    if bill_to:
        bill_to_df = pd.DataFrame([
            {"Field": field, "Value": value} 
            for field, value in bill_to.items() if value
        ])
        tables["Bill To Details"] = bill_to_df
    
    # Invoice Details Table
    invoice_details = extracted_data.get("Invoice Details", {})
    if invoice_details:
        invoice_df = pd.DataFrame([
            {"Field": field, "Value": value} 
            for field, value in invoice_details.items() if value
        ])
        tables["Invoice Details"] = invoice_df
    
    # Financial Summary Table
    financial = extracted_data.get("Financial Summary", {})
    if financial:
        financial_df = pd.DataFrame([
            {"Field": field, "Value": value} 
            for field, value in financial.items() if value
        ])
        tables["Financial Summary"] = financial_df
    
    # Items Table
    items = extracted_data.get("Items", [])
    if items:
        items_df = pd.DataFrame(items)
        # Remove empty columns
        items_df = items_df.loc[:, (items_df != '').any(axis=0)]
        tables["Items"] = items_df
    
    # Tax Summaries Table
    tax_summaries = extracted_data.get("Tax Line Summaries", [])
    if tax_summaries:
        tax_df = pd.DataFrame(tax_summaries)
        tax_df = tax_df.loc[:, (tax_df != '').any(axis=0)]
        tables["Tax Line Summaries"] = tax_df
    
    return tables

def format_translation_markdown(translation_data):
    """Create formatted translation markdown content"""
    translation_markdown = f"# Invoice Translation\n\n"
    translation_markdown += f"**Source Language:** {translation_data['source_language']}\n\n"
    translation_markdown += f"**Translation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    translation_markdown += "---\n\n"
    
    for i, result in enumerate(translation_data['results']):
        translation_markdown += f"## Page {i+1}\n\n"
        translation_markdown += result['translated_text']
        translation_markdown += "\n\n---\n\n"
    
    return translation_markdown

def format_markdown_content(markdown_data):
    """Combine markdown content from multiple pages"""
    return "\n\n---\n\n".join([doc.text for doc in markdown_data])

def convert_dataframe_to_csv_string(dataframe):
    """Convert pandas DataFrame to CSV string"""
    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def filter_empty_values(data_dict):
    """Remove empty values from dictionary"""
    return {k: v for k, v in data_dict.items() if v}

def format_currency_value(value):
    """Format currency values for display"""
    if value is None or value == '':
        return ''
    try:
        if isinstance(value, (int, float)):
            return f"{value:,.2f}"
        return str(value)
    except:
        return str(value)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def create_comprehensive_csv_data(invoice_filename, extracted_data, bounding_box_data, markdown_data=None, translation_data=None):
    """Create comprehensive CSV with invoice filename, extracted JSON, bounding JSON, markdown text, and translated text"""
    
    # Combine markdown text from multiple pages
    markdown_text = ""
    if markdown_data:
        markdown_text = "\n\n".join([doc.text for doc in markdown_data])
    
    # Combine translated text from multiple pages
    translated_text = ""
    if translation_data and translation_data.get('results'):
        translated_text = "\n\n".join([result['translated_text'] for result in translation_data['results']])
    
    csv_data = [{
        "Invoice_Filename": invoice_filename,
        "Markdown_Text": markdown_text,
        "Translated_Text": translated_text,
        "Extracted_JSON": json.dumps(extracted_data, indent=2) if extracted_data else "",
        "Bounding_Box_JSON": json.dumps(bounding_box_data, indent=2) if bounding_box_data else ""
    }]
    
    return pd.DataFrame(csv_data) 