#!/usr/bin/env python
# coding: utf-8

"""A pronounciation lexicon for German with some useful functions to handle it

GERpronouncing provides a set of functions inspired by the pronouncing library (https://pypi.org/project/pronouncing/) which is described as "a simple interface for the CMU Pronouncing Dictionary" (http://www.speech.cs.cmu.edu/cgi-bin/cmudict). These functions comprise ipa code, rhyme extraction, meter recognition and syllable counting. Furthermore each word form entry contains a lemma tag which is usefull for disambiguation of homophones.

The underlying data of the pronounciation lexicon was extracted from wiktionary with the wiktionary_de_parser library (https://pypi.org/project/wiktionary-de-parser/)"""

import os
import pkg_resources
import zipfile
import site
from itertools import combinations_with_replacement

# open data
archive = zipfile.ZipFile(site.getsitepackages()[-1]+"\\GERpronouncing\\data\\de_ipa_wiktionary.zip", 'r')
with archive.open("de_ipa_wiktionary.csv") as csvfile:
    wiki_read = csvfile.read().decode('utf-8')
    wiki_rows = [row.split(",") for row in wiki_read.split("\r\n")[1:-1]]
    archive.close()
    
words_dict = {}
lemmas_dict = {}
ipas_dict = {}
rhymes_dict = {}
syllables_dict = {}
meters_dict = {}

