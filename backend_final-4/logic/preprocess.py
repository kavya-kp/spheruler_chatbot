import os

def load_stopwords():
    stopwords = set()
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct path to data/stopwords.txt relative to the script's directory
    # Note: preprocess.py is in logic/, data is in ../data/
    data_path = os.path.join(current_dir, '..', 'data', 'stopwords.txt')
    
    with open(data_path, "r") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                stopwords.add(word)
    return stopwords


def expand_genz_language(text):
    """
    Expand Gen Z abbreviations and slang to full words.
    Examples: y -> why, u -> you, r -> are
    """
    genz_map = {
        ' y ': ' why ',
        ' u ': ' you ',
        ' r ': ' are ',
        ' ur ': ' your ',
        ' wat ': ' what ',
        ' wats ': ' what is ',
        ' wht ': ' what ',
        ' hw ': ' how ',
        ' wen ': ' when ',
        ' wer ': ' where ',
        ' whr ': ' where ',
        ' y r ': ' why are ',
        ' y is ': ' why is ',
        ' cuz ': ' because ',
        ' bcuz ': ' because ',
        ' plz ': ' please ',
        ' pls ': ' please ',
        ' thx ': ' thanks ',
        ' thanx ': ' thanks ',
        ' urs ': ' yours ',
        ' tho ': ' though ',
        ' rn ': ' right now ',
        ' gonna ': ' going to ',
        ' wanna ': ' want to ',
        ' gotta ': ' got to ',
        ' dunno ': ' do not know ',
        ' idk ': ' i do not know ',
    }
    
    # Replace Gen Z abbreviations using word-by-word matching
    words = text.lower().split()
    expanded_words = []
    
    # Create a mapping without spaces for easier lookup
    lookup_map = {k.strip(): v.strip() for k, v in genz_map.items()}
    
    for word in words:
        if word in lookup_map:
            expanded_words.append(lookup_map[word])
        else:
            expanded_words.append(word)
    
    return ' '.join(expanded_words)


def correct_common_spelling(text):
    """
    Correct common spelling mistakes in domain-specific terms.
    """
    spelling_corrections = {
        'spheruler': ['speruler', 'spherular', 'spheruller', 'sperular', 'spheruler'],
        'accupan': ['acupan', 'accupann', 'acupann', 'akupan'],
        'fcf': ['fccf', 'fcff', 'fc'],
        'patent': ['pattent', 'patant', 'patnt'],
        'panoramic': ['panoramc', 'panaromic', 'panoramac'],
        'technology': ['tecnology', 'technolgy', 'techology'],
        'imaging': ['imagng', 'imging', 'imageing'],
        'visualization': ['visualisation', 'visualizaton', 'vizualization'],
        'product': ['prodcut', 'produkt', 'porduct'],
        'products': ['prodcuts', 'produkts', 'porducts'],
        'location': ['locaton', 'loction', 'lokation'],
        'mission': ['mision', 'misssion', 'missoin'],
        'vision': ['vison', 'visoin', 'vizion'],
        'contact': ['contct', 'kontact', 'cantact'],
        'founder': ['foonder', 'foundor', 'foundr'],
        'founders': ['foonders', 'foundors', 'foundrs'],
        'karthik': ['kartik', 'karthick', 'kartick'],
        'guru': ['gru', 'guroo'],
    }
    
    words = text.lower().split()
    corrected_words = []
    
    for word in words:
        corrected = word
        # Check if this word is a misspelling
        for correct_word, misspellings in spelling_corrections.items():
            if word in misspellings or word == correct_word:
                corrected = correct_word
                break
        corrected_words.append(corrected)
    
    return ' '.join(corrected_words)


def preprocess(text):
    """
    Preprocess user input by:
    1. Expanding Gen Z language
    2. Correcting spelling
    3. Removing stopwords
    4. Lowercasing
    """
    # Step 1: Expand Gen Z abbreviations
    text = expand_genz_language(text)
    
    # Step 2: Correct common spelling mistakes
    text = correct_common_spelling(text)
    
    # Step 3: Load stopwords and remove them
    stopwords = load_stopwords()
    words = text.lower().split()
    
    # Step 4: Filter out stopwords
    filtered_words = [word for word in words if word not in stopwords]
    
    return filtered_words
