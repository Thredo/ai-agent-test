import os

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


# # TEST
# if __name__ == "__main__":
#     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#     print(result)

