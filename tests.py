#!/usr/bin/env python3
from functions.write_file import write_file

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

if __name__ == "__main__":
    main()
