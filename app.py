import io
import time

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from src import AzureInvoiceParser, LlamaInvoiceParser
from src.translation import MarkdownTranslator

# Set page config
st.set_page_config(
    page_title="Invoice Parser",
    page_icon="📄",
    layout="wide"
)

# Initialize session state for caching
if 'parsed_results' not in st.session_state:
    st.session_state.parsed_results = {}

# Initialize parsers and translator
azure_parser = AzureInvoiceParser()
llama_parser = LlamaInvoiceParser()
translator = MarkdownTranslator()

st.title("Invoice Parser: LlamaParse")

# Add some helpful information
st.markdown("""

    ```
    Power up workflow's with LlamaParse to pull every detail from Invoice PDFs in seconds
    Translate any non-English invoice into clear, accurate English
    Transform messy invoice text into clean, structured fields ready for analytics or ERP upload
    ```
""") 

# File uploader
uploaded_file = st.file_uploader("Upload an invoice", type=["pdf"])

if uploaded_file is not None:
    # Calculate file hash for caching
    file_content = uploaded_file.read()
    
    with st.expander("View Invoice"):
        pdf_viewer(uploaded_file.getvalue())

    # Create two columns for results
    col1, col2 = st.columns(2, border=True)
            
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
                # Create tabs for each page
                tabs = st.tabs([f"Page {i+1}" for i in range(len(markdown_data_llama))])
                
                # Display each page in its respective tab
                for i, tab in enumerate(tabs):
                    with tab:
                        st.markdown(markdown_data_llama[i].text)
            else:
                st.warning("No markdown data could be generated from the invoice.")
                
        except Exception as e:
            st.error(str(e))

    with col2:
        st.header("Markdown Translation to English")
        if markdown_data_llama:
            try:
                # Process first page for language detection
                with st.spinner("Detecting language..."):
                    translation_result = translator.process_markdown(markdown_data_llama[0].text)
                
                # Display language and translation info above pages
                st.info(f"Source Language: {translation_result['source_language']}")

                # Create tabs for translated content
                translation_tabs = st.tabs([f"Page {i+1}" for i in range(len(markdown_data_llama))])
                
                translation_text = ""
                # Process and display each page
                for i, tab in enumerate(translation_tabs):
                    with tab:
                        with st.spinner(f"Processing page {i+1}..."):
                            start_time = time.perf_counter()
                            translation_result = translator.process_markdown(markdown_data_llama[i].text)
                            end_time = time.perf_counter()                                
                            
                            # Display translated content
                            st.markdown(translation_result['translated_text'])

                            translation_text += (translation_result['translated_text'] + '\n\n')

                            if translation_result['translated_text']:
                                st.success(f"Translation Time: {int(end_time - start_time)} seconds")
            except Exception as e:
                st.error(f"Translation error: {str(e)}")
        else:
            st.warning("No markdown content available for translation.")

    with st.container(border=True):
        st.header("LlamaParse Structured Extraction")
        try:
            # Parse the invoice
            with st.spinner("Parsing invoice..."):
                start_time = time.perf_counter()
                extracted_data_llama = llama_parser.parse_invoice(translation_text)
                end_time = time.perf_counter()
                st.info(f"Time taken by LlamaParse Extraction: {int(end_time - start_time)} seconds")
                
            if extracted_data_llama:
                st.subheader("Extracted Information")
                st.json(extracted_data_llama)
            else:
                st.warning("No data could be extracted from the invoice.")
                
        except Exception as e:
            st.error(str(e))

    # with col3:
    #     st.header("Azure Document Intelligence")
        # try:
        #     # Parse the invoice
        #     with st.spinner("Parsing invoice..."):
        #         start_time = time.perf_counter()
        #         extracted_data_azure = azure_parser.parse_invoice(file_content)
        #         end_time = time.perf_counter()
        #         st.info(f"Time taken by Azure Document Intelligence: {int(end_time - start_time)} seconds")
            
        #     if extracted_data_azure:
        #         st.subheader("Extracted Information")
        #         st.json(extracted_data_azure)
        #     else:
        #         st.warning("No data could be extracted from the invoice.")
                
        # except Exception as e:
        #     st.error(str(e))