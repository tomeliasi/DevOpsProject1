from flask import Flask, jsonify, render_template
import google.generativeai as genai
import geminiService # type: ignore

app = Flask(__name__)

# Initialize counters
funny_count = 0
not_funny_count = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-joke')
def get_joke():
    response = geminiService.model.generate_content(geminiService.prompt)
    return jsonify({'joke': response.text})

@app.route('/update-counter/<counter_type>')
def update_counter(counter_type):
    global funny_count, not_funny_count
    if counter_type == 'funny':
        funny_count += 1
        return jsonify({'funny_count': funny_count})
    elif counter_type == 'not_funny':
        not_funny_count += 1
        return jsonify({'not_funny_count': not_funny_count})
    return jsonify({'error': 'Invalid counter type'})

if __name__ == '__main__':
    app.run(debug=True)