from elasticsearch import Elasticsearch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import ElasticsearchStore
import requests

ES_HOST = "https://elasticsearch-sample-rag-sample.apps.cluster-7lkbd.7lkbd.sandbox580.opentlc.com"
ES_AUTH = ("elastic", "2DgOfW1G9w5h8yE41Pa72Q1c")
INFERENCE_SERVER_URL = "https://granite-31-2b-instruct-rag-sample.apps.cluster-7lkbd.7lkbd.sandbox580.opentlc.comm/v1/completions"
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
