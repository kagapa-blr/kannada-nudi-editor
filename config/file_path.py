opt = "dev"

if opt == "dev":
    bloomfilter_data = "datasets/dictionary_words_test.txt"
    symspell_word_freq_data = "datasets/word_freq_test.txt"
    userWordFile = "datasets/userAddWords/myCollections_test.json"
elif opt == "pro":
    bloomfilter_data = "datasets/dictionary_words_prod.txt"
    symspell_word_freq_data = "datasets/word_freq_prod.txt"
    userWordFile = "datasets/userAddWords/myCollections.json"

