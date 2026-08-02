// Timeout function
const sleep = (seconds) => new Promise(resolve => setTimeout(resolve, seconds * 1000));

// Function to make a new notification
async function notify(message) {
    const holder = document.getElementById("message-holder")

    const notif = document.getElementById("message")

    holder.classList.add("visible")

    await sleep(0.4)

    notif.textContent = message
    notif.classList.add("visible")

    await sleep(5)

    notif.classList.remove("visible")
    await new Promise(requestAnimationFrame)
    notif.textContent = ""

    await sleep(0.15)

    holder.classList.remove("visible")
}