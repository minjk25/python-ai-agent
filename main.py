import os
import sys
import argparse

from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERATIONS

console = Console()

def main():
    
    parser = argparse.ArgumentParser(description="AI code Assistant.")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini AI.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please set it in your .env file.")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    #if args.verbose:
    print()
    console.print(
        Panel.fit(
            f'[bold][#e7af47]󰁕 User prompt: [/#e7af47]"{args.user_prompt}"[/bold]',
            border_style="#e7af47"
        )
    )
    print()
    
    for _ in range(MAX_ITERATIONS):
        try:
            response_answer = generate_content(client, messages, args)
            
            if response_answer:
                console.print("[bold #e7af47]\n󰌵 Agent Response 󰌵[/bold #e7af47]")
                console.print(
                    Panel.fit(
                        f"[bold cyan]{response_answer}[/bold cyan]",
                    border_style="#e7af47"
                    )
                )
                return
        except Exception as e:
            console.print(f"[bold red]Error in generate_content: {e}[/bold red]")
            return
    
    console.print("[bold red]Error: Maximum iterations reached without a final response.[/bold red]")
    sys.exit(1)

def generate_content(client, messages, args):
    with console.status("[bold green]Thinking...", spinner="dots"):
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
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
                console.print(f"\n[#333539] ◇ Prompt tokens: {response.usage_metadata.prompt_token_count}[/#333539]")
                console.print(f"[#2d3034] ◇ Response tokens: {response.usage_metadata.candidates_token_count}[/#2d3034]")
                console.print(f"[#2d3034] ◇ Total tokens: {response.usage_metadata.total_token_count}[/#2d3034]\n")
            if not function_call_result.parts:
                raise Exception("No 'parts' list in function call result")
            if not function_call_result.parts[0].function_response:
                raise Exception("No 'function response' object in parts list")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No 'response' dict in function response object")
            
            function_result_list.append(function_call_result.parts[0])
            
            if args.verbose:
                console.print("[#2b6f77]● Result:[/#2b6f77]")
                console.print(
                    Panel.fit(
                        f"[#2b6f77]{function_call_result.parts[0].function_response.response["result"]}[/#2b6f77]",
                    border_style="#2b6f77"
                    )
                )
                print("\n-------------------------------------------------------------------------------\n")
        
        messages.append(types.Content(role="user", parts=function_result_list))
    
    else:
        if args.verbose:
                console.print(
                    Panel.fit(
                        f"[bold cyan]⚠ Agnet preparing response ... [/bold cyan]",
                    border_style="cyan"
                    )
                )
                console.print(f"\n[#637182] ◇ Prompt tokens: {response.usage_metadata.prompt_token_count}[/#637182]")
                console.print(f"[#637182] ◇ Response tokens: {response.usage_metadata.candidates_token_count}[/#637182]")
                console.print(f"[#637182] ◇ Total tokens: {response.usage_metadata.total_token_count}[/#637182]")
        return response.text

color = "#637182"

if __name__ == "__main__":
    main()