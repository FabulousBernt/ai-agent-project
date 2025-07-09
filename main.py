import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file,
        ]
    )

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

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            function_call_part = response.function_calls[0]
            function_call_result = call_function(function_call_part, verbose)
            try:
                function_response = function_call_result.parts[0].function_response.response
            except Exception as e:
                raise RuntimeError("Failed to retrieve function response") from e
            if verbose:
                print(f"\nFunction call response: {function_response}")
            messages.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=function_response.get("result", json.dumps(function_response)))]
                )
            )
        else:
            if response.text:
                print("\nResponse:")
                print(response.text)
                break

    if verbose:
        print(f"\nUser prompt: {user_prompt}")
        usage = response.usage_metadata
        print("Token Usage:")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
