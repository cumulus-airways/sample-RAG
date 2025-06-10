from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your Granite model inference URL and params
INFERENCE_SERVER_URL = "https://granite-31-2b-instruct-my-sample-project.apps.cluster-nc45c.nc45c.sandbox1007.opentlc.com/v1/completions"
MODEL_NAME = "granite-31-2b-instruct"

def query_granite(prompt):
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
        return f"Error: {response.status_code}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"answer": "Please provide a question."})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"answer": "Please provide a question."})

    # ✅ Call your RAG backend API
    try:
        rag_response = requests.post(
            "http://localhost:8000/chat",  # Your FastAPI RAG endpoint
            json={"question": question},
            headers={"Content-Type": "application/json"}
        )
        if rag_response.status_code == 200:
            answer = rag_response.json().get("response", "No answer returned.")
        else:
            answer = f"Error from RAG API: {rag_response.status_code}"
    except Exception as e:
        answer = f"Request failed: {e}"

    return jsonify({"answer": answer.strip()})

    # For demo, just send question as prompt
    prompt = f"Answer the question:\n{question}\nAnswer:"
    answer = query_granite(prompt)
    return jsonify({"answer": answer.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
