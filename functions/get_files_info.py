import os


def get_files_info(working_directory, directory=None):
    if directory is None:
        target_path = working_directory
        relative_directory = "."
    else:
        target_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        if not target_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        relative_directory = directory

    if not os.path.isdir(target_path):
        return f'Error: "{relative_directory}" is not a directory'

    try:
        files = os.listdir(target_path)
        lines = []
        for filename in files:
            full_path = os.path.join(target_path, filename)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            lines.append(f"- {filename}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error accessing {target_path}: {str(e)}"
