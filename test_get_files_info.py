# test_get_files_info.py

from functions.get_files_info import get_files_info

working_directory = "calculator"
directories = [".","pkg", "/bin", "../"]

def test(working_directory, directories):
    for directory in directories:
        raw_result = get_files_info(working_directory, directory)
        indented_result = "\n".join("  " + line for line in raw_result.splitlines())
        if directory == ".":
            directory_name = "current"
        else:
            directory_name = f"'{directory}'"
        print(f"Result for {directory_name} directory:\n{indented_result}")
        print("----------------------------------------------------------------")

if __name__ == "__main__":
    test(working_directory, directories)