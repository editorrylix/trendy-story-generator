document.getElementById("story-form").addEventListener("submit", function (event) {
    event.preventDefault();

    // Collect form data
    const trendSource = document.getElementById("trend-source").value;
    const genre = document.getElementById("genre").value;
    const tone = document.getElementById("tone").value;
    const timePeriod = document.getElementById("time-period").value;
    const duration = document.getElementById("duration").value;
    const includeHashtags = document.getElementById("hashtags").checked;
    const customInput = document.getElementById("custom-input").value; // Custom input field

    // Send data to backend
    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            trendSource,
            genre,
            tone,
            timePeriod,
            duration,
            includeHashtags,
            customInput,  // Include custom input
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("story-content").innerText = data.story;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
