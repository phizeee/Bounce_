import openai
import pandas as pd
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Load dataset and convert to text
# data = pd.read_excel('Dataset 1 (Sustainability Research Results).xlsx')
# data_texts = data.apply(lambda row: row.to_string(), axis=1).tolist()
#
#
# # Generate embeddings for each row and save to a list
# data_embeddings = []
# for text in data_texts:
#     embedding = openai.Embedding.create(input=text, engine="text-embedding-ada-002")['data'][0]['embedding']
#     data_embeddings.append(embedding)
#
# # Save embeddings to a JSON file
# with open('data_embeddings.json', 'w') as f:
#     json.dump(data_embeddings, f)
#
# print("Embeddings generated and saved to 'data_embeddings.json'")

# Load dataset and convert to text
data = pd.read_excel('Dataset 2 (Christmas Research Results).xlsx')
data_texts = data.apply(lambda row: row.to_string(), axis=1).tolist()


# Generate embeddings for each row and save to a list
data_embeddings = []
for text in data_texts:
    embedding = openai.Embedding.create(input=text, engine="text-embedding-ada-002")['data'][0]['embedding']
    data_embeddings.append(embedding)

# Save embeddings to a JSON file
with open('data_embeddings2.json', 'w') as f:
    json.dump(data_embeddings, f)

print("Embeddings generated and saved to 'data_embeddings.json'")