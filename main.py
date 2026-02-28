import os
import sys
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.markdown import Markdown
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERATIONS, gray1, blue1, orange1

console = Console()

def main():
    
    parser = argparse.ArgumentParser(description="AI code Assistant.")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini AI.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please set it in your '.env' file.")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    print()
    console.print(
        Panel.fit(
            f'[bold][{orange1}]󰁕 User prompt: [/{orange1}]"{args.user_prompt}"[/bold]',
            border_style=orange1
        )
    )
    print()
    
    for _ in range(MAX_ITERATIONS):
        try:
            response_answer = generate_content(client, messages, args)
            
            if response_answer:
                console.print(f"[bold {orange1}]\n󰌵 Agent Response 󰌵[/bold {orange1}]")
                console.print(
                    Panel.fit(
                        Markdown(
                            response_answer,
                            # style="cyan"
                        ),
                        border_style=orange1
                    )
                )
                return
        except Exception as e:
            console.print(f"[bold red]Error in generate_content: {e}[/bold red]")
            return
    
    console.print("[bold red]Error: Maximum iterations reached without a final response.[/bold red]")
    sys.exit(1)

def generate_content(client, messages, args):
    with console.status("[bold green]Thinking...\n", spinner="dots"):
        response = client.models.generate_content(
            model='gemini-2.5-pro', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
    
    candidates = response.candidates
    if candidates:
        for candidate in candidates:
            if candidate.content:
                messages.append(candidate.content)
    
    if response.usage_metadata is None:
        raise RuntimeError(
            "Missing usage metadata in API response. "
            "The model may not have returned token usage information."
        )
    
    function_calls = response.function_calls
    if function_calls:
        function_result_list = []
        for function_call in function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if args.verbose:
                show_tokens(response, gray1)
            if not function_call_result.parts:
                raise Exception("No 'parts' list in function call result")
            if not function_call_result.parts[0].function_response:
                raise Exception("No 'function response' object in parts list")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No 'response' dict in function response object")
            
            function_result_list.append(function_call_result.parts[0])
            
            if args.verbose:
                console.print(f"[{blue1}]\n● Result:[/{blue1}]")
                console.print(
                    Panel.fit(
                        f"[{blue1}]{function_call_result.parts[0].function_response.response["result"]}[/{blue1}]",
                    border_style=blue1
                    )
                )
                print("\n--------------------------------------------------------------------------------\n")
        
        messages.append(types.Content(role="user", parts=function_result_list))
    
    else:
        console.print(
            Columns(
                [
                    "\n[bold cyan]╰→[/bold cyan]\n",
                    Panel.fit(
                        f"[bold cyan]⚠ Agent preparing response... [/bold cyan]",
                        border_style="cyan"
                    )
                ],
                expand=False,
            )
        )
        
        if args.verbose:
            show_tokens(response, gray1)
        
        return response.text

def show_tokens(response, color):
    console.print(f"\n[{color}] ◇ Prompt tokens: {response.usage_metadata.prompt_token_count}[/{color}]")
    console.print(f"[{color}] ◇ Response tokens: {response.usage_metadata.candidates_token_count}[/{color}]")
    console.print(f"[{color}] ◇ Total tokens: {response.usage_metadata.total_token_count}[/{color}]")

if __name__ == "__main__":
    main()