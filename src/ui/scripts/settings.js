// Set out all available languages and keys
const selectLanguage = document.getElementById("selectLanguage")
for (const [key, value] of Object.entries(settingsKeys["Language"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectLanguage.appendChild(option);
}

// Put out all available gemini models
const selectAI = document.getElementById("selectAI")
for (const [key, value] of Object.entries(settingsKeys["Gemini_model"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectAI.appendChild(option);
}

// Set current values for all settings
selectLanguage.value = settings["Language"]
selectAI.value = settings["Gemini_model"]
document.getElementById("aiChatColor").value = settings["aiColor"]
document.getElementById("userChatColor").value = settings["userColor"]
document.getElementById("backgroundImage").textContent = settings["background"]
document.getElementById("googleBooksKey").value = settings["GBooksAPIkey"]
document.getElementById("geminiKey").value = settings["GeminiAPI"]

// Save current settings
function saveSettings() {
    const settings = {}

    // Get language
    settings["Language"] = document.getElementById("selectLanguage").value

    // Get Gemini model
    settings["Gemini_model"] = document.getElementById("selectAI").value

    // Get AI chat color
    settings["aiColor"] = document.getElementById("aiChatColor").value

    // Get user chat color
    settings["userColor"] = document.getElementById("userChatColor").value

    // Graphical User Interface usage
    settings["GUI_useage"] = document.getElementById("guiUsage").checked

    // Get background image
    settings["background"] = document.getElementById("backgroundImage").textContent

    // Gemini API key
    settings["GeminiAPI"] = document.getElementById("geminiKey").value

    // Google Books API key
    settings["GBooksAPIkey"] = document.getElementById("googleBooksKey").value

    python.saveSettings(settings)
}
document.getElementById("saveSettings").addEventListener("click", saveSettings)

// Export library button function
document.getElementById("exportLibrary").addEventListener("click", python.exportLibrary)

// Import library button function
document.getElementById("importLibrary").addEventListener("click", python.importLibrary)

// Background changing button
document.getElementById("backgroundImage").addEventListener("click", () => {
    const filename = python.backgroundChange()
    document.getElementById("backgroundImage").textContent = filename
})