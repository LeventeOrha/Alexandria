"""
Code that handles category names
Reading categories in from the categories.yml file
"""

import alexandria.utils as u
import yaml

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