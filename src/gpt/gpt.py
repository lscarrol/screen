import os
import openai

def call_gpt3(request):
   openai.api_key = os.getenv('OPENAI_API_KEY')

   response = openai.Completion.create(
     engine="text-davinci-002",
     prompt="What do you think this is?",
     max_tokens=60
   )

   return response.choices[0].text.strip()