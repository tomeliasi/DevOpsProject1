
import google.generativeai as genai
import geminiService # type: ignore
# import fathersJokesArray from fathersJokes

def littleJokefromAI():
	response = geminiService.model.generate_content(geminiService.prompt)
	# הדפס את התגובה
	print(response.text)

littleJokefromAI()