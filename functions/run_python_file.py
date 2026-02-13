import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        is_file = os.path.isfile(target_file)
        if is_file is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        command_result = subprocess.run(command,
                                        cwd=abs_working_dir,
                                        capture_output=True,
                                        text=True,
                                        timeout=30)
        
        output_parts = []

        if command_result.returncode != 0:
            output_parts.append(f"Process exited with code {command_result.returncode}")
        if not command_result.stdout and not command_result.stderr:
            output_parts.append(f"No output produced")
        else:
            if command_result.stdout:
                output_parts.append(f"STDOUT:{command_result.stdout}")
            if command_result.stderr:
                output_parts.append(f"STDERR:{command_result.stderr}")
        "\n".join(output_parts)
        return output_parts
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs arbitrary Python code inside a specified directory",
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