import ast
import os
from io import BytesIO
import json

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

class AzureInvoiceParser:
    def __init__(self):
        load_dotenv()
        self.azure_endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.azure_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.client = DocumentIntelligenceClient(
            endpoint=self.azure_endpoint,
            credential=AzureKeyCredential(self.azure_key)
        )

    def parse_invoice(self, file_content):
        """
        Parse an invoice using Azure Document Intelligence
        """
        try:
            # Analyze the document
            poller = self.client.begin_analyze_document(
                "prebuilt-invoice",
                AnalyzeDocumentRequest(bytes_source=file_content),
            )
            result = poller.result()
            
            if not result.documents:
                return None
            #print(result.documents)  
            invoice = result.documents[0]
            
            # Create a dictionary to store extracted fields
            extracted_data = {
                "Vendor Name": invoice.fields.get("VendorName", {}).get("content", ''),
                "Invoice ID": invoice.fields.get("InvoiceId", {}).get("content", ''),
                "Invoice Date": invoice.fields.get("InvoiceDate", {}).get("content", ''),
                "Due Date": invoice.fields.get("DueDate", {}).get("content", ''),
                "Total Amount": invoice.fields.get("TotalAmount", {}).get("content", ''),
                "Items": []
            }
            print(extracted_data)
            # Extract line items
            for page in result.documents:
                for item in page.fields.get('Items', {}).get('valueArray', []):
                    item_data = {
                        "Description": item.get('valueObject').get("Description", {}).get("content", ''),
                        "Quantity": item.get('valueObject').get("Quantity", {}).get("content", ''),
                        "Unit Price": item.get('valueObject').get("UnitPrice", {}).get("content", ''),
                        "Amount": item.get('valueObject').get("Amount", {}).get("content", '')
                    }
                    extracted_data["Items"].append(item_data)
            
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Error processing with Azure Document Intelligence: {str(e)}") 