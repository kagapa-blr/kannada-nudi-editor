from pybloom_live import ScalableBloomFilter
import file_path as fp
from corpus_clean import get_clean_dictionary

word_list_file = fp.bloomfilter_data

import importlib

bloom_filter = None  # Initialize the Bloom filter to None

def load_bloom_filter():
    global bloom_filter
    bloom_filter = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    with open(word_list_file, 'r', encoding='utf8') as text_file:
        for line in text_file:
            word = line.strip()
            bloom_filter.add(word)
    print("Bloom Filter Successfully Initialized")

def reload_bloom_filter():
    importlib.reload(fp)
    global bloom_filter
    print("Reloaded Bloom Filter Successfully!")
    bloom_filter = None  # Reset the filter to None

def bloom_lookup(keyword):
    if bloom_filter is None:
        load_bloom_filter()  # Ensure the filter is loaded if it's not already
    return keyword in bloom_filter

def start_bloom(data):
    if bloom_filter is None:
        load_bloom_filter()  # Ensure the filter is loaded if it's not already
    result = set()  # Use a set to ensure uniqueness
    for word in data:
        if len(word) > 1:
            if not bloom_lookup(word):
                result.add(word.replace('\u200c',''))
    return result

def clean_dictionary(word_list_file=word_list_file):
    get_clean_dictionary(word_list_file)
    return "Completed!"

# Load the Bloom filter initially
load_bloom_filter()

# Now you can use the bloom_filter for lookups without reinitializing it each time
# For example:
# print(bloom_lookup("ಆಡಳಿತ"))
