from collections import Counter
from math import *


extra = ["'", '"', ',', ':', ')', '(', '=', '-',
         '_', '+', '*', '&', '^', '%', '$', '#', '@', '!', '<', '>',
         '}', '{', '[', ']', '`', '`', "/", ";"]


def docfreq(text):
    text_list = text.split()
    counter = Counter()
    for word in text_list:
        counter[word] += 1
    return counter
        
def inv_doc_freq(text, word, length):
    #idf = {}
    #for word in docfreq(text).keys:
        #idf[word] = log10(length/docfreq(text)[word])
    idf = log10(length/docfreq(text)[word])
    return idf

def word_weight(text):
    weights = {}
    for letter in text:
        if letter in extra:
            text = text.replace(letter, '')
        if letter == '.':
            text = text.replace(letter, ' ')
    splits = text.split()
    length = len(splits)
    for word in splits:
        weights[word] = log(1 + docfreq(text)[word])\
                        * log10(inv_doc_freq(text, word, length))
    return weights

#def score(x):
    

#def lookuptext(text):
