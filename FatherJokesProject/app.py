import json
import random
from flask import Flask, request, jsonify, render_template_string
import redis

app = Flask(__name__)

# Redis connection (if running with Docker, the service name is redis)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Load jokes from the JSON file
with open('jokes.json', 'r') as f:
    jokes = json.load(f)

# Track previously shown jokes in Redis
if not r.exists('shown_jokes'):
    r.set('shown_jokes', json.dumps([]))

# HTML template
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

@app.route('/')
def get_joke():
    # Load previously shown jokes from Redis
    shown_jokes = json.loads(r.get('shown_jokes'))

    # Get a random joke that has not been shown yet
    remaining_jokes = [joke for joke in jokes if joke not in shown_jokes]
    
    if not remaining_jokes:
        # Reset the shown jokes if all jokes have been shown
        shown_jokes = []
        remaining_jokes = jokes

    joke = random.choice(remaining_jokes)
    shown_jokes.append(joke)
    
    # Update shown jokes in Redis
    r.set('shown_jokes', json.dumps(shown_jokes))

    total_likes = r.get("total_likes") or 0
    total_dislikes = r.get("total_dislikes") or 0

    return render_template_string(
        HTML_TEMPLATE,
        joke=joke,
        total_likes=total_likes,
        total_dislikes=total_dislikes
    )

@app.route('/rate', methods=['POST'])
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

    # Thank you page styled
    return render_template_string("""
    <html>
      <head>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
          }
          .message-box {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
          }
          h2 {
            color: #007BFF;
            margin-bottom: 20px;
          }
          a {
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
          }
          a:hover {
            background-color: #0056b3;
          }
        </style>
      </head>
      <body>
        <div class="message-box">
          <h2>Thank you for your feedback!</h2>
          <a href="/">Get a new joke</a>
        </div>
      </body>
    </html>
    """)
