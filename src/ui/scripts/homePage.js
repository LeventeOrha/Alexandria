const currentList = document.getElementById("currentList");
const books = document.querySelectorAll(".currentBook");

let currentIndex = 0;

function updateCurrent() {
    currentList.style.transform = `translateX(-${currentIndex * 100}%)`;
}

document.getElementById("rightArrow").addEventListener("click", () => {
    if (currentIndex < books.length - 1) {
        currentIndex++;
        updateCurrent();
    }
});

document.getElementById("leftArrow").addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCurrent();
    }
});