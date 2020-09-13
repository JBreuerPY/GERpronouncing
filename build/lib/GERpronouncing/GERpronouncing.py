#!/usr/bin/env python
# coding: utf-8

"""A pronounciation lexicon for German with some useful functions to handle it

GERpronouncing provides a set of functions inspired by the pronouncing library (https://pypi.org/project/pronouncing/) which is described as "a simple interface for the CMU Pronouncing Dictionary" (http://www.speech.cs.cmu.edu/cgi-bin/cmudict). These functions comprise ipa code, rhyme extraction, meter recognition and syllable counting. Furthermore each word form entry contains a lemma tag which is usefull for disambiguation of homophones.

The underlying data of the pronounciation lexicon was extracted from wiktionary with the wiktionary_de_parser library (https://pypi.org/project/wiktionary-de-parser/)"""

import pandas as pd
import os
import pkg_resources
import zipfile
import site
from itertools import combinations_with_replacement
import re

# open data in a pandas dataframe
archive = zipfile.ZipFile(site.getsitepackages()[-1]+"\\pronouncingTEST\\data\\de_ipa_wiktionary.zip", 'r')
csvfile = archive.open("de_ipa_wiktionary.csv")
data = pd.read_csv(csvfile, dtype={"syllables":int,"words":"object","ryhmes":"object","meters":"object"})
    
# assign variables to indexed dataframes
Wdata = data.set_index("words")
Mdata = data.set_index("meters")
Rdata = data.set_index("rhymes")
Sdata = data.set_index("syllables")
Ldata = data.set_index("lemma")
Idata = data.set_index("ipa")

########################################################################################
# lemmas
########################################################################################

# The lemmas function returns a list of possible lemmas of a given word
# input: word (string)
# output: list of lemmas (list)
def lemmas(word):
    try:
        if type(Wdata.loc[word]["lemma"]) != str:
            entry = Wdata.loc[word]["lemma"].values.tolist()
        else:
            entry = [Wdata.loc[word]["lemma"]]
        return list(set(entry))
    except:
        return []

# The forms_of function returns a list of forms of a given lemma.
# The info parameter defines which information of the forms will be returned in a list
# it accepts the strings: "words", "lemma", "ipa", "rhymes", "syllables", "meters"
# input: lemma (string), info (integer, default="words")
# output: forms of the given lemma (list)
def forms_of(lemma = "",info="words"):
    try:
        # create iterable list of dataframe entry
        if type(Ldata.loc[lemma][info].values.tolist()) == list:
            iter_list = Ldata.loc[lemma][info].values.tolist()
        else:
            iter_list = [Ldata.loc[lemma][info].values.tolist()]
        # return list with all forms
        return iter_list
    except:
        return []
########################################################################################
# ipa
########################################################################################

# The ipa function returns the ipa code of a given word
# To prevent semantic misunderstandings the lemma can be given as an argument
# Since some words have multiple pronouncation variations, the variation can be chosen by setting the
# "variation" argument with an integer. To get a list of all variations the "variation" argument can be set with
# the string "all".
# input: word (string), lemma (string), variation (integer or string ("all"))
# output: ipa code (string/list)
def ipa(word,lemma = "",variation=0):
    try:
        # choose the correct lemma
        if lemma == "" or lemma not in lemmas(word):
            lemma = lemmas(word)[0]
        # create iterable list of dataframe entry
        if type(Wdata.loc[word].values.tolist()[0]) == list:
            row_list = Wdata.loc[word].values.tolist()
        else:
            row_list = [Wdata.loc[word].values.tolist()]
        # create list with all pronounciation variations
        variations = [i[1] for i in row_list if i[0] == lemma]
        # if variation index is out of index, the highest possible index is assigned
        if type(variation) == int and variation > len(variations) - 1:
            variation = len(variations)-1
        # return the chosen or default ipa variation
        if variation != "all":
            return variations[variation]
        # return a list of all ipa variations
        else:
            return variations
    except:
        if variation != "all":
            return ""
        else:
            return []
    
########################################################################################
# rhyme
########################################################################################
    
