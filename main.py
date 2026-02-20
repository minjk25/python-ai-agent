import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        contents=messages
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
    
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()