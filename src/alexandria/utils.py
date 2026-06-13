"""
Utility functions, used in different codes
"""

import json
import os

SETTINGS = "./datafiles/settings.json"

def checkSettings() -> None:
    if os.path.isfile(SETTINGS):
        return
    
    print(f"Settings file {SETTINGS} is not found!")
    new_settings = input("Add actual settings file (relative/absolute path): ")

    new_param_keys = list(readSettings(new_settings).keys())
    proper_keys = list(createSettings().keys())

    if set(new_param_keys) == set(proper_keys):
        print("All good now!")
        return
    
    s = "These are not the settings we are looking for. Search for properties:"
    s += str(proper_keys).replace("[", "").replace("]", "").replace("'", "")
    s += "Restart program if you have found it. Bye!"
    raise KeyError(s)
            

def readSettings(file: str = SETTINGS) -> dict[str, str]:
    """
    Read the settings file
    
    Returns
    -------
    params: `dict`
        Dictionary of settings
    """
    with open(file, "rt", encoding="utf-8") as inp:
        params = json.load(inp)
    return params

def writeSettings(params: dict) -> None:
    """
    Write `params` dictionary out into the settings file
    """
    with open(SETTINGS, 'wt', encoding="utf-8") as out:
        json.dump(params, out, ensure_ascii=False)
    return

def createSettings() -> dict[str, str]:
    """
    Create factory settings
    """
    params = {}

    # API key storage file
    params["API_file"] = "./datafiles/API.key"

    # Gemini model
    params["Gemini_model"] = "gemini-3.5-flash"

    # Source database
    params["datafile"] = "./datafiles/books.db"

    # Settings and starting prompts for AI
    params["AI_settings"] = "./datafiles/ai.json"

    # Categories translation
    params["categories"] = "./datafiles/categories.yml"

    # Language file for CMD model
    params["Language_file"] = "./datafiles/cmd_langs.yml"

    # Default language
    params["Language"] = "hu"
    
    return params