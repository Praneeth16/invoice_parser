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

st.title("Invoice Parser Comparison: Azure vs LlamaParse")

# Add some helpful information
st.markdown("""
Compare invoice parsing capabilities between:

    Azure Document Intelligence by Microsoft Azure
    LlamaParse by Llama-Index

""") 

# Initialize parsers
azure_parser = AzureInvoiceParser()
llama_parser = LlamaInvoiceParser()

# File uploader
uploaded_file = st.file_uploader("Upload an invoice", type=["pdf"])

if uploaded_file is not None:
    with st.expander("View Invoice"):
        pdf_viewer(uploaded_file.getvalue())

    # Create two columns for results
    col1, col2 = st.columns(2, border=True)
    
    with col1:
        st.header("Azure Document Intelligence")
        try:
            # Read the file content
            file_content = uploaded_file.read()
            
            # Parse the invoice
            with st.spinner("Parsing invoice..."):
                start_time = time.perf_counter()
                extracted_data_azure = azure_parser.parse_invoice(file_content)
                end_time = time.perf_counter()
            
            if extracted_data_azure:
                st.subheader("Extracted Information")
                st.info(f"Time taken by Azure Document Intelligence: {int(end_time - start_time)} seconds")
                st.json(extracted_data_azure)
            else:
                st.warning("No data could be extracted from the invoice.")
                
        except Exception as e:
            st.error(str(e))
    
    with col2:
        st.header("LlamaParse")
        try:
            # Read the file content again (since it was consumed by Azure parser)
            uploaded_file.seek(0)
            file_content = uploaded_file.read()
            
            # Parse the invoice
            with st.spinner("Parsing invoice..."):
                start_time = time.perf_counter()
                extracted_data_llama = llama_parser.parse_invoice(file_content)
                end_time = time.perf_counter()
            
            if extracted_data_llama:
                st.subheader("Extracted Information")
                st.info(f"Time taken by LlamaParse: {int(end_time - start_time)} seconds")
                st.json(extracted_data_llama)
            else:
                st.warning("No data could be extracted from the invoice.")
                
        except Exception as e:
            st.error(str(e))

