
# GERpronouncing
A pronounciation lexicon for German with some useful functions to handle it

GERpronouncing provides a set of functions inspired by the *pronouncing* library (https://pypi.org/project/pronouncing/) which is described as "a simple interface for the CMU Pronouncing Dictionary" (http://www.speech.cs.cmu.edu/cgi-bin/cmudict). These functions comprise **ipa code, rhyme extraction, meter recognition** and **syllable counting**. Furthermore each word form entry contains a **lemma** tag which is usefull for disambiguation of homographs. Semantic disambiguation for words with lemmas which are written in the same othographic way but inherit different meanings can only partially be handeld by choosing a **pronounciation variation** (see bellow).

The underlying data of the pronounciation lexicon was extracted from wiktionary with the *wiktionary_de_parser* library (https://pypi.org/project/wiktionary-de-parser/)

# Installing the package from the github directory
```python
pip install git+https://github.com/JBreuerPY/GERpronouncing
```

# Importing the module like this


```python
import GERpronouncing as gp
```

# 1. Getting started: IPA

#### 1.1 IPA code: The international phonetic alphabet is the formal system used here to describe phonetic realisation of written Text
The `GERpronouncing.ipa(word,lemma,variation)` function returns the ipa code of a given word.

To prevent semantic misunderstandings the `lemma` parameter can set with a string containing the lemma of the word.

Since some words have multiple pronouncation variations, the variation can be chosen by setting the
variation parameter with an integer. To get a list of all variations the `variation` argument can be set with
the string `"all"`.

The `lemma` and the `variation` parameter are optional. Per default they choose the first availabe index of the data.
- input: word (string), lemma (string), variation (integer or string ("all"))
- output: ipa code (string/list)


```python
# IPA of the word "Montage" with the lemma "Montag", default variation
print(gp.ipa("Montage",lemma="Montag"))
# IPA of the word "Montage" with the lemma "Montage", default variation
print(gp.ipa("Montage",lemma="Montage"))
# 2nd Variation (index 1)
print(gp.ipa("Montage",lemma="Montag",variation=1))
# list with all variations
print(gp.ipa("Montage",lemma="Montag",variation="all"))
```

    ˈmoːntaːɡə
    mɔnˈtaːʒə
    ˈmoːnˌtaːɡə
    ['ˈmoːntaːɡə', 'ˈmoːnˌtaːɡə']
    

# 2. Rhyme

#### 2.1 Rhyme ending in IPA code
The `GERpronouncing.rhyme(word,lemma,variation)` function returns the rhyme in IPA code of a given word
if the word is unknown and unable to disambiguate an empty string will be returned.
- input: word (string), lemma (string), variation (integer or string ("all"))
- output: rhyme (string/list)


```python
# rhyme of the word "Bug" with the lemma "Bug", default variation
print(gp.rhyme("Bug",lemma="Bug"))
# rhyme Variation (index 1)
print(gp.rhyme("Bug",lemma="Bug",variation=1))
# rhyme with all variations
print(gp.rhyme("Bug",lemma="Bug",variation="all"))
```

    aɡ
    uːk
    ['aɡ', 'uːk']
    

#### 2.2 Create a list of rhyming words

The `GERpronouncing.rhymes(word,lemma,variation)` function returns a list of words, that rhyme with a given word.
- input: word (string), lemma (string), variation (integer or string ("all"))
- output: list of rhyming words (list)


```python
# list of rhyming words of 1st variation (index 0)
print(gp.rhymes("überfahren",variation=0)[:5])
# list of rhyming words of 2nd variation (index 1)
print(gp.rhymes("überfahren",variation=1)[:5])
# setting the variation parameter on "all" will return a list of rhyming words of all variations
print(gp.rhymes("überfahren",variation="all")[:5])
```

    ['herüberfahren', 'überfahren', 'vorüberfahren']
    ['Bibliothekaren', 'viviparen', 'solaren', 'Husaren', 'Zaren']
    ['herüberfahren', 'überfahren', 'vorüberfahren', 'Bibliothekaren', 'viviparen']
    

# 3. Syllables

#### 3.1 Counting syllables

The `GERpronouncing.count_syllables(word,lemma,variation)` function returns the number of syllables a given word contains.
- input: word (string), lemma (string), variation (integer or string ("all"))
- output: number of syllables (integer/list)


```python
print(gp.count_syllables("Computerlinguistik"))
```

    6
    

#### 3.2 Creating a list of words with the same number of syllables

The `GERpronouncing.same_syllables(word,lemma,variation)` function returns a list of words consisting of the same number of syllables as a given word
- input: word (string), lemma (string), variation (integer/string)
- output: list of words with the same number of syllables (list)


```python
# Print the first 5 examples
print(gp.same_syllables("Computerlinguistik")[:5])
```

    ['Lüftungsanlagenbaus', 'hinaufgeklommene', 'medikamentierter', 'graphithaltigeres', 'Institutsleiterin']
    

# 4. Meter
The following functions can be used to work with metrical characteristics.
The meter ist extraced by assigning the following *stress levels* to every syllable:
- 0: unstressed
- 1: primary stress
- 2: secondary stress


#### 4.1 Meter pattern

The `GERpronouncing.meter(word,lemma,variation)` function simply returns the **meter pattern** of a given word
- input: word (string), lemma (string), variation (integer/string)
- output: peter pattern (string/list)


```python
print(gp.meter("übersetzen",variation=0))
print(gp.meter("übersetzen",variation=1))
print(gp.meter("übersetzen",variation="all"))
```

    1020
    2010
    ['1020', '2010']
    

#### 4.2 Creating a list of words following the same meter pattern

The `GERpronouncing.meters(word,lemma,variation)` function returns a list of words following the same meter pattern of a given word.
- input: word (string), lemma (string), variation (integer)
- output: list of words with the same meter pattern (string)


```python
# Print the first 5 examples
print(gp.meters("Veranstaltung")[:5])
```

    ['gecharterte', 'bewertenden', 'durchgeistigter', 'beträchtliche', 'begönnerte']
    

#### 4.3 Creating a list of words using a self defined metre pattern

The `GERpronouncing.meters_like(pattern)` function returns a list of words following the same meter pattern of a given pattern (i.e "10002")
- input: pattern (string)
- output: list of words with the same meter pattern (list)


```python
# Print the first 5 examples of the pattern "10"
print(gp.meters_like("10")[:5])
```

    ['tätschlet', 'handeln', 'langen', 'tempern', 'Classics']
    

# 5. Lemmas

#### 5.1 Looking up possible lemmas of words

The `GERpronouncing.lemmas(word)` function returns a list of all possible lemmas of a given word.
- input: word (string)
- output: list of lemmas (list)


```python
# list of possible lemmas of "Montage"
print(gp.lemmas("Montage"))
```

    ['Montage', 'Montag']
    

#### 5.2 Looking up possible forms of lemmas

The `GERpronouncing.forms_of(word)` function returns a list of forms of a given lemma.
- input: lemma (string)
- output: forms of the given lemma (list)


```python
print(gp.forms_of("Montag"))
```

    ['Montages', 'Montag', 'Montagen', 'Montage', 'Montags']
    


```python

```
