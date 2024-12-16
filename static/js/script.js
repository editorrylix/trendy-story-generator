document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById("generate-btn");
    const resultContainer = document.getElementById("result");

    generateBtn.addEventListener("click", () => {
        resultContainer.innerHTML = "Generating story... 🔄";
        // You can add animations or loading effects here
    });
});
