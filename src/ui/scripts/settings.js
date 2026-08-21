// Set out all available languages and keys
const selectLanguage = document.getElementById("selectLanguage")
for (const [key, value] of Object.entries(window.app.settingsKeys["Language"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectLanguage.appendChild(option);
}

// Put out all available gemini models
const selectAI = document.getElementById("selectAI")
for (const [key, value] of Object.entries(window.app.settingsKeys["Gemini_model"])) {
    const option = document.createElement("option");
    option.value = key;          // value attribute
    option.textContent = value;  // visible text
    selectAI.appendChild(option);
}

// Set current values for all settings
selectLanguage.value = window.app.settings["Language"]
selectAI.value = window.app.settings["Gemini_model"]
document.getElementById("aiChatColor").value = window.app.settings["aiColor"]
document.getElementById("userChatColor").value = window.app.settings["userColor"]
document.getElementById("backgroundImage").textContent = window.app.settings["background"]
document.getElementById("googleBooksKey").value = window.app.settings["GBooksAPIkey"]
document.getElementById("geminiKey").value = window.app.settings["GeminiAPI"]
document.getElementById("toReadShelves").value = window.app.settings["toReadShelf"]
document.getElementById("ownedShelves").value = window.app.settings["ownedShelf"]

// Save current settings
async function saveSettings() {
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

    // Big shelf name
    settings["toReadShelf"] = document.getElementById("toReadShelves").value

    // Small shelf name
    settings["ownedShelf"] = document.getElementById("ownedShelves").value

    await window.python.saveSettings(settings)

    notify(window.app.inCodeText["SuccessfulSave"])
}
document.getElementById("saveSettings").addEventListener("click", saveSettings)

// Export library button function
document.getElementById("exportLibrary").addEventListener("click", window.python.exportLibrary)

// Import library button function
document.getElementById("importLibrary").addEventListener("click", window.python.importLibrary)

// Background changing button
document.getElementById("backgroundImage").addEventListener("click", async () => {
    const filename = await window.python.backgroundChange()
    document.getElementById("backgroundImage").textContent = filename
})