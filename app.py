from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores import ElasticsearchStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
import subprocess
import requests
import os

app = Flask(__name__)

### --- RAG Pipeline Setup ---

def clone_repo(repo_url, target_dir="repo"):
    if not os.path.exists(target_dir):
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    return os.path.join(target_dir, "document .docx")  # adjust if needed

repo_url = "https://github.com/Keerthana1695/sample-RAG.git"
doc_path = clone_repo(repo_url)

loader = UnstructuredLoader(doc_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=128,
    chunk_overlap=64
)
split_docs = text_splitter.split_documents(docs)

# Elasticsearch and Granite inference config
ES_HOST = "https://elasticsearch-sample-rag-sample.apps.cluster-7lkbd.7lkbd.sandbox580.opentlc.com"
ES_AUTH = ("elastic", "2DgOfW1G9w5h8yE41Pa72Q1c")
INFERENCE_SERVER_URL = "https://granite-31-2b-instruct-rag-sample.apps.cluster-7lkbd.7lkbd.sandbox580.opentlc.com/v1/completions"
MODEL_NAME = "granite-31-2b-instruct"

client = Elasticsearch([ES_HOST], basic_auth=ES_AUTH, verify_certs=False)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
vector_store = ElasticsearchStore(es_connection=client, index_name="rh_index", embedding=embeddings)

def query_granite(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.01,
        "top_p": 0.95,
        "presence_penalty": 1.03,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(INFERENCE_SERVER_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['choices'][0]['text']
    else:
        raise Exception(f"Inference failed: {response.status_code} - {response.text}")

def answer_query(query: str) -> str:
    results = vector_store.similarity_search(query)
    if not results:
        return "No relevant context found."

    context = results[0].page_content
    prompt = f"""Answer the question based on the context below.

Context:
{context}

Question:
{query}

Answer:"""

    return query_granite(prompt)

### --- Flask Routes ---

@app.route("/")
def home():
    return render_template("index.html")  # Optional: add index.html for form-based UI

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"response": "Please provide a question."}), 400

    try:
        answer = answer_query(question)
        return jsonify({"response": answer.strip()})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
