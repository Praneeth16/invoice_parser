import io
import time

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from src import AzureInvoiceParser, LlamaInvoiceParser

# Set page config
st.set_page_config(
    page_title="Invoice Parser Comparison",
    page_icon="📄",
    layout="wide"
)

# Initialize session state for caching
if 'parsed_results' not in st.session_state:
    st.session_state.parsed_results = {}

# Initialize parsers
azure_parser = AzureInvoiceParser()
llama_parser = LlamaInvoiceParser()

st.title("Invoice Parser Comparison: Azure vs LlamaParse")

# Add some helpful information
st.markdown("""
Compare invoice parsing capabilities between:

    Azure Document Intelligence by Microsoft Azure
    LlamaParse by Llama-Index

""") 

# File uploader
uploaded_file = st.file_uploader("Upload an invoice", type=["pdf"])

if uploaded_file is not None:
    # Calculate file hash for caching
    file_content = uploaded_file.read()
    
    with st.expander("View Invoice"):
        pdf_viewer(uploaded_file.getvalue())

    # Create two columns for results
    col1, col2, col3 = st.columns([3, 1, 1], border=True)
            
    with col1:
        st.header("LlamaParse Markdown Parsing")
        try:
                # Convert PDF to Markdown
            with st.spinner("Converting PDF to Markdown..."):
                start_time = time.perf_counter()
                markdown_data_llama = llama_parser.pdf_to_markdown(file_content)
                end_time = time.perf_counter()
                st.info(f"Time taken by LlamaParse Parsing: {int(end_time - start_time)} seconds")
            
            if markdown_data_llama:
                st.subheader("Markdown Content")
                st.markdown(markdown_data_llama[0].text)

            else:
                st.warning("No markdown data could be generated from the invoice.")
                
        except Exception as e:
            st.error(str(e))

    with col2:
        st.header("LlamaParse Structured Extraction")
        try:
            # Parse the invoice
            with st.spinner("Parsing invoice..."):
                start_time = time.perf_counter()
                extracted_data_llama = llama_parser.parse_invoice(file_content)
                end_time = time.perf_counter()
                st.info(f"Time taken by LlamaParse Extraction: {int(end_time - start_time)} seconds")
                
            if extracted_data_llama:
                st.subheader("Extracted Information")
                st.json(extracted_data_llama)
            else:
                st.warning("No data could be extracted from the invoice.")
                
        except Exception as e:
            st.error(str(e))

    with col3:
        st.header("Azure Document Intelligence")
        try:
            # Parse the invoice
            with st.spinner("Parsing invoice..."):
                start_time = time.perf_counter()
                extracted_data_azure = azure_parser.parse_invoice(file_content)
                end_time = time.perf_counter()
                st.info(f"Time taken by Azure Document Intelligence: {int(end_time - start_time)} seconds")
            
            if extracted_data_azure:
                st.subheader("Extracted Information")
                st.json(extracted_data_azure)
            else:
                st.warning("No data could be extracted from the invoice.")
                
        except Exception as e:
            st.error(str(e))