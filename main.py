import os
import argparse


from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    generate_content(client, messages, args)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    
    if response.usage_metadata is None:
        raise RuntimeError(
            "Missing usage metadata in API response. "
            "The model may not have returned token usage information."
        )
    
    if args.verbose:
        print("User prompt:", args.user_prompt)
        print()
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Total tokens:", response.usage_metadata.total_token_count)
        print()
    
    function_calls = response.function_calls
    if function_calls:
        function_result_list = []
        for function_call in function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("No 'parts' list in function call result")
            if not function_call_result.parts[0].function_response:
                raise Exception("No 'function response' object in parts list")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No 'response' dict in function response object")
            
            function_result_list.append(function_call_result.parts[0])
            
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                
    else:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()