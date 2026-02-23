# test_get_file_content.py

from functions.get_file_content import get_file_content

working_directory = "calculator"
file_paths = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

def test(working_directory, file_paths):
    for file in file_paths:
        content = get_file_content(working_directory, file)
        print(content)
        print("----------------------------------------------------------------")

if __name__ == "__main__":
    test(working_directory, file_paths)
