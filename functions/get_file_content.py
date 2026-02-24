# functions/get_file_content.py

from config import MAX_CHARS
from google.genai import types

import os

def get_file_content(working_directory, file_path) -> str:
    target_file = None
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
        error_msg = str(e)
        if target_file:
            error_msg = error_msg.replace(target_file, file_path)
        
        return f'Error reading to "{file_path}": {error_msg}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the text content (at most {MAX_CHARS} characters) of a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file that should be read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)