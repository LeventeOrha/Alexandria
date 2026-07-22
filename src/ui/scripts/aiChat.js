// Send and get new message in AI chat
function createNewMessage(content, sender) {
    // Create a HTML div to straight put in
    // sender MUST BE "ai" or "user"

    // Rewrite message to HTML
    const htmlMessage = marked.parse(content)

    // Create the holder
    const message = document.createElement("div")
    message.className = `${sender}Message`

    // Create the inner span
    const span = document.createElement("span")
    span.className = `${sender}MessageText`

    // Put in text
    span.innerHTML = htmlMessage

    // Wrap it
    message.appendChild(span)

    // Put it out
    document.getElementById("aiBody").appendChild(message)
}

const sendMessage = document.getElementById("sendNewMessage")
function sendNewMessage() {
    // Get the new text from the user
    const textarea = document.getElementById("writeNewMessage")
    var userMessage = textarea.value

    // Clear out text area
    textarea.value = ""

    // Put out the user message
    createNewMessage(userMessage, "user")

    // Get the answer
    const answer = python.getAIMessage(userMessage)

    // Put out the answer
    createNewMessage(answer, "ai")

    // Scroll down to the bottom
    aiBody = document.getElementById("aiBody")
    aiBody.scrollTop = aiBody.scrollHeight
}

sendMessage.addEventListener('click', sendNewMessage)
document.getElementById("writeNewMessage").addEventListener('keydown', (e) => {
    if (e.key != "Enter") return
    sendNewMessage()
})