# the rhyme function returns the rhyme in ipa code of a given word
# input: word (string), lemma (string), variation (integer or string ("all"))
# output: rhyme/rhyme variations (string/list)
def rhyme(word,lemma = "",variation=0):
    try:
        ipa_word = ipa(word,lemma,variation)
        # choose the correct lemma
        if lemma == "" or lemma not in lemmas(word):
            lemma = lemmas(word)[0]
        # return chosen variation
        if variation != "all":
            # create iterable list of dataframe entry
            if type(Idata.loc[ipa_word].values.tolist()[0]) == list:
                row_list = Idata.loc[ipa_word].values.tolist()
            else:
                row_list = [Idata.loc[ipa_word].values.tolist()]
            # create list with all rhyme variations
            variations = [i[2] for i in row_list if i[1] == lemma]
            # if variation index is out of index, the highest possible index is assigned
            if type(variation) == int and variation > len(variations) - 1:
                variation = len(variations)-1
            return variations[variation]
        # return a list with all variations
        else:
            variations = []
            for ipa_tok in ipa_word:
                # create iterable list of dataframe entry
                if type(Idata.loc[ipa_tok].values.tolist()[0]) == list:
                    row_list = Idata.loc[ipa_tok].values.tolist()
                else:
                    row_list = [Idata.loc[ipa_tok].values.tolist()]
                # create list with all rhyme variations
                variations += [i[2] for i in row_list if i[1] == lemma]
            return variations
    except:
        if variation != "all":
            return ""
        else:
            return []
        
# the rhymes function returns a list of words, that rhyme with a given word
# input: word (string), lemma (string), variation (integer or string ("all"))
# output: list of rhyming words (list)
def rhymes(word,lemma = "",variation=0):
    try:
        ipa_word = ipa(word,lemma,variation)
        rhyme_word = rhyme(word,lemma,variation)
        # return a list with rhyme words of the specified variation
        if variation != "all":
            # create iterable list of dataframe entry
            if type(Rdata.loc[rhyme_word].values.tolist()[0]) == list:
                tok_list = Rdata.loc[rhyme_word].values.tolist()
            else:
                tok_list = [Rdata.loc[rhyme_word].values.tolist()]
            all_rhymes = [tok[0] for tok in tok_list if tok[0] != word]
            return all_rhymes
        # return a list with rhyme words of all variations
        else:
            all_rhymes = []
            for rhyme_tok in rhyme_word:
                # create iterable list of dataframe entry
                if type(Rdata.loc[rhyme_tok].values.tolist()[0]) == list:
                    tok_list = Rdata.loc[rhyme_tok].values.tolist()
                else:
                    tok_list = [Rdata.loc[rhyme_tok].values.tolist()]
                all_rhymes += [tok[0] for tok in tok_list if tok[0] != word]
            return all_rhymes
    except:
        return []
    
########################################################################################
# syllables
########################################################################################
    
# the count_syllables function returns the number of syllables a given word contains
# input: word (string), lemma (string), variation (integer or string ("all"))
# output: number of syllables/list of all possible syllable variations (integer/list)
def count_syllables(word,lemma = "",variation=0):
    try:
        # choose the correct lemma
        if lemma == "" or lemma not in lemmas(word):
            lemma = lemmas(word)[0]
        # create iterable list of dataframe entry
        if type(Wdata.loc[word].values.tolist()[0]) == list:
            iter_list = Wdata.loc[word].values.tolist()
        else:
            iter_list = [Wdata.loc[word].values.tolist()]
        variations = [i[3] for i in iter_list if i[0] == lemma]
        if variation != "all":
            # if variation index is out of index, the highest possible index is assigned
            if type(variation) == int and variation > len(variations) - 1:
                variation = len(variations)-1
            return variations[variation]
        return variations
    except:
        if variation != "all":
            return ""
        else:
            return []
    
# the same_syllables function returns a list of words, consisting of the same number of syllables as a given word
# input: word (string), lemma (string), variation (integer)
# output: list of words with the same number of syllables (list)
def same_syllables(word,lemma = "",variation=0):
    try:
        if type(variation) != int:
            variation = 0
        # create iterable list of dataframe entry
        if type(Sdata.loc[count_syllables(word)].values.tolist()[0]) == list:
            iter_list = Sdata.loc[count_syllables(word)].values.tolist()
        else:
            iter_list = [Sdata.loc[count_syllables(word)].values.tolist()]
        syllables_list = [tok[0] for tok in iter_list if tok[0] != word]
        return syllables_list
    except:
        []

