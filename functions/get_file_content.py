# functions/get_file_content.py

import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path) -> str:
    try:
        abspath_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_working_dir, file_path))
        common_path = os.path.commonpath([abspath_working_dir, target_file])
        
        # guardrails
        if common_path != abspath_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(target_file, "r") as file:
            str_content = file.read(MAX_CHARS)
            if file.read(1):
                str_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return str_content
    
    except Exception as e:
        error_msg = str(e).replace(target_file, file_path)
        return f'Error reading to "{file_path}": {error_msg}'
    
