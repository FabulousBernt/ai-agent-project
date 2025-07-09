import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Give the AI the ability to write to files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path to write to inside the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content string to write into the file."
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"