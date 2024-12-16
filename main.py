from flask import Flask, render_template, request, jsonify
import google.generativeai as genai  # Gemini API
import random

app = Flask(__name__, template_folder="templates")

# Configure Gemini API
API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")  # Load Gemini Pro Model


# ====================== HELPER FUNCTIONS ======================

def fetch_trends(source):
    """
    Simulates fetching trends based on the source.
    Extend this function to integrate real APIs if needed.
    """
    trend_mapping = {
        "google_trends": "AI in Tech",
        "tiktok_api": "Dance Challenges",
        "reddit_api": "Space Exploration Memes",
    }
    return trend_mapping.get(source, "A Viral Phenomenon")


def build_prompt(trend, genre, tone, time_period, duration, include_hashtags):
    """
    Builds a structured prompt to send to the Gemini API.
    """
    prompt = (
        f"Write a short, engaging story incorporating the following details:\n"
        f"- **Trend**: {trend}\n"
        f"- **Genre**: {genre} (Comedy, Horror, Motivational, Mystery, etc.)\n"
        f"- **Tone**: {tone} (Lighthearted, Dark, Inspirational, etc.)\n"
        f"- **Time Period**: {time_period} (Past, Present, Future)\n"
        f"- **Duration**: Fit the story into {duration} seconds.\n"
        f"Include visual elements like stock footages, sound effects, and timestamps for each scene to make it immersive.\n"
    )
    if include_hashtags:
        prompt += "Add relevant hashtags at the end for a social media audience."
    return prompt


def generate_story_with_gemini(prompt):
    """
    Generates content using the Gemini API based on the prompt.
    """
    try:
        response = model.generate_content(prompt)
        story = response.text.strip() if response and response.text else "No story generated."
        return story
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error generating story with Gemini API."


# ====================== ROUTES ======================

@app.route("/", methods=["GET"])
def index():
    """
    Renders the main UI page.
    """
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_story():
    """
    Generates a story based on user input and returns it as JSON.
    """
    try:
        # Parse input data from request
        data = request.get_json()
        trend_source = data.get('trendSource')
        genre = data.get('genre')
        tone = data.get('tone')
        time_period = data.get('timePeriod')
        duration = data.get('duration')
        include_hashtags = data.get('includeHashtags')

        # Fetch trending topic
        trend = fetch_trends(trend_source)

        # Build Gemini prompt
        prompt = build_prompt(trend, genre, tone, time_period, duration, include_hashtags)

        # Generate story
        story = generate_story_with_gemini(prompt)

        # Return response
        return jsonify({
            "story": story,
            "trend": trend
        })

    except Exception as e:
        print(f"Error generating story: {e}")
        return jsonify({
            "story": "Error generating story. Please try again.",
            "trend": "N/A"
        }), 500


# ====================== MAIN ======================

if __name__ == "__main__":
    app.run(debug=True, port=8000)
