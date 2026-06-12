"""
Code that handles category names
Reading categories in from the categories.yml file
"""

import alexandria.utils as u
import yaml
import re
import unicodedata

def readCategories():
    """
    Read categories and their translations
    """
    params = u.readSettings()

    with open(params["categories"], "rt", encoding="utf-8") as inp:
        categories = yaml.safe_load(inp)

    return categories

def translateCategories(cats: list, lang: str = "en"):
    """
    Translate a list of categories into what is in the database

    Returns
    -------
    res: `list[str]`
        Translated AND filtered categories
    """
    categories = readCategories()

    if lang not in next(iter(categories.values())):
        raise NotImplementedError(f"Language '{lang}' is not available yet. Sorry!")

    res = []

    cats[:] = [s.lower() for s in cats]

    for key in categories:
        if categories[key][lang].lower() in cats:
            if key not in res: # Avoid double categories
                res.append(key)
    
    return res

def normalizeText(s: str):
    """
    From a complicated text, make it just English alphabet characters
    Replace every sign with "+"
    """
    # Decompose unicode characters
    s = unicodedata.normalize("NFKD", s)

    # Remove diacritics (accents)
    s = "".join(c for c in s if not unicodedata.combining(c))

    # Replace non-alphanumeric runs with "+"
    s = re.sub(r"[^A-Za-z0-9]+", "-", s)

    # Trim leading/trailing "+"
    s = s.strip("+")
    
    return s