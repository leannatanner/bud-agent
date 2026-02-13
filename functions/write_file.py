import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if valid_target_file is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        is_dir = os.path.isdir(target_file)
        if is_dir is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Creates only missing directories in a target file path
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of a file in a specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of a file inside the working directory",
            ),
        },
    ),
)