import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences

# Load the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the text
input_ids = []
attention_masks = []
sentences = ["I love this movie!", "This film is terrible."]

for sentence in sentences:
   encoded_dict = tokenizer.encode_plus(
       sentence,                    
       add_special_tokens = True, # Add '[CLS]' and '[SEP]'
       max_length = 64,            
       pad_to_max_length = True,
       return_attention_mask = True, 
       return_tensors = 'pt',    
   )
   
   input_ids.append(encoded_dict['input_ids'])
   attention_masks.append(encoded_dict['attention_mask'])

input_ids = pad_sequences(input_ids, dtype="long", padding='post', truncating='post')
attention_masks = pad_sequences(attention_masks, dtype="long", padding='post', truncating='post')

# Convert lists into tensors
input_ids = torch.tensor(input_ids)
attention_masks = torch.tensor(attention_masks)

# Create a DataLoader
data = TensorDataset(input_ids, attention_masks)
sampler = RandomSampler(data)
dataloader = DataLoader(data, sampler=sampler, batch_size=32)

# Load the BERT model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

# Start training
for epoch in range(num_epochs):
   total_loss = 0
   model.train()
   for step, batch in enumerate(dataloader):
       b_input_ids = batch[0].to(device)
       b_input_mask = batch[1].to(device)
       model.zero_grad()
       outputs = model(b_input_ids, 
                      token_type_ids=None, 
                      attention_mask=b_input_mask, 
                      labels=None)
       loss = outputs[0]
       total_loss += loss.item()
       loss.backward()
       torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
       optimizer.step()
   avg_train_loss = total_loss / len(dataloader)
   print("Average training loss: {0:.2f}".format(avg_train_loss))


from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForSequenceClassification.from_pretrained("EleutherAI/gpt-j-6B")

inputs = tokenizer("Hello, my name is John.", return_tensors='pt')
outputs = model(**inputs)

# Get the predicted class
predicted_class = torch.argmax(outputs.logits, dim=-1).item()

print(predicted_class)
