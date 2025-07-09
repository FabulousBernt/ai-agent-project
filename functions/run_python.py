import os
import subprocess
from google.genai import types


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",  # <-- Correct function name here
    description="Runs a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to run within the working directory."
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python", abs_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=abs_working_dir,
                timeout=30,
                text=True
            )
            output_parts = []
            if result.stdout:
                output_parts.append("STDOUT:\n" + result.stdout)
            if result.stderr:
                output_parts.append("STDERR:\n" + result.stderr)
            if result.returncode != 0:
                output_parts.append(f"Process exited with code {result.returncode}")
            if not result.stdout and not result.stderr:
                output_parts.append("No output produced.")
            return "\n".join(output_parts)
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out after 30 seconds."
        except Exception as e:
            return f"Error: {str(e)}"

    except Exception as e:
        return f"Error: executing Python file: {e}"