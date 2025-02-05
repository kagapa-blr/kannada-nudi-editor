import re


def has_letters_or_digits(word):
    # Define a regular expression pattern
    pattern = re.compile(r'[a-zA-Z\d]')
    # Use re.search to check if the pattern is present in the word
    return bool(re.search(pattern, word))


import os


def remove_spaces_in_filenames(folder_path):
    """
    Removes spaces from all filenames inside the specified folder.
    :param folder_path: Path to the folder containing the files.
    """
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return
    for filename in os.listdir(folder_path):
        new_filename = filename.replace(" ", "")  # Remove spaces
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)

        if old_path != new_path:  # Ensure names are different before renaming
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

    print("Renaming completed.")
