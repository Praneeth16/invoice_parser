# Invoice Parser Comparison

A Streamlit web application that compares invoice parsing capabilities between Azure Document Intelligence and LlamaParse.

## Features

- **Multi-Parser Support:** Compare results from Azure Document Intelligence and LlamaParse
- **Structured Data Extraction:** Extract key invoice information (vendor, invoice ID, amounts, line items)
- **Markdown Conversion:** Convert PDF invoices to readable markdown format
- **Visual PDF Viewing:** Built-in PDF viewer for uploaded invoices
- **Performance Metrics:** Track and display parsing time for each engine

## Setup

### Prerequisites

- Python 3.8+
- Azure Document Intelligence API access
- LlamaParse API access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/invoice_parser.git
cd invoice_parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_azure_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_azure_key
LLAMA_CLOUD_API_KEY=your_llama_api_key
```

## Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Open the provided URL in your browser (typically http://localhost:8501)

3. Upload an invoice PDF file using the file uploader

4. View the comparison results:
   - LlamaParse Markdown output
   - LlamaParse structured data extraction
   - (Azure functionality available but commented out in current version)

## Project Structure

- `app.py` - Main Streamlit application
- `src/` - Source code for parsers
  - `azure_parser.py` - Azure Document Intelligence integration
  - `llama_parser.py` - LlamaParse integration
  - `models.py` - Data models for structured output

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
