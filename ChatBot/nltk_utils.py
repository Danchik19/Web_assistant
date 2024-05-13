import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer #поддержка русского
import numpy as np

nltk.download('punkt') #скачать при первом запуске

stemmer = PorterStemmer()

#Токенизация
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

#Стемминг
def stem(word):
    stemmer = SnowballStemmer("russian") #строчка для добавления русского языка
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32) # нулевая матрица
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag
