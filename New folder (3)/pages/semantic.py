import streamlit as st
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import chromadb

# Initialize Streamlit app
st.title('Semantic Search Engine App-video_subtitle')

# Load SentenceTransformer model
model = SentenceTransformer("distilbert-base-nli-mean-tokens")

# Connect to ChromaDB client and collection
client = chromadb.PersistentClient(path=r"C:\Users\pamar\Downloads\New folder (2)\embedd_db")
collection = client.get_collection("searchengines")

def clean_text(text):
    """Preprocess the input text for search."""
    # Remove non-alphanumeric characters and convert to lowercase
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    
    # Tokenize the text
    tokens = word_tokenize(clean_text)
    
    # Remove stopwords and lemmatize tokens
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words]
    
    # Join the filtered tokens back into a string
    clean_text = ' '.join(clean_tokens)
    
    return clean_text.strip()

def search_documents(query):
    """Perform a semantic search query and return relevant documents."""
    # Preprocess the query
    cleaned_query = clean_text(query)
    
    # Encode the cleaned query to get semantic embeddings
    query_embedding = model.encode([cleaned_query])

    # Perform a query on the ChromaDB collection using the embeddings
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5,
        include=['documents', 'metadatas']
    )
    documents = results['documents']
    
   

    return  documents

# Load the Streamlit app for semantic search
def main_semantic_search():
    

    # User input: search query
    query = st.text_input('Enter your search query:')

    # Trigger search on button click
    if st.button('Search') and query:
        # Perform search and get relevant documents, metadatas, and similarities
        relevant_documents= search_documents(query)

        # Display search results
        if  relevant_documents:
            st.subheader(f'Top 5 most relevant documents for "{query}"')
            for idx, document in enumerate(relevant_documents):  # Use enumerate to get both index and document
                st.write(f'Document {idx + 1}:')
                st.write(document)
                

if __name__ == '__main__':
    main_semantic_search()
