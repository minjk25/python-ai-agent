# test_run_python_file.py

from functions.run_python_file import run_python_file

working_directory = "calculator"
file_paths_with_args = [
    ("main.py", None),
    ("main.py", ["3 + 5"]),
    ("tests.py", None),
    ("../main.py", None),
    ("nonexistent.py", None),
    ("lorem.txt", None)
]

def test(working_directory, file_paths_with_args):
    for file_path, argument in file_paths_with_args:
        result = run_python_file(working_directory, file_path, argument)
        print(result)
        print("----------------------------------------------------------------")

if __name__ == "__main__":
    test(working_directory, file_paths_with_args)