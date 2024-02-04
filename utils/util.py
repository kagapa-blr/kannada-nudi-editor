import re


def has_letters_or_digits(word):
    # Define a regular expression pattern
    pattern = re.compile(r'[a-zA-Z\d]')
    # Use re.search to check if the pattern is present in the word
    return bool(re.search(pattern, word))
