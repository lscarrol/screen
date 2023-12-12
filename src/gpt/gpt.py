import openai
openai.api_key = ''

def classify_text(text):
   prompt = f"Given this text, what do you think this is? {text}"
   response = openai.Completion.create(
       engine="davinci-instruct-beta-v3",
       prompt=prompt,
       temperature=.7,
       max_tokens=500,
       top_p=1,
       frequency_penalty=0,
       presence_penalty=0,
       stop=["\n"]
   )
   classification = response['choices'][0]['text']
   return classification