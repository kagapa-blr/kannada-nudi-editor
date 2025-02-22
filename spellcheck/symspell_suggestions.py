from config import file_path as fp
from symspellpy import SymSpell, Verbosity
from logger import setup_logger
from utils.corpus_clean import get_clean_words_for_dictionary

# Initialize logger
logger = setup_logger(logger_name='symspell')
logger.info("Initializing SymSpell Model")

# Load SymSpell model
symspell_model = SymSpell(max_dictionary_edit_distance=2)
if symspell_model.load_dictionary(fp.symspell_word_freq_data, encoding='utf-8', term_index=0, count_index=1):
    logger.info(f"Dictionary loaded successfully from {fp.symspell_word_freq_data}")
else:
    logger.error(f"Failed to load dictionary from {fp.symspell_word_freq_data}")

# Log dictionary statistics
logger.info(f"Total words in dictionary: {symspell_model.word_count}")
logger.info(f"Max edit distance: {symspell_model._max_dictionary_edit_distance}")


logger.info("SymSpell Model Ready")


# Function to return spelling suggestions
def suggestionReturner(word):
    suggestion_list = []
    suggestions = symspell_model.lookup(word, Verbosity.ALL)

    for i in suggestions:
        if len(i.term) >= len(word) and i.term != word:
            suggestion_list.append(i.term)

    if len(suggestion_list) > 5:
        suggestion_list = suggestion_list[:5]

    suggestion_list = [get_clean_words_for_dictionary(word) for word in suggestion_list]
    return suggestion_list
