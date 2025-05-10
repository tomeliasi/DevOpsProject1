from flask import Flask, request, jsonify, render_template_string
import redis
import google.generativeai as genai
import random
from google.generativeai.types import GenerationConfig

app = Flask(__name__)

# Redis connection (if running with Docker, the service name is redis)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Configure API key for Gemini API
genai.configure(api_key="AIzaSyAx83Q5ZdKwnOlosMPuAiJUcWT04UBQbJU")
model = genai.GenerativeModel('gemini-1.5-flash')

# Update the HTML template to remove private likes and dislikes for each joke
HTML_TEMPLATE = """
<html>
  <head>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        color: #333;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
      }
      .container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        width: 100%;
      }
      h1 {
        font-size: 24px;
        color: #007BFF;
      }
      p {
        font-size: 18px;
        line-height: 1.6;
      }
      .button-group {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
      }
      button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s;
      }
      button:hover {
        background-color: #007BFF;
        color: white;
      }
      .total {
        margin-top: 20px;
        font-size: 18px;
        color: #555;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Joke of the Day</h1>
      <p>{{ joke }}</p>
      <div class="button-group">
        <form action="/rate" method="post">
          <input type="hidden" name="joke" value="{{ joke }}">
          <button name="rating" value="like">Like</button>
          <button name="rating" value="dislike">Dislike</button>
        </form>
      </div>
      <div class="total">
        <p><strong>Total Likes:</strong> {{ total_likes }}</p>
        <p><strong>Total Dislikes:</strong> {{ total_dislikes }}</p>
      </div>
    </div>
  </body>
</html>
"""

# Update the get_joke function so that it only displays the total_likes and total_dislikes
@app.route('/')
def get_joke():
    # Add randomness to the prompt
    prompt = f"Tell me a random dad joke #{random.randint(1, 99999)}"
    
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=1.0  # higher randomness
        )
    )
    joke = response.text.strip()

    total_likes = r.get("total_likes") or 0
    total_dislikes = r.get("total_dislikes") or 0

    return render_template_string(
        HTML_TEMPLATE,
        joke=joke,
        total_likes=total_likes,
        total_dislikes=total_dislikes
    )

@app.route('/rate', methods=['POST'])
def rate_joke():
    joke = request.form.get('joke')
    rating = request.form.get('rating')
    key = f"joke:{joke}"

    # Save the rating to Redis and update global like/dislike counters
    if rating == "like":
        r.hset(key, "likes", int(r.hget(key, "likes") or 0) + 1)
        r.incr("total_likes")
    elif rating == "dislike":
        r.hset(key, "dislikes", int(r.hget(key, "dislikes") or 0) + 1)
        r.incr("total_dislikes")

    # After rating, redirect back to the home page with a new joke
    return f"Thank you for your feedback! <a href='/'>Get a new joke</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

