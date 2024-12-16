from flask import Flask, render_template, request, jsonify
import google.generativeai as genai  # Import Gemini API
import random

app = Flask(__name__, template_folder="templates")

# Configure Gemini API
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

# Function to fetch trends
def fetch_trends(source):
    if source == "google_trends":
        return "AI in Tech"
    elif source == "tiktok_api":
        return "Dance Challenges"
    elif source == "reddit_api":
        return "Space Exploration Memes"
    else:
        return "A Viral Phenomenon"

# Function to generate a story using Gemini API
def generate_story_with_gemini(trend, genre, tone, time_period, duration):
    prompt = (
        f"Write a short story incorporating the following elements:\n"
        f"- Trend: {trend}\n"
        f"- Genre: {genre} (e.g., Comedy, Horror, Motivational, Mystery, etc.)\n"
        f"- Tone: {tone} (e.g., Lighthearted, Dark, Inspirational, etc.)\n"
        f"- Time Period: {time_period} (e.g., Past, Present, Future)\n"
        f"- Duration: The story should be concise and fit within {duration}.\n"
        f"Make the story engaging and creative while adhering to the trend and genre."
        "Also Include the sound effects and visual elemnts(Stock Footages) required at each subtitles with the video timestamp"
    )

    # Call Gemini API
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        story = response.text.strip() if response.text else "No story generated."
        return story
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error generating story with Gemini API."

# Route to render the form
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Route to generate the story
@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.get_json()
    trend_source = data['trendSource']
    genre = data['genre']
    tone = data['tone']
    time_period = data['timePeriod']
    duration = data['duration']
    include_hashtags = data['includeHashtags']

    # Prepare AI prompt
    prompt = f"Write a {duration}-second {genre} story in a {tone} tone, set in the {time_period}, based on {trend_source} trends."
    if include_hashtags:
        prompt += " Add some relevant hashtags at the end."

    # Generate story using Gemini API
    response = model.generate_content(prompt)
    story = response.text

    return jsonify({'story': story})


    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"script": "Error generating story", "trend": "N/A"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
