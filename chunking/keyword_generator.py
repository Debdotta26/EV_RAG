"""
keyword_generator.py

Hybrid Keyword Generator

Features
--------
✓ Stopword removal
✓ Number & punctuation removal
✓ Lemmatization
✓ Domain keyword boosting
✓ Bigram extraction
✓ Heading boosting
✓ Duplicate removal
✓ Frequency-based ranking
"""

import re
from collections import Counter

try:
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
except Exception:
    lemmatizer = None


STOPWORDS = {
    "the","and","of","to","in","for","on","with","is","are",
    "was","were","be","been","being","that","this","these",
    "those","as","at","by","or","an","a","from","into","it",
    "its","their","there","which","during","after","before",
    "about","under","against","overall","all","india"
}


DOMAIN_TERMS = {
    "wheat","rice","maize","mustard","jowar","bajra","millet",
    "cotton","onion","potato","tomato",
    "rainfall","weather","temperature",
    "reservoir","groundwater","fertilizer",
    "fertilizers","seed","seeds",
    "harvest","harvesting","crop","crops",
    "pest","disease",
    "cyclone","cyclonic",
    "forecast","monsoon",
    "horticulture",
    "rabi","kharif","summer",
    "irrigation","moisture",
    "yield","production",
    "storage","water",
    "pulse","pulses",
    "oilseed"
}


def normalize(word):

    word = word.lower()

    if lemmatizer:
        try:
            word = lemmatizer.lemmatize(word)
        except:
            pass

    return word


def tokenize(text):

    words = re.findall(r"[a-zA-Z]+", text.lower())

    tokens = []

    for word in words:

        word = normalize(word)

        if len(word) < 3:
            continue

        if word in STOPWORDS:
            continue

        tokens.append(word)

    return tokens


def generate_keywords(text,
                      heading="",
                      top_n=10):

    words = tokenize(text)

    unigram = Counter(words)

    # -----------------------
    # Bigrams
    # -----------------------

    bigrams = Counter()

    for i in range(len(words)-1):

        phrase = words[i] + " " + words[i+1]

        bigrams[phrase] += 2

    # -----------------------
    # Domain boost
    # -----------------------

    for term in DOMAIN_TERMS:

        if term in unigram:
            unigram[term] += 5

    # -----------------------
    # Heading boost
    # -----------------------

    heading_words = tokenize(heading)

    for word in heading_words:

        unigram[word] += 6

    # -----------------------
    # Merge scores
    # -----------------------

    scores = {}

    for k,v in unigram.items():

        scores[k] = scores.get(k,0)+v

    for k,v in bigrams.items():

        scores[k] = scores.get(k,0)+v

    # -----------------------
    # Remove weak keywords
    # -----------------------

    scores = {

        k:v

        for k,v in scores.items()

        if v>=2

    }

    # -----------------------
    # Sort
    # -----------------------

    keywords = sorted(

        scores.items(),

        key=lambda x:(x[1],len(x[0])),

        reverse=True

    )

    final=[]

    seen=set()

    for word,_ in keywords:

        if word not in seen:

            final.append(word)

            seen.add(word)

        if len(final)>=top_n:
            break

    return final