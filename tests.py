from functions.get_file_content import get_file_content

print("Test 1: get_file_content('calculator', 'main.py')")
print(get_file_content("calculator", "main.py"))
print()

print("Test 2: get_file_content('calculator', 'pkg/calculator.py')")
print(get_file_content("calculator", "pkg/calculator.py"))
print()

print("Test 3: get_file_content('calculator', '/bin/cat')")
print(get_file_content("calculator", "/bin/cat"))
print()

print("Test 4: get_file_content('calculator', 'lorem.txt')")
print(get_file_content("calculator", "lorem.txt"))
print()