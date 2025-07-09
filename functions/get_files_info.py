import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    work_path = os.path.abspath(working_directory)
    joined_path = os.path.abspath(os.path.join(working_directory,directory))
    
    if not joined_path.startswith(work_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(joined_path):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(joined_path)
    files_with_data = []
    try:
        for file in files:
            size = os.path.getsize(joined_path+"/"+file)
            is_file = os.path.isfile(joined_path+"/"+file)
            files_with_data.append(f"- {file}: file_size={size} bytes, is_dir={not is_file}\n")
        return "".join(files_with_data)
    
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in the specified directory along with their sizes, constrained to the working directory",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself",
            ),
        },
    ),
)