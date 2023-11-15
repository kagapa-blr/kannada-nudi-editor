import os
from collections import Counter

import docx
import file_path as fp


def cleanWords(word_):
    p = """pmg k:-B}u!8&9‘೭_೮r೯MQ೪6lJ\IqLfKy'VWD%~OwH2s೧…x*c`C“–X5@E#n|)ʼPe+Y[j47v’/UhFRS$೨T”;GiA,=೫>.೦3೩"<Na(^bt•Z1?]0z೬do{"""
    for i in p:
        word_ = word_.replace(i.strip(), "")
    return word_

# clean collection files
def get_clean_dictionary(file_name):
    if file_name.endswith(".txt"):
        with open(file_name, 'r', encoding='utf-8') as file:
            words = set([cleanWords(word.strip()) for word in file])
            words = [word for word in words if word]
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("\n".join(words))
        print(f'Cleaned words written back to {file_name}')
    else:
        return "file is not txt file format"
    return f'Cleaned words written back to {file_name}'


# clearn freq files
def returnCleanFrequency(file_name):
    if file_name.endswith('.txt'):
        word_frequency_dict = {}
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 2:
                    word, frequency = parts
                    cleaned_word = cleanWords(word)
                    if type(frequency)== int:
                        frequency = int(frequency)
                    if cleaned_word:
                        word_frequency_dict[cleaned_word] = frequency
        with open(file_name, 'w', encoding='utf-8') as file:
            for word, frequency in word_frequency_dict.items():
                file.write(f"{word} {frequency}\n")
        print(f'Cleaned words written back to {file_name}')
    else:
        return "file is not txt file format"
    return f'Cleaned words written back to {file_name}'


def cleanmultipleFiles(directory_path):
    file_list = os.listdir(directory_path)
    # Iterate through the files and read them one by one
    for file_name in file_list:
        # Check if the item in the directory is a file (not a subdirectory)
        if os.path.isfile(os.path.join(directory_path, file_name)):
            file_name = os.path.join(directory_path, file_name)
            returnCleanFrequency(file_name)
            get_clean_dictionary(file_name)
    print("Successfully cleaned all files!")
    return "completed!"
#returnCleanFrequency("../datasets/freq_test.txt")




def get_clean_words_for_dictionary(word):
    p = """೧^l=F–೬B#yJwfz•+2umE<'!CxULvr]8VNdhH‘_>)- :sYQ7.g9n%W,G`1…"&?6೯I”೮೨Tb“@೭೫ʼKX4೪[iDScM;*t\’{5k/pa(PAeZ~O3R|j}q೩$"""#string.punctuation + 'ʼ“”•0123456789೧೨೩೪೫೬೭೮೯೦@#$%^&*()`_ʼ,.;ʼ' + ' ' + '"' + """'()*+,-./‘’’’“”;<=–>?@[\]^_`{|}~""" + '…' + '' + '“'+'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in p:
        word = word.replace(i.strip(), "")
    return word


# Function to extract Kannada words from a text file

def extract_kannada_words_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.docx':
        content = read_docx(file_path)
        content = [get_clean_words_for_dictionary(word) for word in content.split() if len(word) > 1]
        return  content
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            content = [get_clean_words_for_dictionary(word) for word in content.split() if len(word) > 1]
            return content

# Function to calculate word frequency
def calculate_word_frequency(words):
    word_counts = Counter(words)
    return word_counts
def read_docx(file):
    doc = docx.Document(file)
    doc_text = ""
    for paragraph in doc.paragraphs:
        doc_text += paragraph.text + "\n"
    return doc_text

