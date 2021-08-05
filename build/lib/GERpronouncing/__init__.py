import os
import pkg_resources
import zipfile
import site
from itertools import combinations_with_replacement

# Load data
archive = zipfile.ZipFile(site.getsitepackages()[-1]+"\\GERpronouncing\\data\\de_ipa_wiktionary.zip", 'r')

with archive.open("de_ipa_wiktionary.csv") as csvfile:
    wiki_read = csvfile.read().decode('utf-8')
    wiki_rows = [row.split(",") for row in wiki_read.split("\n")[1:-1] if len(row.split(",")) == 4]
    archive.close()

ipa_vowels = ['o','u','i','a','ə','ɐ','ɪ','ʏ','ʊ','e','ɛ','ø','ɔ','œ','y','ɑ','æ','ɯ','ɒ','ε','ɘ','I','U','ɜ','ɝ','ı','ɵ','ʌ','ɨ','õ','ā']


# function to identify the rhyme of a given ipa-word
def get_rhyme(ipa_word):
    rhyme = ipa_word
    # for words with more syllables identify the main stress part of the word
    # and cut off the rest
    if "ˈ" in rhyme:
        while rhyme[0] != "ˈ":
            rhyme = rhyme[1:]
        rhyme = rhyme[1:]
    # cut off all consonants until the next vowel
    for i in rhyme:
        if i not in ipa_vowels:
            rhyme = rhyme[1:]
        else:
            break
    return rhyme

# function to identify the meter of a given ipa-word
def get_meter(ipa_word):
    vowels = []
    string = ""
    for index,letter in enumerate(ipa_word):
        if letter in ["ˌ","ˈ",'̯']:
            string += letter
        if letter in ipa_vowels+['̩','̍'] and index != len(ipa_word)-1:
            string += letter
            if ipa_word[index+1] != '̯':
                vowels.append(string)
                string = ""
        if letter in ipa_vowels+['̩','̍'] and index == len(ipa_word)-1:
            string += letter
            vowels.append(string)
    meter = ""
    for vowel in vowels:
        if "ˈ" in vowel:
            meter += "1"
        elif "ˌ" in vowel:
            meter += "2"
        else:
            meter += "0"
    return meter

# Create dictionaries for easier access
# (This takes a few seconds when GERpronouncing is imported, but improves performance afterwards)
words_dict = {}
rhymes_dict = {}
syllables_dict = {}
meters_dict = {}

for word, lemma, ipa, meter in wiki_rows:
    rhyme = get_rhyme(ipa)
    syllables = len(meter)
    
    if word not in words_dict:
        words_dict[word] = [{"lemma":lemma,"ipa":ipa,"rhyme":rhyme,"syllables":syllables,"meter":meter}]
    else:
        words_dict[word] += [{"lemma":lemma,"ipa":ipa,"rhyme":rhyme,"syllables":syllables,"meter":meter}]
        
    if rhyme not in rhymes_dict:
        rhymes_dict[rhyme] = [word]
    else:
        rhymes_dict[rhyme] += [word]
        
    if meter not in meters_dict:
        meters_dict[meter] = [word]
    else:
        meters_dict[meter] += [word]
        
    if syllables not in syllables_dict:
        syllables_dict[syllables] = [word]
    else:
        syllables_dict[syllables] += [word]
        

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
    
# The possible_forms_of function returns a list of possible forms of a given lemma.
# input: lemma (string)
# output: forms of the given lemma (list)
def possible_forms_of(lemma):
    try:
        return [word[0] for word in wiki_rows if word[1] == lemma]
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
            return [l1 for l2 in [[word for word in rhymes_dict[rhyme_word]] for rhyme_word in rhyme_output] for l1 in l2]
        else:
            return [word for word in rhymes_dict[rhyme_output]]
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
            return [l1 for l2 in [[word for word in syllables_dict[syllables_word]] for syllables_word in syllables_output] for l1 in l2]
        else:
            return [word for word in syllables_dict[syllables_output]]
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
            return [l1 for l2 in [[word for word in meters_dict[meter_word]] for meter_word in meter_output] for l1 in l2]
        else:
            return [word for word in meters_dict[meter_output]]
    except:
        return []
    
# The meters_like function returns a list of words following the same meter pattern of a given pattern (i.e "10002")
# input: pattern (string)
# output: list of words with the same meter pattern (list)
def meters_like(meter_pattern,levels=True):
    try:
        #return list(dict.fromkeys([minidict["lemma"] for minidict in meters_dict[meter_pattern]]))
        return [word for word in meters_dict[meter_pattern]]
    except:
        return []
