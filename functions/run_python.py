import os
import subprocess

def run_python_file(working_directory, file_path):
    # Convert to absolute path for checking
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if file is outside working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file exists
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if file is a Python file
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Execute the Python file
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )
        
        # Format the output
        output = []
        
        if result.stdout:
            output.append(f"STDOUT: {result.stdout.strip()}")
        
        if result.stderr:
            output.append(f"STDERR: {result.stderr.strip()}")
        
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if not output:
            return "No output produced."
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error executing Python file: {e}"
