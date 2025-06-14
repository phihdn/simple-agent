import os
import pathlib


def get_files_info(working_directory, directory=None):
    """
    Get information about files in a directory.

    Args:
        working_directory (str): The base directory that restricts access.
        directory (str): The directory to list files from (relative to working_directory).
                         If None, defaults to working_directory.

    Returns:
        str: A string representation of the directory contents or an error message.
    """
    try:
        # If directory is not provided, use the working directory
        if directory is None:
            directory = working_directory

        # Convert paths to absolute and resolve any symlinks
        working_directory_path = pathlib.Path(working_directory).resolve()
        directory_path = pathlib.Path(
            os.path.join(working_directory, directory)
        ).resolve()

        # Check if the directory is outside the working directory
        if not str(directory_path).startswith(str(working_directory_path)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path exists and is a directory
        if not directory_path.exists():
            return f'Error: "{directory}" does not exist'
        if not directory_path.is_dir():
            return f'Error: "{directory}" is not a directory'

        # Get directory contents
        result = []
        for item in directory_path.iterdir():
            try:
                file_size = os.path.getsize(item)
                is_dir = item.is_dir()
                result.append(
                    f"- {item.name}: file_size={file_size} bytes, is_dir={is_dir}"
                )
            except Exception as e:
                result.append(f"- {item.name}: Error reading file info: {str(e)}")

        # Return the formatted string of directory contents
        return "\n".join(result) if result else "Directory is empty."

    except Exception as e:
        return f"Error: {str(e)}"
