# call_function.py

from rich.console import Console
from rich.panel import Panel
from google.genai import types
from config import WORKING_DIR
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

console = Console()

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ],
)

function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

def call_function(function_call, verbose=False):
    args = dict(function_call.args) if function_call.args else {}
    function_name = function_call.name
    mapped_function = function_map.get(function_name)
    
    if mapped_function is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    console.print(
        Panel.fit(
            f"[bold cyan]⚠ Agent Calling function:[/bold cyan] [bold]{function_name}()[/bold]",
        border_style="cyan"
        )
    )
    
    if verbose:
        if function_name == "write_file":
            file_path_value = args.get("file_path", "")
            content_value = args.get("content", "")
            console.print(f"[cyan]  ├─ file_path:[/cyan] [bold]{file_path_value}[/bold]")
            console.print(f"[cyan]  ├─ content:[/cyan]")
            console.print(
                    Panel.fit(
                        f"[#2b6f77]{content_value}[/#2b6f77]",
                    border_style="#2b6f77"
                    )
                )
        elif function_name == "run_python_file":
            file_path_value = args.get("file_path", "")
            args_value = args.get("args", "")
            console.print(f"[cyan]  ├─ file_path:[/cyan] [bold]{file_path_value}[/bold]")
            console.print(f"[cyan]  ├─ args:[/cyan] [bold]{args_value}[/bold]")
        else:
            for param, value in args.items():
                console.print(f"[cyan]  ├─ {param}:[/cyan] [bold]{value}[/bold]")
    
    args["working_directory"] = WORKING_DIR
    function_result = mapped_function(**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )