from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    args = dict(function_call_part.args)
    args["working_directory"] = "calculator"
    name = function_call_part.name

    # Dispatch function
    if name == "get_files_info":
        result = get_files_info(**args)
    elif name == "get_file_content":
        result = get_file_content(**args)
    elif name == "run_python_file":
        result = run_python_file(**args)
    elif name == "write_file":
        result = write_file(**args)
    else:
        # Return error Content if unknown function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    # Return successful result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )