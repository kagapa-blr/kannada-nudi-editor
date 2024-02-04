from config import file_path as fp
from symspellpy import SymSpell, Verbosity

from utils.corpus_clean import get_clean_words_for_dictionary

symspell_model = SymSpell(max_dictionary_edit_distance=2)
symspell_model.load_dictionary(fp.symspell_word_freq_data, encoding='utf-8', term_index=0, count_index=1)


def suggestionReturner(word):
    suggestion_list = []
    suggestions = symspell_model.lookup(word, Verbosity.ALL)
    for i in suggestions:
        if len(i.term) >= len(word) and i.term!=word:
            suggestion_list.append(i.term)
    if len(suggestion_list) > 5:
        suggestion_list = suggestion_list[:5]
    suggestion_list = [get_clean_words_for_dictionary(word) for word in suggestion_list]
    return suggestion_list