from transformers import pipeline

def generate_text(prompt):
   generator = pipeline('text-generation', model='gpt2')
   return generator(prompt, max_length=100, num_return_sequences=1)

text = "The text extracted from the image"
print(generate_text(text))