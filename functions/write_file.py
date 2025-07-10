import os
from google.genai import types

def write_file(working_directory, file_path, content):
    work_path = os.path.abspath(working_directory)
    joined_path = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not joined_path.startswith(work_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        directory = os.path.dirname(joined_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(joined_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes the content on the given file",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file_path to get the file from. If not provided or a wrong path is given it returns an error message",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to put on the file",
            ),
        },
    ),
)