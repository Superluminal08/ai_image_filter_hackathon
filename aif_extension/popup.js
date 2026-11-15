let text = "Button Clicked!";
let nextText = "Button Unclicked!";

document.getElementById("change-btn").addEventListener("click", () => {
    document.querySelector("h3").textContent = text;
    let temp = text;
    text = nextText;
    nextText = temp;

});