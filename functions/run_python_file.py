# functions/run_python_file.py

from google.genai import types

import os
import subprocess

def run_python_file(working_directory, file_path, args=None) -> str:
    target_file = None
    try:
        abspath_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_working_dir, file_path))
        common_path = os.path.commonpath([abspath_working_dir, target_file])
        
        # guardrails
        if common_path != abspath_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.lower().endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        completed_process = subprocess.run(
            command,
            cwd=abspath_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output_list = []
        return_code = completed_process.returncode
        std_out = completed_process.stdout
        std_err = completed_process.stderr
        
        if return_code != 0:
            output_list.append(f"Process exited with code {return_code}")
        
        if not std_out and not std_err:
            output_list.append("No output produced")
        else:
            if std_out:
                output_list.append(f"STDOUT: {std_out}")
            if std_err:
                output_list.append(f"STDERR: {std_err}")
        
        return "\n".join(output_list)
    
    except Exception as e:
        error_msg = str(e)
        if target_file:
            error_msg = error_msg.replace(target_file, file_path)
        
        return f'Error executing Python file "{file_path}": {error_msg}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a specified Python file relative to the working directory with optional arguments and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the python file that should be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of command-line arguments to pass to the Python script.",
            )
        },
        required=["file_path"]
    ),
)