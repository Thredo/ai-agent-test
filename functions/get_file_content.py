import os
from google.genai import types

def get_file_content(working_directory, file_path):
    work_path = os.path.abspath(working_directory)
    joined_path = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not joined_path.startswith(work_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_path):
        f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000
    try:
        with open(joined_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'\n [...File "{joined_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Lists contents of file in the specified directory. In case the file has more than 10000 characters it truncates it",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file_path to get the file from. If not provided or a wrong path is given it returns an error message",
            ),
        },
    ),
)