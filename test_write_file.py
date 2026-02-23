# test_write_file.py

from functions.write_file import write_file

working_directory = "calculator"
file_paths_with_contents = {
    "lorem.txt" : "wait, this isn't lorem ipsum",
    "pkg/morelorem.txt" : "lorem ipsum dolor sit amet",
    "/tmp/temp.txt" : "this should not be allowed"
}


def test(working_directory, file_paths_with_contents):
    for file_path, content in file_paths_with_contents.items():
        result = write_file(working_directory, file_path, content)
        print(result)
        print("----------------------------------------------------------------")

if __name__ == "__main__":
    test(working_directory, file_paths_with_contents)