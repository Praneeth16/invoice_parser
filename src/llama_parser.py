import os
import tempfile
from llama_cloud_services import LlamaExtract
from dotenv import load_dotenv
from .models import InvoiceData

class LlamaInvoiceParser:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        self.extractor = LlamaExtract(api_key=self.api_key)

    def parse_invoice(self, file_content):
        """
        Parse an invoice using LlamaParse with structured output
        """
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name

            try:
                try:
                    agent = self.extractor.get_agent(name='invoice-agent')
                except:
                    agent = self.extractor.create_agent(name='invoice-agent', data_schema=InvoiceData)

                #extract data from the document
                extracted_data = agent.extract(
                    temp_file_path,
                ).data

                print(extracted_data)
                
                # Convert to dictionary for display
                structured_data = {
                    "Vendor Name": extracted_data.get('vendor_name', ''),
                    "Invoice ID": extracted_data.get('invoice_id', ''),
                    "Invoice Date": extracted_data.get('invoice_date', ''),
                    "Due Date": extracted_data.get('due_date', ''),
                    "Total Amount": extracted_data.get('total_amount', ''),
                    "Items": [
                        {
                            "Description": item.get('description', ''),
                            "Quantity": item.get('quantity', ''),
                            "Unit Price": item.get('unit_price', ''),
                            "Amount": item.get('amount', '')
                        }
                        for item in extracted_data.get('items', [])
                    ]
                }
                
                return structured_data
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise Exception(f"Error processing with LlamaParse: {str(e)}") 
