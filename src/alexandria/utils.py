"""
Utility functions, used in different codes
"""

import json

def readSettings(file: str = "settings.json"):
    """
    Read the settings file

    Parameters
    ----------
    file: `str`
        Source file that contains the settings, json
    
    Returns
    -------
    params: `dict`
        Dictionary of settings
    """
    with open(file, "rt", encoding="utf-8") as inp:
        params = json.load(inp)
    return params