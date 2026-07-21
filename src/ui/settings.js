// Get current settings from Python
const [params, keys] = python.getSettings()

// Set out all available languages and keys
const selectLanguage = document.getElementById("selectLanguage")
for (const [key, value] of Object.entries(keys["lang"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectLanguage.appendChild(option);
}

// Put out all available gemini models
const selectAI = document.getElementById("selectAI")
for (const [key, value] of Object.entries(keys["gemini-model"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectAI.appendChild(option);
}

// Set current values for all settings
selectLanguage.value = params["lang"]
selectAI.value = params["gemini-model"]
document.getElementById("aiChatColor").value = params["aiColor"]
document.getElementById("userChatColor").value = params["userColor"]

// Save current settings
function saveSettings() {
    const params = {}

    // Get language
    params["lang"] = document.getElementById("selectLanguage").value

    // Get Gemini model
    params["gemini-model"] = document.getElementById("selectAI").value

    // Get AI chat color
    params["aiColor"] = document.getElementById("aiChatColor").value

    // Get user chat color
    params["userColor"] = document.getElementById("userChatColor").value

    // Graphical User Interface usage
    params["GUI"] = document.getElementById("guiUsage").checked

    python.saveSettings(params)
}
document.getElementById("saveSettings").addEventListener("click", saveSettings)

// Export library button function
document.getElementById("exportLibrary").addEventListener("click", python.exportLibrary)

// Import library button function
document.getElementById("importLibrary").addEventListener("click", python.importLibrary)