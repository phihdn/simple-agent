#!/usr/bin/env python3
from functions.get_file_content import get_file_content



def main():
    print('Test 1: get_file_content("calculator", "main.py")')
    content = get_file_content("calculator", "main.py")
    print(f"Content length: {len(content)} characters")
    print(content)
    
    print('\nTest 2: get_file_content("calculator", "pkg/calculator.py")')
    content = get_file_content("calculator", "pkg/calculator.py")
    print(f"Content length: {len(content)} characters")
    print(content)
    
    print('\nTest 3: get_file_content("calculator", "/bin/cat")')
    print(get_file_content("calculator", "/bin/cat"))


if __name__ == "__main__":
    main()
