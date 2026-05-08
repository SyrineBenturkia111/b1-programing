# Lab Task 3: File Manager with os Module

import os

def file_manager():
    print("Current working directory is:", os.getcwd())

    folder_name = "lab_files"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' is created")
    else:
        print(f"Folder '{folder_name}' already exists")

    file_names = ["file1.txt", "file2.txt", "file3.txt"]
    for file_name in file_names:
        path = os.path.join(folder_name, file_name)
        with open(path, 'w') as f:
            pass
        print(f"Created: {path}")

    print(f"\nThe Files in '{folder_name}' are:")
    contents = os.listdir(folder_name)
    for item in contents:
        print(item)


    old_name = os.path.join(folder_name, "file2.txt")
    new_name = os.path.join(folder_name, "renamed_file2.txt")
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"\nWe Renamed '{old_name}' to '{new_name}'")
    else:
        print(f"\nFile '{old_name}' is not found for renaming")


    print("\n-Cleaning up-")
    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        os.remove(file_path)
        print(f"The Removed file: {file_path}")

    os.rmdir(folder_name)
    print(f"The Removed folder: '{folder_name}'")
    print("Our Cleanup is complete. All the files and the folder were deleted")

if __name__ == "__main__":
    file_manager()