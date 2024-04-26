import streamlit as st
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from joblib import load
import pandas as pd
from scipy.sparse import csr_matrix
import pickle

# Load the serialized DataFrame from 'chunk_df.pkl'
with open(r'C:\Users\pamar\Downloads\New folder (2)\chunk_df.pkl', 'rb') as file:
    chunk_df = pickle.load(file)
# Load TF-IDF vectorizer and matrix
tfidf_vectorizer = load('tfidf_vectorizer.joblib')
tfidf_matrix_sparse = load('tfidf_matrix.joblib')
tfidf_matrix = csr_matrix(tfidf_matrix_sparse)  

# Function to clean subtitle text
def clean_subtitle(subtitle_text):
    # Remove timestamps
    subtitle_text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\r\n', '', subtitle_text)
    
    # Remove non-printable characters and special characters
    cleaned_text = re.sub(r'[^\x20-\x7E]', '', subtitle_text)
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)

    # Remove HTML tags and URLs
    cleaned_text = re.sub(r'<[^>]+>', '', cleaned_text)
    cleaned_text = re.sub(r'http\S+', '', cleaned_text)

    # Remove line breaks and extra spaces
    cleaned_text = re.sub(r'\r?\n', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    # Convert text to lowercase
    cleaned_text = cleaned_text.lower()

    # Remove any remaining irrelevant content (words with 1 or 2 characters)
    cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)

    return cleaned_text.strip()

# Function to process the query
def process_query(query):
    # Preprocess the query
    cleaned_query = clean_subtitle(query)

    # Transform the cleaned query using the loaded TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([cleaned_query])

   
    query_sparse = csr_matrix(query_vector)

    # Calculate cosine similarity between the query vector and documents
    cosine_similarities = cosine_similarity(query_sparse, tfidf_matrix, dense_output=False).toarray().flatten()

    # Get the indices of the top 5 most similar documents
    top_indices = cosine_similarities.argsort()[-3:][::-1]

    top_documents = []
    for idx in top_indices:
        top_documents.append((chunk_df.iloc[idx], cosine_similarities[idx]))

# Initialize a list to store the required information
    result_info = []

# Extract the required information from the top_documents list
    for document, score in top_documents:
        result_info.append({
        'Cosine Similarity Score': score,
        'Name': document['name'],
        'Chunk': document['chunk_text'],
        'Chunk ID': document['chunk_index']
    })
    return result_info

# Load the Streamlit app
def main():
    st.title('Keywordsearchengine App-video_subtitle')

    # User input for search query
    query = st.text_input('Enter your query:')
    
    # Submit button to process the query
    if st.button('Submit'):
        if query:
            result_info = process_query(query)
            # Display the top 5 most similar documents and their cosine similarity scores
            st.subheader("Top 3 most similar documents:")
            for info in result_info:
                st.write("Name:", info['Name'])
                st.write("Cosine Similarity Score:", info['Cosine Similarity Score'])
                st.write("Chunk ID:", info['Chunk ID'])
                st.write("Chunk:", info['Chunk'])
                st.write("---")

if __name__ == '__main__':
    main()
