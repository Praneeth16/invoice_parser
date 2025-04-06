# Invoice Parser Comparison

This Streamlit application compares invoice parsing capabilities between Azure Document Intelligence and LlamaParse. It allows users to upload invoices and see how each service extracts and structures the information.

## Features

- Upload invoices in PDF, PNG, JPG, or JPEG format
- Side-by-side comparison of parsing results
- Structured output from Azure Document Intelligence
- Structured extraction from LlamaParse using the official Cloud API
- Visual display of uploaded images

## Architecture

This application uses a modular architecture:

- `src/models.py`: Pydantic models for structured data
- `src/azure_parser.py`: Azure Document Intelligence parser
- `src/llama_parser.py`: LlamaParse implementation using LlamaIndex Cloud
- `app.py`: Main Streamlit application

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API credentials:
   ```
   AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_azure_endpoint
   AZURE_DOCUMENT_INTELLIGENCE_KEY=your_azure_key
   LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Upload an invoice using the file uploader
3. View the parsed results from both services side by side

## Requirements

- Python 3.8+
- Azure Document Intelligence service
- LlamaParse API key from LlamaIndex Cloud
- Required Python packages (see requirements.txt)

## Notes

- Azure Document Intelligence provides structured data extraction using a pre-built invoice model
- LlamaParse uses LlamaIndex Cloud's document parsing and structured output extraction
- The app supports PDF, PNG, JPG, and JPEG formats
- Images are displayed when uploaded in image formats 