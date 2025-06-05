import hashlib
import pickle
import time
from pathlib import Path
import streamlit as st

# Create cache directory
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

def get_file_hash(file_content):
    """Generate consistent hash for file content"""
    return hashlib.md5(file_content).hexdigest()

def load_from_cache(cache_key, cache_type):
    """Load data from disk cache"""
    cache_file = CACHE_DIR / f"{cache_key}_{cache_type}.pkl"
    if cache_file.exists():
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            st.warning(f"Cache loading error for {cache_type}: {str(e)}")
    return None

def save_to_cache(cache_key, cache_type, data):
    """Save data to disk cache"""
    cache_file = CACHE_DIR / f"{cache_key}_{cache_type}.pkl"
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        st.warning(f"Cache saving error for {cache_type}: {str(e)}")

def get_cached_or_compute_markdown(file_content, file_hash, llama_parser):
    """Get markdown data from cache or compute it"""
    # Check session state first
    if (st.session_state.current_file_hash == file_hash and 
        st.session_state.markdown_data is not None and
        st.session_state.bounding_box_data is not None):
        return st.session_state.markdown_data, st.session_state.bounding_box_data, True
    
    # Check disk cache
    cached_markdown = load_from_cache(file_hash, "markdown")
    cached_bounding_box = load_from_cache(file_hash, "bounding_box")
    if cached_markdown is not None and cached_bounding_box is not None:
        st.session_state.markdown_data = cached_markdown
        st.session_state.bounding_box_data = cached_bounding_box
        return cached_markdown, cached_bounding_box, True
    
    # Compute new
    with st.spinner("Converting PDF to Markdown..."):
        start_time = time.perf_counter()
        markdown_data, bounding_box_data = llama_parser.pdf_to_markdown(file_content)
        end_time = time.perf_counter()
        st.info(f"Time taken by LlamaParse Parsing: {int(end_time - start_time)} seconds")
    
    # Save to cache
    save_to_cache(file_hash, "markdown", markdown_data)
    save_to_cache(file_hash, "bounding_box", bounding_box_data)
    st.session_state.markdown_data = markdown_data
    st.session_state.bounding_box_data = bounding_box_data
    
    return markdown_data, bounding_box_data, False

def get_cached_or_compute_translation(markdown_data, file_hash, translator):
    """Get translation data from cache or compute it"""
    # Check session state first
    if (st.session_state.current_file_hash == file_hash and 
        st.session_state.translation_data is not None):
        return st.session_state.translation_data, True
    
    # Check disk cache
    cached_data = load_from_cache(file_hash, "translation")
    if cached_data is not None:
        st.session_state.translation_data = cached_data
        return cached_data, True
    
    # Compute new
    translation_results = []
    translation_text = ""
    
    # Process first page for language detection
    with st.spinner("Detecting language..."):
        first_result = translator.process_markdown(markdown_data[0].text)
    
    st.info(f"Source Language: {first_result['source_language']}")
    
    # Process all pages
    for i, doc in enumerate(markdown_data):
        with st.spinner(f"Processing page {i+1}..."):
            start_time = time.perf_counter()
            translation_result = translator.process_markdown(doc.text)
            end_time = time.perf_counter()
            
            translation_results.append(translation_result)
            translation_text += (translation_result['translated_text'] + '\n\n')
            
            if translation_result['translated_text']:
                st.success(f"Translation Time: {int(end_time - start_time)} seconds")
    
    translation_data = {
        'results': translation_results,
        'combined_text': translation_text,
        'source_language': first_result['source_language']
    }
    
    # Save to cache
    save_to_cache(file_hash, "translation", translation_data)
    st.session_state.translation_data = translation_data
    
    return translation_data, False

def get_cached_or_compute_extraction(translation_text, file_hash, llama_parser):
    """Get extraction data from cache or compute it"""
    # Check session state first
    if (st.session_state.current_file_hash == file_hash and 
        st.session_state.extracted_data is not None):
        return st.session_state.extracted_data, True
    
    # Check disk cache
    cached_data = load_from_cache(file_hash, "extraction")
    if cached_data is not None:
        st.session_state.extracted_data = cached_data
        return cached_data, True
    
    # Compute new
    with st.spinner("Parsing invoice..."):
        start_time = time.perf_counter()
        extracted_data = llama_parser.parse_invoice(translation_text)
        end_time = time.perf_counter()
        st.info(f"Time taken by LlamaParse Extraction: {int(end_time - start_time)} seconds")
    
    # Save to cache
    save_to_cache(file_hash, "extraction", extracted_data)
    st.session_state.extracted_data = extracted_data
    
    return extracted_data, False

def initialize_session_cache():
    """Initialize session state cache variables"""
    if 'parsed_results' not in st.session_state:
        st.session_state.parsed_results = {}
    if 'current_file_hash' not in st.session_state:
        st.session_state.current_file_hash = None
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
    if 'markdown_data' not in st.session_state:
        st.session_state.markdown_data = None
    if 'bounding_box_data' not in st.session_state:
        st.session_state.bounding_box_data = None
    if 'translation_data' not in st.session_state:
        st.session_state.translation_data = None

def clear_session_cache():
    """Clear session cache for new file"""
    st.session_state.markdown_data = None
    st.session_state.bounding_box_data = None
    st.session_state.translation_data = None
    st.session_state.extracted_data = None 