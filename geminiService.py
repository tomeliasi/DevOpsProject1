import google.generativeai as genai # type: ignore

Geminiapi = "AIzaSyCkwuMWjlfH3TQfAPk22TMvologsem1EK8"

# הגדרת המפתח
genai.configure(api_key=Geminiapi)

# יצירת מודל
model = genai.GenerativeModel('gemini-1.5-flash')

# הגדרת ה-Prompt
prompt = "שלח לי בדיחת קרש אחת."
