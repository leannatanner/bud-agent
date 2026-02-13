import os
from google.genai import types
from configs import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if valid_target_file is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        is_file = os.path.isfile(target_file)
        if is_file is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string
            return file_content_string
    
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file contents of a file in a specified directory",
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