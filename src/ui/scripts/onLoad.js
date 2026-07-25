// Functions to run at the start of the app

// Shortcut API connection
// With safeguard, using actual python when available, otherwise the dummy js class
let python = new Python(); // start with dummy

window.addEventListener('pywebviewready', () => {
    python = window.pywebview.api;
    console.log("Switched to real API");
});

// Get all settings now
const [settings, settingsKeys] = python.getSettings()

// Set background image and chat colors
document.documentElement.style.setProperty("--user-chat-bg", settings["userColor"]) // User message color
document.documentElement.style.setProperty("--ai-chat-bg", settings["aiColor"]) // AI message color
document.documentElement.style.setProperty("--background-image", `url(${settings["background"]})`) // Background image

// Set ai message text colors based on their backgrounds
function getTextColor(hex) {
    // Remove '#'
    hex = hex.replace("#", "")

    // Expand shorthand (#abc → #aabbcc)
    if (hex.length === 3) {
        hex = hex.split("").map(c => c + c).join("")
    }

    const r = parseInt(hex.substring(0, 2), 16)
    const g = parseInt(hex.substring(2, 4), 16)
    const b = parseInt(hex.substring(4, 6), 16)

    // Perceived brightness
    const brightness = (r * 299 + g * 587 + b * 114) / 1000

    return brightness > 128 ? "#000000" : "#FFFFFF"
}
document.documentElement.style.setProperty("--user-chat-color", getTextColor(settings["userColor"]))
document.documentElement.style.setProperty("--ai-chat-color", getTextColor(settings["aiColor"]))

// Get language-fitting text
const langText = python.getText(settings["Language"])

// Fill up the HTML text first
// Placeholders first
for (const [key, value] of Object.entries(langText["placeholders"])) {
    document.getElementById(key).placeholder = value
}

// textContents next
for (const [key, value] of Object.entries(langText["textContents"])) {
    document.getElementById(key).textContent = value
}

// "Export" in-code text into this dict
const inCodeText = langText["inCodeOptions"]

// Get shelves and categories
var shelfOptions = python.getShelves()
shelfOptions.push(inCodeText["new"])
const categoryOptions = python.getCategories()

// Set the distance from the left edge of main divs on startup
const navHolder = document.querySelector(".nav-holder");
const mainDivs = document.querySelectorAll(".main")

function positionMain() {
    const navWidth = navHolder.getBoundingClientRect().width;
    const vw = window.innerWidth * 0.015; // 1.5vw in pixels

    const left = navWidth + vw;

    mainDivs.forEach(div => {
        div.style.left = `${left}px`;
    });
}

positionMain();
// And at every resize
window.addEventListener("resize", positionMain);

// Change all select to a text input if "New" is picked
document.addEventListener("change", function (event) {
  const select = event.target;

  if (select.tagName === "SELECT" && select.value === inCodeText["new"]) {
    const input = document.createElement("input");

    // Preserve id and class
    input.id = select.id;
    input.className = select.className;

    // Optional: preserve other useful attributes
    input.name = select.name;
    input.type = "text";

    // Replace the select
    select.replaceWith(input);

    // Optional: focus the new input
    input.focus();
  }
});