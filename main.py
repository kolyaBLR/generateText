#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
from random import uniform
from collections import defaultdict

def gen_lines(corpus):
    data = open(corpus)
    for line in data:
        yield line.decode('utf-8').lower()

def gen_tokens(lines):
    for line in lines:
        for token in get_re_alphabet(language).findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.iteritems():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model

def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token



def get_directory(language):
    return "language" + "/" + language + ".txt";

def is_last_error(error_count):
    temp = error_count - int(error_count)
    return random.random() <= temp

def generate_array_random_unique(count, len):
    array = []
    for i in range(count):
        item = random.randint(0, len - 2)
        array.append(item)
    return array

def get_random_unique_symbol(symbol, language):
    alphabet = {
        "ru" : u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
        "en" : u"abcdefghijklmnopqrstuvwxyz",
        "be" : u"абвгдеёжзійклмнопрстуўфхцчшыьэюя"};
    new_symbol = symbol
    while symbol == new_symbol:
        new_symbol = alphabet[language][random.randint(0, len(alphabet[language]) - 2)]
    return new_symbol

def get_text_error(text, array, language):
    new_text = ""
    for i in range(len(text)):
        symbol = text[i]
        for item in array:
            if (i == item):
                symbol = get_random_unique_symbol(symbol, language)
        new_text += symbol
    return new_text

def generate_error(text, count, language):
    if (is_last_error(count)):
        count = int(count) + 1
    array = generate_array_random_unique(int(count), len(text))
    return get_text_error(text, array, language)

def generate_text(paragraph_count, sentence_count, model, error_count, language):
    paragraph = ""
    for i in range(paragraph_count):
        for j in range(sentence_count):
            text = generate_error(generate_sentence(model), error_count, language)
            paragraph += text  + " "
        paragraph += "\n\n"
    return paragraph

def get_re_alphabet(language):
    language_array = {
        "ru" : re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+'),
        "en" : re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+'),
        "be" : re.compile(u'[абвгдеёжзійклмнопрстуўфхцчшыьэюя0-9-]+|[.,:;?!]+')
    }
    return language_array[language]

def in_language(language):
    is_lang = False
    language_array = ["ru", "en", "be"]
    for i in language_array:
        if (i == language):
            is_lang = True
    return is_lang

def generate(language, paragraph_count, sentence_count, error_count):
    model = train(get_directory(language))
    return generate_text(paragraph_count, sentence_count, model, error_count, language)

is_input = True
exception = ""
while is_input:
    try:
        is_input = False
        language = raw_input("language (ru, en, be):")
        is_input = not in_language(language)
        paragraph = int(raw_input("paragraph count:"))
        sentence = int(raw_input("sentence count:"))
        error = float(raw_input("error count:"))
    except:
        is_input = True
print(generate(language, paragraph, sentence, error))