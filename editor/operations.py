import docx
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMenu, QToolBar, QMessageBox, \
    QInputDialog, QLineEdit, QTextEdit

from config import file_path as fp
from keyboard.create_kannada_keyboard import KannadaTextEdit
from spellcheck.bloom_filter import bloom_lookup, start_bloom, reload_bloom_filter
from spellcheck.symspell_suggestions import suggestionReturner
from utils.corpus_clean import get_clean_words_for_dictionary
from utils.util import has_letters_or_digits

