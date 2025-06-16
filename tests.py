#!/usr/bin/env python3
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():
    print('Test 1: write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    
    print('\nTest 2: write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    
    print('\nTest 3: write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
    
    print('\nTest 4: run_python_file("calculator", "main.py")')
    result = run_python_file("calculator", "main.py")
    print(result)
    
    print('\nTest 5: run_python_file("calculator", "tests.py")')
    result = run_python_file("calculator", "tests.py")
    print(result)
    
    print('\nTest 6: run_python_file("calculator", "../main.py")')
    result = run_python_file("calculator", "../main.py")
    print(result)
    
    print('\nTest 7: run_python_file("calculator", "nonexistent.py")')
    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    main()
