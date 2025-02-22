from pybloom_live import ScalableBloomFilter
from config import file_path as fp
from logger import setup_logger
from utils.corpus_clean import get_clean_dictionary

import importlib

# Initialize logger
logger = setup_logger(logger_name='bloomfilter')

# Bloom Filter Variables
word_list_file = fp.bloomfilter_data
bloom_filter = None  # Initially set to None

def load_bloom_filter():
    """Loads words into the Bloom Filter and logs statistics."""
    global bloom_filter
    bloom_filter = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    word_count = 0  # Track the number of words added

    with open(word_list_file, 'r', encoding='utf8') as text_file:
        for line in text_file:
            word = line.strip()
            bloom_filter.add(word)
            word_count += 1

    logger.info(f"Bloom Filter Successfully Initialized with {word_count} words")
    logger.info(f"Bloom Filter Capacity: {bloom_filter.capacity}, Error Rate: {bloom_filter.error_rate}")

def reload_bloom_filter():
    """Reloads the Bloom Filter by resetting and reloading it."""
    importlib.reload(fp)
    global bloom_filter
    bloom_filter = None  # Reset the filter to None
    logger.info("Reloaded Bloom Filter Successfully!")

def bloom_lookup(keyword):
    """Checks if a keyword exists in the Bloom Filter."""
    if bloom_filter is None:
        load_bloom_filter()  # Ensure filter is loaded
    exists = keyword in bloom_filter
    #logger.info(f"Lookup for '{keyword}': {'Found' if exists else 'Not Found'}")
    return exists

def start_bloom(data):
    """Filters words that are not present in the Bloom Filter."""
    if bloom_filter is None:
        load_bloom_filter()  # Ensure filter is loaded

    result = set()  # Use a set to store unique words
    for word in data:
        if len(word) > 1:
            if not bloom_lookup(word):
                clean_word = word.replace('\u200c', '')  # Remove zero-width characters
                result.add(clean_word)

    logger.info(f"Filtered {len(data)} words, {len(result)} were not found in Bloom Filter")
    return result

def clean_dictionary(word_list_file=word_list_file):
    """Cleans the dictionary file using an external function."""
    get_clean_dictionary(word_list_file)
    logger.info("Completed Dictionary Cleanup!")
    return "Completed!"

# Load the Bloom filter initially
load_bloom_filter()

# Example lookup (for testing)
# logger.info(bloom_lookup("ಆಡಳಿತ"))