########################################################################################
# meter
# the following functions can be used to work with metrical characteristics
# the meter ist extraced by assigning the following stress levels to every syllable:
# 0: unstressed
# 1: primary stress
# 2: secondary stress
########################################################################################

# The meter function simply returns the meter pattern of a given word
# input: word (string), lemma (string), variation (integer)
# output: peter pattern (string)
def meter(word,lemma = "",variation=0):
    try:
        # choose the correct lemma
        if lemma == "" or lemma not in lemmas(word):
            lemma = lemmas(word)[0]
        # create iterable list of dataframe entry
        if type(Wdata.loc[word].values.tolist()[0]) == list:
            row_list = Wdata.loc[word].values.tolist()
        else:
            row_list = [Wdata.loc[word].values.tolist()]
        # create list with all pronounciation variations
        variations = [i[4] for i in row_list if i[0] == lemma]
        # if variation index is out of index, the highest possible index is assigned
        if type(variation) == int and variation > len(variations) - 1:
            variation = len(variations)-1
        # return the chosen or default ipa variation
        if variation != "all":
            return variations[variation]
        # return a list of all ipa variations
        else:
            return variations
    except:
        if variation != "all":
            return ""
        else:
            return []
    
# The meters function returns a list of words following the same meter pattern of a given word
# input: word (string), lemma (string), variation (integer)
# output: list of words with the same meter pattern (string)
def meters(word,lemma = "",variation=0):
    try:
        meter_tok = meter(word,lemma = "",variation=0)
        # if not so yet convert meter_tok to list
        if type(meter_tok[0]) != list:
            meter_tok = [meter_tok]
        meters_list = []
        # itereate over meter_tok and add result to meters_list
        for m_list in meter_tok:
            # create iterable list of dataframe entry
            if type(Mdata.loc[meter_tok].values.tolist()[0]) == list:
                iter_list = Mdata.loc[meter_tok].values.tolist()
            else:
                iter_list = [Mdata.loc[meter_tok].values.tolist()]
            meters_list = [tok[0] for tok in iter_list if tok[0] != word]
        return meters_list
    except:
        return []
    
# The meters_like function returns a list of words following the same meter pattern of a given pattern (i.e "10002")
# input: pattern (string)
# output: list of words with the same meter pattern (list)
def meters_like(meter_pattern,levels=True):
    try:
        # create iterable list
        if type(Mdata.loc[meter_pattern].values.tolist()[0]) == list:
            same_pattern_words = Mdata.loc[meter_pattern].values.tolist()
        else:
            same_pattern_words = [Mdata.loc[meter_pattern].values.tolist()]
        # return wordlist with respect to stress levels
        if levels == True:
            return [tok[0] for tok in same_pattern_words]
        # ignore stress levels
        else:
            # create a list of syllables, where stressed syllables are an empty string and unstressed ones stay 0
            pattern_list = [re.sub(r"1|2","",i) for i in meter_pattern]
            # create a list with only stressed syllables
            stresses = tuple([i for i in meter_pattern if i != "0"])
            # create a list with combinations of possible stressed patterns
            stressed_combinations = list(combinations_with_replacement(stresses,len(stresses)))
            # create an empty list for pattern variations to be filled in
            all_patterns = []
            # fill in the pattern variations
            for pattern_part in stressed_combinations+[stresses]:
                tape = list(pattern_part)
                new_list = pattern_list.copy()
                for index, stress_level in list(enumerate(pattern_list)):
                    if stress_level != "0":
                        new_list[index] = tape.pop(0)
                all_patterns += [new_list]
            # create a list of all patterns which are existing in the data
            all_patterns_strings = ["".join(pattern) for pattern in all_patterns if "".join(pattern) in data["meters"].values.tolist()]
            # create the final list with all stress variations
            meters_like_no_level = [l1 for l2 in [meters_like(p) for p in all_patterns_strings] for l1 in l2]
            # return the list
            return meters_like_no_level
    except:
        return []