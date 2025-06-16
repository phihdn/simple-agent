import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    # Create function schemas
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the content of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )
    
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file and returns its output, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )
    
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a file, creating directories if needed, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
            required=["file_path", "content"],
        ),
    )

    # Define available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    # Update system prompt to instruct LLM on how to use functions
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    model_name = "gemini-2.0-flash-001"
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # Check if the response contains function calls
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                # LLM made a function call
                function_call_part = part.function_call
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                
                # Execute the appropriate function based on the function call
                if function_call_part.name == "get_files_info":
                    directory = function_call_part.args.get("directory", "")
                    result = get_files_info(os.getcwd(), directory)
                    print(result)
                elif function_call_part.name == "get_file_content":
                    file_path = function_call_part.args.get("file_path", "")
                    result = get_file_content(os.getcwd(), file_path)
                    print(result)
                elif function_call_part.name == "run_python_file":
                    file_path = function_call_part.args.get("file_path", "")
                    result = run_python_file(os.getcwd(), file_path)
                    print(result)
                elif function_call_part.name == "write_file":
                    file_path = function_call_part.args.get("file_path", "")
                    content = function_call_part.args.get("content", "")
                    result = write_file(os.getcwd(), file_path, content)
                    print(result)
            else:
                # Regular text response
                print("Response:")
                print(part.text)
    else:
        # Fallback to just printing the text
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
