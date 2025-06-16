#!/usr/bin/env python3
from functions.run_python import run_python_file

def main():
    # Tests for executing Python files using run_python_file function
    print('\nTest 1: Running calculator/main.py')
    result = run_python_file("calculator", "main.py")
    print(f"Result: {result}")
    
    print('\nTest 2: Running calculator/tests.py')
    result = run_python_file("calculator", "tests.py")
    print(f"Result: {result}")
    
    print('\nTest 3: Attempting to run file outside project directory (calculator/../main.py)')
    result = run_python_file("calculator", "../main.py")
    print(f"Result: {result}")
    
    print('\nTest 4: Attempting to run non-existent file (calculator/nonexistent.py)')
    result = run_python_file("calculator", "nonexistent.py")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
