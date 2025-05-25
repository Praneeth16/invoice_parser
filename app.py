import io
import time
import json
import pandas as pd
from datetime import datetime

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from src import AzureInvoiceParser, LlamaInvoiceParser
from src.translation import MarkdownTranslator
from src.cache_manager import (
    initialize_session_cache, 
    clear_session_cache,
    get_file_hash,
    get_cached_or_compute_markdown,
    get_cached_or_compute_translation,
    get_cached_or_compute_extraction
)
from src.data_processors import (
    convert_to_csv_data,
    create_summary_tables,
    format_translation_markdown,
    format_markdown_content,
    convert_dataframe_to_csv_string
)
from src.file_utils import (
    extract_original_filename,
    create_filename_with_task,
    validate_uploaded_file,
    get_file_info
)

# Set page config
st.set_page_config(
    page_title="🚀 AI-Powered Invoice Parser & Translator",
    page_icon="📄",
    layout="wide"
)

# Initialize session state for caching
initialize_session_cache()

# Initialize parsers and translator
azure_parser = AzureInvoiceParser()
llama_parser = LlamaInvoiceParser()
translator = MarkdownTranslator()

st.title("🚀 AI-Powered Invoice Parser & Translator")

# Add enhanced information
st.markdown("### 🎯 Transform Your Invoice Processing Workflow")

# Create columns for feature highlights
col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.markdown("""
    **⚡ Lightning-Fast Parsing**
    
    Extract every detail from invoice PDFs in seconds using advanced LlamaParse technology
    """)

with col2:
    st.markdown("""
    **🌍 Universal Translation**
    
    Automatically translate non-English invoices into clear, accurate English
    """)

with col3:
    st.markdown("""
    **📊 Structured Output**
    
    Transform messy invoice text into clean, structured data ready for analytics or ERP systems
    """)

# File uploader
with st.container(border=True):
    st.markdown("#### 📄 Upload an Invoice")
    uploaded_file = st.file_uploader("Invoice PDF", type=["pdf"])

if uploaded_file is not None:
    # Validate uploaded file
    is_valid, validation_message = validate_uploaded_file(uploaded_file)
    if not is_valid:
        st.error(f"File validation failed: {validation_message}")
        st.stop()
    
    # Calculate file hash for caching
    file_content = uploaded_file.read()
    file_hash = get_file_hash(file_content)
    
    # Update session state file hash
    if st.session_state.current_file_hash != file_hash:
        st.session_state.current_file_hash = file_hash
        clear_session_cache()
    
    # Get file info
    file_info = get_file_info(uploaded_file)
    st.info(f"📊 File: {file_info['filename']} ({file_info['size_mb']:.1f} MB)")
    
    with st.expander("View Invoice"):
        pdf_viewer(uploaded_file.getvalue())

    # Create two columns for results
    col1, col2 = st.columns(2, border=True)
            
    with col1:
        st.header("LlamaParse Markdown Parsing")
        try:
            # Get markdown data (cached or computed)
            markdown_data_llama, was_cached = get_cached_or_compute_markdown(
                file_content, file_hash, llama_parser
            )
            
            if was_cached:
                st.info("✅ Using cached markdown parsing results")
            
            if markdown_data_llama:
                # Create tabs for each page
                tabs = st.tabs([f"Page {i+1}" for i in range(len(markdown_data_llama))])
                
                # Display each page in its respective tab
                for i, tab in enumerate(tabs):
                    with tab:
                        st.markdown(markdown_data_llama[i].text)
                
                # Download section for markdown
                st.subheader("📥 Download Markdown")
                
                # Format markdown content
                combined_markdown = format_markdown_content(markdown_data_llama)
                original_name = extract_original_filename(uploaded_file)
                filename = create_filename_with_task(original_name, "parsing", "md")
                
                st.download_button(
                    label="📄 Download Markdown",
                    data=combined_markdown,
                    file_name=filename,
                    mime="text/markdown",
                    help="Download parsed markdown content"
                )
            else:
                st.warning("No markdown data could be generated from the invoice.")
                
        except Exception as e:
            st.error(str(e))

    with col2:
        st.header("Markdown Translation to English")
        if markdown_data_llama:
            try:
                # Get translation data (cached or computed)
                translation_data, was_cached = get_cached_or_compute_translation(
                    markdown_data_llama, file_hash, translator
                )
                
                if was_cached:
                    st.info("✅ Using cached translation results")
                    st.info(f"Source Language: {translation_data['source_language']}")

                # Create tabs for translated content
                translation_tabs = st.tabs([f"Page {i+1}" for i in range(len(markdown_data_llama))])
                
                # Display each page
                for i, tab in enumerate(translation_tabs):
                    with tab:
                        result = translation_data['results'][i]
                        st.markdown(result['translated_text'])

                # Download section for translation
                st.subheader("📥 Download Translation")
                
                # Format translation content
                translation_markdown = format_translation_markdown(translation_data)
                original_name = extract_original_filename(uploaded_file)
                filename = create_filename_with_task(original_name, "translation", "md")
                
                st.download_button(
                    label="🌍 Download Translation",
                    data=translation_markdown,
                    file_name=filename,
                    mime="text/markdown",
                    help="Download translated content as markdown"
                )

            except Exception as e:
                st.error(f"Translation error: {str(e)}")
        else:
            st.warning("No markdown content available for translation.")

    with st.container(border=True):
        st.header("LlamaParse Structured Extraction")
        try:
            if 'translation_data' in locals() and translation_data:
                # Get extraction data (cached or computed)
                extracted_data_llama, was_cached = get_cached_or_compute_extraction(
                    translation_data['combined_text'], file_hash, llama_parser
                )
                
                if was_cached:
                    st.info("✅ Using cached extraction results")
                    
                if extracted_data_llama:
                    # Create tabs for JSON and Table views
                    json_tab, table_tab = st.tabs(["📋 JSON View", "📊 Table View"])
                    
                    with json_tab:
                        st.subheader("Extracted Information (JSON)")
                        st.json(extracted_data_llama)
                    
                    with table_tab:
                        st.subheader("Extracted Information (Tables)")
                        
                        # Create summary tables
                        tables = create_summary_tables(extracted_data_llama)
                        
                        # Display each table
                        for table_name, df in tables.items():
                            st.write(f"**{table_name}**")
                            st.dataframe(df, use_container_width=True)
                            st.write("")  # Add some spacing
                    
                    # Download section
                    st.subheader("📥 Download Options")
                    col_json, col_csv = st.columns(2)
                    
                    with col_json:
                        # JSON download
                        json_str = json.dumps(extracted_data_llama, indent=2)
                        original_name = extract_original_filename(uploaded_file)
                        filename = create_filename_with_task(original_name, "json", "json")
                        
                        st.download_button(
                            label="📄 Download JSON",
                            data=json_str,
                            file_name=filename,
                            mime="application/json",
                            help="Download extracted data as JSON file"
                        )
                    
                    with col_csv:
                        # CSV download
                        csv_df = convert_to_csv_data(extracted_data_llama)
                        csv_string = convert_dataframe_to_csv_string(csv_df)
                        original_name = extract_original_filename(uploaded_file)
                        filename = create_filename_with_task(original_name, "table", "csv")
                        
                        st.download_button(
                            label="📊 Download CSV",
                            data=csv_string,
                            file_name=filename,
                            mime="text/csv",
                            help="Download extracted data as CSV file"
                        )
                    
                else:
                    st.warning("No data could be extracted from the invoice.")
            else:
                st.warning("Translation data not available for extraction.")
                
        except Exception as e:
            st.error(str(e))