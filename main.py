import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompts = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    user_prompt = " ".join(prompts)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )
    print("\nResponse:")
    print(response.text)

    if verbose:
        print(f"\nUser prompt: {user_prompt}")
        usage = response.usage_metadata
        print("Token Usage:")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
