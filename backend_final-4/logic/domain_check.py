import os

def load_domain_keywords():
    keywords = set()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'domain_keywords.txt')
    
    with open(data_path, "r") as f:
        for line in f:
            keyword = line.strip().lower()
            if keyword:
                keywords.add(keyword)
    return keywords


def is_domain_valid(words, original_input=""):
    """
    Check if query is related to Spheruler Solutions.
    
    Args:
        words: List of preprocessed words (after stopword removal)
        original_input: Original user input before preprocessing
    
    Returns:
        bool: True if domain is valid, False otherwise
    """
    domain_keywords = load_domain_keywords()
    
    # Check preprocessed words
    for word in words:
        if word.lower() in domain_keywords:
            return True
    
    # IMPROVED: Also check original input for important query words
    original_lower = original_input.lower()
    
    # Common question patterns that should always be considered valid
    generic_company_queries = [
        'where', 'location', 'address', 'contact', 'email', 'phone',
        'who', 'founder', 'started', 'created', 'owner',
        'what', 'company', 'about', 'do', 'offer', 'provide',
        'why', 'mission', 'vision', 'goal', 'purpose',
        'how', 'work', 'works', 'technology', 'tech',
        'product', 'products', 'service', 'services',
        'patent', 'patents', 'innovation',
        'located', 'based', 'situated',
        'spheruler', 'solutions', 'when', 'time'
    ]
    
    # Check if original input contains any of these query words
    for query_word in generic_company_queries:
        if query_word in original_lower:
            return True
    
    return False
