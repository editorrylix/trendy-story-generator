from flask import Flask, render_template, request, jsonify
from pytrends.request import TrendReq
import praw

app = Flask(__name__, template_folder="templates")

# Function to fetch Google Trends
def fetch_google_trends():
  try:
    pytrends = TrendReq(hl='en-US', tz=360)
    trending = pytrends.trending_searches(pn='united_states')
    return trending[0][0] if not trending.empty else "No trends found"
  except pytrends.exceptions.RequestError as e:
    print(f"Error fetching Google Trends: {e} (Likely API Key issue)")
    return "Error fetching Google Trends"
  except Exception as e:
    print(f"Unexpected Error fetching Google Trends: {e}")
    return "Error fetching Google Trends"

# Function to fetch Reddit Trends
def fetch_reddit_trends():
    try:
        reddit = praw.Reddit(
            client_id="YOUR_REDDIT_CLIENT_ID",
            client_secret="YOUR_REDDIT_CLIENT_SECRET",
            user_agent="your_app_name"
        )
        hot_posts = reddit.subreddit("all").hot(limit=5)
        trends = [post.title for post in hot_posts]
        return trends[0] if trends else "No Reddit trends found"
    except Exception as e:
        print(f"Error fetching Reddit Trends: {e}")
        return "Error fetching Reddit Trends"

# Route to render the UI
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Route to generate the story
@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        trend_source = data['trendSource']
        custom_keyword = data.get('customKeyword', '')
        genre = data['genre']
        tone = data['tone']
        time_period = data['timePeriod']
        duration = data['duration']
        include_hashtags = data['includeHashtags']

        # Fetch the trend
        if trend_source == "google_trends":
            trend = fetch_google_trends()
        elif trend_source == "reddit_api":
            trend = fetch_reddit_trends()
        elif trend_source == "custom_input":
            trend = custom_keyword if custom_keyword else "Custom trend not provided"
        else:
            trend = "Unknown source"

        # Prepare story prompt
        prompt = (
            f"Write a {duration}-second {genre} story in a {tone} tone, "
            f"set in the {time_period}, based on the trend: {trend}."
        )
        if include_hashtags:
            prompt += " Add relevant hashtags at the end."

        # Dummy response (replace this with Gemini API call if needed)
        story = f"Generated story based on trend: {trend}."

        return jsonify({'story': story})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"story": "Error generating story", "trend": "N/A"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
