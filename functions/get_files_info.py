# functions/get_files_info.py

import os

def get_files_info(working_directory, directory=".") -> str:
    target_dir = None
    try:
        abspath_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath_working_dir, directory))
        common_path = os.path.commonpath([abspath_working_dir, target_dir])
        
        # guardrails
        if common_path != abspath_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        str_items = "\n".join(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                for item in os.listdir(target_dir)
                if (item_path := os.path.join(target_dir, item))
            )
        return str_items
    
    except Exception as e:
        error_msg = str(e)
        if target_dir:
            error_msg = error_msg.replace(target_dir, directory)
        
        return f'Error listing files: {error_msg}'
    
