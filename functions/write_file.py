# functions/write_file.py

import os

def write_file(working_directory, file_path, content) -> str:
    target_file = None
    try:
        abspath_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_working_dir, file_path))
        common_path = os.path.commonpath([abspath_working_dir, target_file])
        
        # guardrails
        if common_path != abspath_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)   
        
        with open(target_file, "w") as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        error_msg = str(e)
        if target_file:
            error_msg = error_msg.replace(target_file, file_path)
        
        return f'Error writing to "{file_path}": {error_msg}'