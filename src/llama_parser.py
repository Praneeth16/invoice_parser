import os
import tempfile
from llama_cloud.types import ExtractConfig, ExtractMode
from llama_cloud_services import LlamaExtract, LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
from .models import InvoiceData

class LlamaInvoiceParser:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        self.extractor = LlamaExtract(api_key=self.api_key)
        self.parser = LlamaParse(api_key=self.api_key, 
                result_type="markdown", 
                auto_mode=True,
                auto_mode_trigger_on_image_in_page=True,
                auto_mode_trigger_on_table_in_page=True
                )

    def parse_invoice(self, file_content):
        """
        Parse an invoice using LlamaParse with structured output
        """
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(file_content.encode())
                temp_file_path = temp_file.name

            config = ExtractConfig(
                use_reasoning=True,
                extraction_mode=ExtractMode.MULTIMODAL,
                system_prompt="Extract the information from invoices uploaded as it is without changing any information and strictly do not change any numbers. Pay special attention to distinguish between merchant/vendor details (the company issuing the invoice) and bill-to/customer details (the company being billed)."
            )
            try:
                try:
                    agent = self.extractor.get_agent(name='invoice-agent')
                    if agent:
                        self.extractor.delete_agent(agent.id)
                except ApiError as e:
                    if e.status_code == 404:
                        pass
                    else:
                        raise
                
                agent = self.extractor.create_agent(name='invoice-agent', 
                    data_schema=InvoiceData, 
                    config=config
                    )

                #extract data from the document
                extracted_data = agent.extract(
                    temp_file_path,
                ).data

                print(extracted_data)
                
                # Convert to dictionary for display with new structure
                merchant_data = extracted_data.get('merchant', {})
                bill_to_data = extracted_data.get('bill_to', {})
                
                structured_data = {
                    "Merchant Details": {
                        "Name": merchant_data.get('name', ''),
                        "Business Unit": merchant_data.get('business_unit', ''),
                        "Tax Reg #": merchant_data.get('tax_reg_number', ''),
                        "Tax Payer ID": merchant_data.get('tax_payer_id', ''),
                        "Bank Account #": merchant_data.get('bank_account_number', ''),
                        "IBAN #": merchant_data.get('iban_number', ''),
                        "Address Line 1": merchant_data.get('address_line_1', ''),
                        "City": merchant_data.get('city', ''),
                        "Country": merchant_data.get('country', ''),
                        "Post Code": merchant_data.get('post_code', ''),
                        "Email": merchant_data.get('email', ''),
                    },
                    "Bill To Details": {
                        "Name": bill_to_data.get('name', '') if bill_to_data else '',
                        "Business Unit": bill_to_data.get('business_unit', '') if bill_to_data else '',
                        "Tax Reg #": bill_to_data.get('tax_reg_number', '') if bill_to_data else '',
                        "Tax Payer ID": bill_to_data.get('tax_payer_id', '') if bill_to_data else '',
                        "Address Line 1": bill_to_data.get('address_line_1', '') if bill_to_data else '',
                        "City": bill_to_data.get('city', '') if bill_to_data else '',
                        "Country": bill_to_data.get('country', '') if bill_to_data else '',
                        "Post Code": bill_to_data.get('post_code', '') if bill_to_data else '',
                        "Email": bill_to_data.get('email', '') if bill_to_data else '',
                    } if bill_to_data else None,
                    "Invoice Details": {
                        "Invoice ID": extracted_data.get('invoice_id', ''),
                        "Invoice Date": extracted_data.get('invoice_date', ''),
                        "Due Date": extracted_data.get('due_date', ''),
                        "Currency": extracted_data.get('currency', ''),
                        "Payment Terms": extracted_data.get('payment_terms', ''),
                    },
                    "Financial Summary": {
                        "Total Amount": extracted_data.get('total_amount', ''),
                        "Net Amount": extracted_data.get('net_amount', ''),
                        "Tax Amount": extracted_data.get('tax_amount', ''),
                        "Roundoff Amount": extracted_data.get('roundoff_amount', ''),
                        "Gross Amount": extracted_data.get('gross_amount', ''),
                    },
                    "Items": [
                        {
                            "Description": item.get('description', ''),
                            "Business Line": item.get('business_line', ''),
                            "Quantity": item.get('quantity', ''),
                            "Unit Price": item.get('unit_price', ''),
                            "Tax Rate": item.get('tax_rate', ''),
                            "Tax Amount": item.get('tax_amount', ''),
                            "Gross Amount": item.get('gross_amount', ''),
                            "Net Amount": item.get('net_amount', ''),
                            "Discount": item.get('discount', ''),
                            "Description Country Language": item.get('description_country_language', ''),
                        }
                        for item in extracted_data.get('items', [])
                    ],
                    "Tax Line Summaries": [
                        {
                            "Tax Rate": tls.get('tax_rate', ''),
                            "Tax Amount": tls.get('tax_amount', ''),
                            "Gross Amount": tls.get('gross_amount', ''),
                            "Net Amount": tls.get('net_amount', ''),
                        }
                        for tls in extracted_data.get('tax_line_summaries', [])
                    ] if extracted_data.get('tax_line_summaries') else []
                }
                
                return structured_data
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise Exception(f"Error processing with LlamaParse: {str(e)}")

    def pdf_to_markdown(self, file_content):
        """
        Convert PDF to Markdown using LlamaParse
        """
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name

            file_extractor = {".pdf": self.parser}
            documents = SimpleDirectoryReader(input_files=[temp_file_path], file_extractor=file_extractor).load_data()

            return documents
        except Exception as e:
            raise Exception(f"Error converting PDF to Markdown: {str(e)}")
        finally:
            os.unlink(temp_file_path)
