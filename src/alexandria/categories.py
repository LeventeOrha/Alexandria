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

