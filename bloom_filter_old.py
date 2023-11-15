from pybloom_live import ScalableBloomFilter

class BloomFilter:
    def __init__(self, word_list_file):
        self.word_list_file = word_list_file
        self.bloom_filter = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.load_dictionary()

    def load_dictionary(self):
        try:
            with open(self.word_list_file, 'r', encoding='utf-8') as file:
                for word in file:
                    self.bloom_filter.add(word.strip())
        except FileNotFoundError:
            # Handle the case when the dictionary file doesn't exist
            pass

    def contains_word(self, word):
        return word in self.bloom_filter
