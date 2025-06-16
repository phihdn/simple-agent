#!/usr/bin/env python3
import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.
    
    Args:
        working_directory (str): The base directory from which relative paths are resolved
        file_path (str): The path to the file to write to (can be relative or absolute)
        content (str): The content to write to the file
    
    Returns:
        str: Success message if the file was written, or error message if an error occurred
    """
    # Convert to absolute paths for comparison
    abs_working_dir = os.path.abspath(working_directory)
    
    # Handle both relative and absolute paths
    if os.path.isabs(file_path):
        abs_file_path = file_path
    else:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file_path is outside the working_directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
        # Write content to file
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {str(e)}'