for row in wiki_rows:
    if row[0] not in words_dict:
        words_dict[row[0]] = [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
    else:
        words_dict[row[0]] += [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
        
    if row[1] not in lemmas_dict:
        lemmas_dict[row[1]] = [{"word":row[0],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
    else:
        lemmas_dict[row[1]] += [{"word":row[0],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
        
    if row[2] not in ipas_dict:
        ipas_dict[row[2]] = [{"lemma":row[1],"word":row[0],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
    else:
        ipas_dict[row[2]] += [{"lemma":row[1],"word":row[0],"rhyme":row[3],"syllables":row[4],"meter":row[5]}]
        
    if row[3] not in rhymes_dict:
        rhymes_dict[row[3]] = [{"lemma":row[1],"ipa":row[2],"word":row[0],"syllables":row[4],"meter":row[5]}]
    else:
        rhymes_dict[row[3]] += [{"lemma":row[1],"ipa":row[2],"word":row[0],"syllables":row[4],"meter":row[5]}]
        
    if row[4] not in syllables_dict:
        syllables_dict[row[4]] = [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"word":row[0],"meter":row[5]}]
    else:
        syllables_dict[row[4]] += [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"word":row[0],"meter":row[5]}]
        
    if row[5] not in meters_dict:
        meters_dict[row[5]] = [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"word":row[0]}]
    else:
        meters_dict[row[5]] += [{"lemma":row[1],"ipa":row[2],"rhyme":row[3],"syllables":row[4],"word":row[0]}]

########################################################################################
# lemmas
########################################################################################

# The lemmas function returns a list of possible lemmas of a given word
# input: word (string)
# output: list of lemmas (list)
def lemmas(word):
    try:
        return list(dict.fromkeys([minidict["lemma"] for minidict in words_dict[word]]))
    except:
        return []
    
# The forms_of function returns a list of forms of a given lemma.
# The info parameter defines which information of the forms will be returned in a list
# it accepts the strings: "words", "lemma", "ipa", "rhymes", "syllables", "meters"
# input: lemma (string), info (integer, default="words")
# output: forms of the given lemma (list)
def forms_of(lemma = "",info="word"):
    if info in ["words","rhymes","meters"]:
        info = info[:-1]
    try:
        return list(dict.fromkeys([minidict[info] for minidict in lemmas_dict[lemma]]))
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
        if variation == "all":
            if lemma == "" or lemma not in lemmas(word):
                return list(dict.fromkeys([minidict["ipa"] for minidict in words_dict[word] if minidict["lemma"] == words_dict[word][0]["lemma"]]))
            else:
                return list(dict.fromkeys([minidict["ipa"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))
        else:
            if lemma == "" or lemma not in lemmas(word):
                return words_dict[word][variation]["ipa"]
            else:
                return list(dict.fromkeys([minidict["ipa"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))[variation]
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
        if variation == "all":
            if lemma == "" or lemma not in lemmas(word):
                return list(dict.fromkeys([minidict["rhyme"] for minidict in words_dict[word] if minidict["lemma"] == words_dict[word][0]["lemma"]]))
            else:
                return list(dict.fromkeys([minidict["rhyme"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))
        else:
            if lemma == "" or lemma not in lemmas(word):
                return words_dict[word][variation]["rhyme"]
            else:
                return list(dict.fromkeys([minidict["rhyme"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))[variation]
    except:
        if variation != "all":
            return ""
        else:
            return []
        
# the rhymes function returns a list of words, that rhyme with a given word
# input: word (string), lemma (string), variation (integer or string ("all"))
# output: list of rhyming words (list)
def rhymes(word,lemma = "",variation=0):
    rhyme_output = rhyme(word,lemma,variation)
    try:
        if variation == "all":
            return list(dict.fromkeys([l1 for l2 in [[minidict["word"] for minidict in rhymes_dict[rhyme_word] if minidict["word"] != word] for rhyme_word in rhyme_output] for l1 in l2]))
        else:
            return list(dict.fromkeys([rhyme["word"] for rhyme in rhymes_dict[rhyme_output] if rhyme["word"] != word]))
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
        if variation == "all":
            if lemma == "" or lemma not in lemmas(word):
                return list(dict.fromkeys([minidict["syllables"] for minidict in words_dict[word] if minidict["lemma"] == words_dict[word][0]["lemma"]]))
            else:
                return list(dict.fromkeys([minidict["syllables"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))
        else:
            if lemma == "" or lemma not in lemmas(word):
                return words_dict[word][variation]["syllables"]
            else:
                return list(dict.fromkeys([minidict["syllables"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))[variation]
    except:
        if variation != "all":
            return ""
        else:
            return []
        
# the same_syllables function returns a list of words, consisting of the same number of syllables as a given word
# input: word (string), lemma (string), variation (integer)
# output: list of words with the same number of syllables (list)
def same_syllables(word,lemma = "",variation=0):
    syllables_output = count_syllables(word,lemma,variation)
    try:
        if variation == "all":
            return list(dict.fromkeys([l1 for l2 in [[minidict["word"] for minidict in syllables_dict[syllables_word]] for syllables_word in syllables_output] for l1 in l2]))
        else:
            return list(dict.fromkeys([syllables["word"] for syllables in syllables_dict[syllables_output]]))
    except:
        return []
    
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
        if variation == "all":
            if lemma == "" or lemma not in lemmas(word):
                return list(dict.fromkeys([minidict["meter"] for minidict in words_dict[word] if minidict["lemma"] == words_dict[word][0]["lemma"]]))
            else:
                return list(dict.fromkeys([minidict["meter"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))
        else:
            if lemma == "" or lemma not in lemmas(word):
                return words_dict[word][variation]["meter"]
            else:
                return list(dict.fromkeys([minidict["meter"] for minidict in words_dict[word] if minidict["lemma"] == lemma]))[variation]
    except:
        if variation != "all":
            return ""
        else:
            return []
        
# The meters function returns a list of words following the same meter pattern of a given word
# input: word (string), lemma (string), variation (integer)
# output: list of words with the same meter pattern (string)
def meters(word,lemma = "",variation=0):
    meter_output = meter(word,lemma,variation)
    try:
        if variation == "all":
            return list(dict.fromkeys([l1 for l2 in [[minidict["word"] for minidict in meters_dict[meter_word]] for meter_word in meter_output] for l1 in l2]))
        else:
            return list(dict.fromkeys([meter["word"] for meter in meters_dict[meter_output]]))
    except:
        return []
    
# The meters_like function returns a list of words following the same meter pattern of a given pattern (i.e "10002")
# input: pattern (string)
# output: list of words with the same meter pattern (list)
def meters_like(meter_pattern,levels=True):
    try:
        return list(dict.fromkeys([minidict["word"] for minidict in meters_dict[meter_pattern]]))
    except:
        return []
