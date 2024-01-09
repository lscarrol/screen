import json
from google.cloud import pubsub_v1
from gensim import corpora
from gensim.models import LdaModel

# List to store the texts
texts = []

def callback(message):
   global texts
   msg_dict = json.loads(message.data)
   text = msg_dict['text']
   texts.append(text)
   print("Received message: {}".format(text))
   message.ack()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('', 'screen-topic')

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for messages on {}..\n".format(subscription_path))

try:
   # Block until the future completes.
   streaming_pull_future.result()
except Exception as e:
   streaming_pull_future.cancel()
   raise e

# Create a dictionary from the texts
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text.split()) for text in texts]

# Train an LDA model on this dictionary
lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

def classify_text(text):
   bow = dictionary.doc2bow(text.split())
   topic_distribution = lda_model.get_document_topics(bow)
   return max(topic_distribution, key=lambda x: x[1])[0]

# Classify the last received text
if texts:
   topic = classify_text(texts[-1])
   print("The topic of the last received text is: {}".format(topic))
else:
   print("No text received yet.")
