from flask import Flask, request, jsonify, render_template_string
import redis
import google.generativeai as genai

# הגדרת Flask
app = Flask(__name__)

# חיבור ל-Redis (אם את מריצה בדוקר, ודאי ששם השירות הוא redis)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# הגדרת מפתח API
genai.configure(api_key="AIzaSyCkwuMWjlfH3TQfAPk22TMvologsem1EK8")
model = genai.GenerativeModel('gemini-1.5-flash')

# תבנית HTML פשוטה
HTML_TEMPLATE = """
<html>
  <body>
    <h1>🤪 בדיחת קרש 🤪</h1>
    <p>{{ joke }}</p>
    <form action="/rate" method="post">
      <input type="hidden" name="joke" value="{{ joke }}">
      <button name="rating" value="like">אהבתי</button>
      <button name="rating" value="dislike">לא אהבתי</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def get_joke():
    response = model.generate_content("שלח לי בדיחת קרש אחת.")
    joke = response.text.strip()
    return render_template_string(HTML_TEMPLATE, joke=joke)

@app.route('/rate', methods=['POST'])
def rate_joke():
    joke = request.form.get('joke')
    rating = request.form.get('rating')
    key = f"joke:{joke}"

    # שמירה ב-Redis
    if rating == "like":
        r.hincrby(key, "likes", 1)
    elif rating == "dislike":
        r.hincrby(key, "dislikes", 1)

    return f"תודה על המשוב! <a href='/'>בדיחה חדשה</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
