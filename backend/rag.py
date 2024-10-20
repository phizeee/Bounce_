import openai
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def load_embeddings(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Load sustainability and Christmas datasets and their embeddings
data_sustainability = pd.read_excel('Dataset 1 (Sustainability Research Results).xlsx')
data_christmas = pd.read_excel('Dataset 2 (Christmas Research Results).xlsx')
data_embeddings_sustainability = load_embeddings('data_embeddings.json')
data_embeddings_christmas = load_embeddings('data_embeddings2.json')

# Helper function to find the most relevant entries
def find_relevant_texts(query, data, embeddings):
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-5:][::-1]  # Top 5 relevant entries
    return data.iloc[top_indices].apply(lambda row: row.to_string(), axis=1).tolist()

# Endpoint-specific functions
def analyze_data(query):
    sustainability_texts = find_relevant_texts(query, data_sustainability, data_embeddings_sustainability)
    christmas_texts = find_relevant_texts(query, data_christmas, data_embeddings_christmas)
    combined_text = "\n\n".join(sustainability_texts + christmas_texts)
    return generate_response(query, combined_text)

def compare_data(query):
    sustainability_texts = find_relevant_texts(query, data_sustainability, data_embeddings_sustainability)
    christmas_texts = find_relevant_texts(query, data_christmas, data_embeddings_christmas)
    comparison_text = "Comparison of findings:\n\n" + "\n\n".join(sustainability_texts + christmas_texts)
    return generate_response(query, comparison_text)

def get_sustainability_insights(query):
    insights = find_relevant_texts(query, data_sustainability, data_embeddings_sustainability)
    return generate_response(query, "\n\n".join(insights))

def get_christmas_insights(query):
    insights = find_relevant_texts(query, data_christmas, data_embeddings_christmas)
    return generate_response(query, "\n\n".join(insights))

def generate_response(query, context):
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=f"Based on the question: '{query}', here's the analysis:\n{context}\n\nAnswer:",
    #     max_tokens=150
    # )
    # Generate response using GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze survey data."},
            {"role": "user",
             "content": f"Based on the question: '{query}', here's the analysis:\n{context}\n\nAnswer:"}
        ],
        max_tokens=150
    )
    # Print the response
    print("\nResponse:", response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']



def find_relevant_texts(query, data, embeddings, top_n=5):
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    return data.iloc[top_indices].apply(lambda row: row.to_string(), axis=1).tolist()

def generate_response(query, context):
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=f"Question: '{query}'\nContext: {context}\nAnswer:",
    #     max_tokens=150
    # )
    # return response['choices'][0]['text'].strip()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze survey data."},
            {"role": "user",
             "content": f"Based on the question: '{query}', here's the analysis:\n{context}\n\nAnswer:"}
        ],
        max_tokens=150
    )
    # Print the response
    print("\nResponse:", response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']

# Additional endpoint-specific functions
def get_dataset_stats():
    column_names = data_sustainability.columns.tolist()
    # column_names = [i for i in column_names if "Unnamed:" not in i or len(i) > 4]
    tags = []
    for i in column_names:
        if i == "Age":
            tags.append(i)
        elif "Unnamed:" not in i and len(i) > 4:
            tags.append(i)
    # tags = [i for i in column_names if "Unnamed:" not in i and len(i) > 4]
    first_row_list = data_sustainability.iloc[0].tolist()
    first_r = [r for r in first_row_list if not pd.isna(r)]
    del tags[0]
    del first_r[0]
    result = {}
    current_tag = tags.pop(0)
    current_values = []

    for value in first_r:
        if value == ' ' and len(tags) > 0:
            if current_tag is not None:
                result[current_tag] = current_values
            current_tag = tags.pop(0)
            current_values = []
        else:
            current_values.append(value)

    if current_tag is not None:
        result[current_tag] = current_values

    column_names2 = data_christmas.columns.tolist()
    # column_names2 = [i for i in column_names2 if "Unnamed:" not in i]
    tags = []
    for i in column_names2:
        if i == "Age":
            tags.append(i)
        elif "Unnamed:" not in i and len(i) > 4:
            tags.append(i)
    # tags = [i for i in column_names2 if "Unnamed:" not in i and len(i) > 4  and "Age" in i]
    first_row_list = data_christmas.iloc[0].tolist()
    first_r = [r for r in first_row_list if not pd.isna(r)]
    del tags[0]
    del first_r[0]
    result2 = {}
    current_tag = tags.pop(0)
    current_values = []

    for value in first_r:
        if value == ' ' and len(tags) > 0:
            if current_tag is not None:
                result2[current_tag] = current_values
            current_tag = tags.pop(0)
            current_values = []
        else:
            current_values.append(value)

    if current_tag is not None:
        result2[current_tag] = current_values

    return {
        "sustainability": {
            "entries": len(column_names),
            "columns": result #list(data_sustainability.columns)
        },
        "christmas": {
            "entries": len(column_names2),
            "columns": result2 #list(data_christmas.columns)
        }
    }

def retrieve_entries(query, dataset="sustainability", top_n=5):
    data = data_sustainability if dataset == "sustainability" else data_christmas
    embeddings = data_embeddings_sustainability if dataset == "sustainability" else data_embeddings_christmas
    top_texts = find_relevant_texts(query, data, embeddings, top_n)
    return top_texts

def compare_demographics(query):
    sust_texts = find_relevant_texts(query, data_sustainability, data_embeddings_sustainability)
    xmas_texts = find_relevant_texts(query, data_christmas, data_embeddings_christmas)
    return generate_response(query, f"Sustainability Data:\n{sust_texts}\n\nChristmas Data:\n{xmas_texts}")

def related_topics():
    return ["Sustainable Shopping", "Eco-Friendly Gifts", "Consumer Spending", "Holiday Activities", "Budgeting & Financial Planning"]

def custom_query(query, dataset="sustainability"):
    data = data_sustainability if dataset == "sustainability" else data_christmas
    embeddings = data_embeddings_sustainability if dataset == "sustainability" else data_embeddings_christmas
    relevant_texts = find_relevant_texts(query, data, embeddings)
    return generate_response(query, "\n\n".join(relevant_texts))

def sentiment_analysis(query, dataset="sustainability"):
    data = data_sustainability if dataset == "sustainability" else data_christmas
    embeddings = data_embeddings_sustainability if dataset == "sustainability" else data_embeddings_christmas
    texts = find_relevant_texts(query, data, embeddings)
    sentiment_context = "\n\n".join(texts)
    # sentiment_response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=f"Analyze the sentiment of the following context: {sentiment_context}",
    #     max_tokens=50
    # )
    sentiment_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze survey data."},
            {"role": "user",
             "content": f"Analyze the sentiment of the following context: {sentiment_context}"}
        ],
        max_tokens=1000
    )

    # Print the response
    print("\nResponse:", sentiment_response['choices'][0]['message']['content'])
    return sentiment_response['choices'][0]['message']['content']
