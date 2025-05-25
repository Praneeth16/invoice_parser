import json
from datetime import datetime
from pathlib import Path

def extract_original_filename(uploaded_file):
    """Extract filename without extension from uploaded file"""
    if uploaded_file is None:
        return "invoice"
    return uploaded_file.name.rsplit('.', 1)[0]

def generate_timestamp():
    """Generate timestamp string for file naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_filename_with_task(original_filename, task_type, extension=None):
    """Create filename with original name, task type, and timestamp"""
    timestamp = generate_timestamp()
    base_filename = f"{original_filename}_{task_type}_{timestamp}"
    
    if extension:
        return f"{base_filename}.{extension}"
    return base_filename

def validate_uploaded_file(uploaded_file, allowed_extensions=None):
    """Validate uploaded file type and size"""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    if allowed_extensions is None:
        allowed_extensions = ['pdf']
    
    # Check file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return False, f"File type '{file_extension}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size (optional - you can set a max size)
    max_size_mb = 50  # 50 MB limit
    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.1f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
    
    return True, "File is valid"

def create_download_content(data, content_type):
    """Create downloadable content based on type"""
    if content_type == "json":
        return json.dumps(data, indent=2)
    elif content_type == "markdown":
        return data  # Assuming data is already formatted markdown string
    elif content_type == "csv":
        # Assuming data is a pandas DataFrame or CSV string
        if hasattr(data, 'to_csv'):
            return data.to_csv(index=False)
        return str(data)
    else:
        return str(data)

def get_file_info(uploaded_file):
    """Get comprehensive file information"""
    if uploaded_file is None:
        return {}
    
    return {
        "filename": uploaded_file.name,
        "original_name": extract_original_filename(uploaded_file),
        "extension": uploaded_file.name.split('.')[-1].lower(),
        "size_bytes": len(uploaded_file.getvalue()),
        "size_mb": len(uploaded_file.getvalue()) / (1024 * 1024),
        "mime_type": uploaded_file.type if hasattr(uploaded_file, 'type') else None
    }

def sanitize_path(path_string):
    """Sanitize path string to prevent directory traversal"""
    # Remove any path traversal attempts
    clean_path = str(path_string).replace('..', '').replace('/', '').replace('\\', '')
    return clean_path

def ensure_directory_exists(directory_path):
    """Ensure directory exists, create if it doesn't"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    return Path(directory_path)

def get_cache_file_path(cache_key, cache_type, cache_dir="cache"):
    """Generate cache file path"""
    ensure_directory_exists(cache_dir)
    return Path(cache_dir) / f"{cache_key}_{cache_type}.pkl"

def cleanup_temp_files(file_patterns, max_age_hours=24):
    """Clean up temporary files older than specified hours"""
    import time
    import glob
    
    current_time = time.time()
    
    for pattern in file_patterns:
        for file_path in glob.glob(pattern):
            try:
                file_age = current_time - Path(file_path).stat().st_mtime
                if file_age > (max_age_hours * 3600):  # Convert hours to seconds
                    Path(file_path).unlink()
            except Exception:
                pass  # Ignore errors during cleanup

def get_safe_filename(filename):
    """Create a safe filename by removing/replacing invalid characters"""
    import re
    # Remove or replace invalid characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    safe_name = re.sub(r'_+', '_', safe_name)
    # Trim and ensure it's not empty
    safe_name = safe_name.strip('_')
    if not safe_name:
        safe_name = "file"
    return safe_name 