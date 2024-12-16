document.getElementById('generate-btn').addEventListener('click', async () => {
    const trendSource = document.getElementById('trend-source').value;
    const genre = document.getElementById('genre').value;
    const tone = document.getElementById('tone').value;
    const timePeriod = document.getElementById('time-period').value;
    const duration = document.getElementById('duration').value;
    const includeHashtags = document.getElementById('hashtags').checked;

    // Prepare the request payload
    const payload = {
        trendSource,
        genre,
        tone,
        timePeriod,
        duration,
        includeHashtags
    };

    // Call the backend API
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    // Display the result
    if (response.ok) {
        const data = await response.json();
        document.getElementById('story-content').innerHTML = `<p>${data.story}</p>`;
    } else {
        document.getElementById('story-content').innerHTML = '<p>Error generating story. Try again!</p>';
    }
});
