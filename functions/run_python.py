import os
import subprocess

def run_python_file(working_directory, file_path):
    work_path = os.path.abspath(working_directory)
    joined_path = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not joined_path.startswith(work_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_path):
        return f'Error: File "{file_path}" not found.'
    if file_path[-3::] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        res = subprocess.run(["python3", joined_path], timeout=30, text=True, capture_output=True)
        print(f'STDOUT: {res.stdout}')
        print(f'STDERR: {res.stderr}')
        
        if res.returncode != 0:
            print(f'Process exited with code {res.CalledProcessError}')
        if not res.stdout and not res.stderr:
            return "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


# # # TEST
# if __name__ == "__main__":
#     result = run_python_file("calculator", "tests.py")

