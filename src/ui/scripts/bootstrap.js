async function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.body.appendChild(script);
    });
}

window.addEventListener("pywebviewready", async () => {
    window.python = new Python()

    window.app = {}

    const [settings, settingsKeys] = await window.python.getSettings()
    window.app.settings = settings
    window.app.settingsKeys = settingsKeys

    const langText = await window.python.getText(settings["Language"])
    window.app.langText = langText

    const inCodeText = langText["inCodeOptions"]
    window.app.inCodeText = inCodeText

    var shelfOptions = await window.python.getShelves()
    shelfOptions.push(inCodeText["new"])
    window.app.shelfOptions = shelfOptions

    const categoryOptions = await window.python.getCategories()
    window.app.categoryOptions = categoryOptions

    await loadScript("scripts/messages.js")
    await loadScript("scripts/onLoad.js")
    await loadScript("scripts/nav.js")
    await loadScript("scripts/homePage.js")
    await loadScript("scripts/searchOnline.js")
    await loadScript("scripts/bookData.js")
    await loadScript("scripts/aiChat.js")
    await loadScript("scripts/settings.js")
})