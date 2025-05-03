from flask import Flask, request, jsonify, render_template_string
import redis
import google.generativeai as genai

app = Flask(__name__)

# Redis connection (if running with Docker, the service name is redis)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Configure API key for Gemini API
genai.configure(api_key="AIzaSyCkwuMWjlfH3TQfAPk22TMvologsem1EK8")
model = genai.GenerativeModel('gemini-1.5-flash')

# Simple HTML template
HTML_TEMPLATE = """
<html>
  <body>
    <h1>🤪 Joke of the day 🤪</h1>
    <p>{{ joke }}</p>
    <p><strong>Likes: {{ likes }}</strong></p>
    <p><strong>Dislikes: {{ dislikes }}</strong></p>
    <form action="/rate" method="post">
      <input type="hidden" name="joke" value="{{ joke }}">
      <button name="rating" value="like">Like</button>
      <button name="rating" value="dislike">Dislike</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def get_joke():
    # Get a joke from Gemini API
    response = model.generate_content("Send me a random dad joke.")
    joke = response.text.strip()

    # Retrieve likes and dislikes from Redis (default to 0 if not found)
    likes = r.hget(f"joke:{joke}", "likes") or 0
    dislikes = r.hget(f"joke:{joke}", "dislikes") or 0

    # Return the joke page with likes and dislikes displayed
    return render_template_string(HTML_TEMPLATE, joke=joke, likes=likes, dislikes=dislikes)

@app.route('/rate', methods=['POST'])
def rate_joke():
    joke = request.form.get('joke')
    rating = request.form.get('rating')
    key = f"joke:{joke}"

    # Save the rating to Redis
    if rating == "like":
        r.hset(key, "likes", int(r.hget(key, "likes") or 0) + 1)
    elif rating == "dislike":
        r.hset(key, "dislikes", int(r.hget(key, "dislikes") or 0) + 1)

    # After rating, redirect back to the home page with a new joke
    return f"Thank you for your feedback! <a href='/'>Get a new joke</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

