from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"answer": "Please provide a question."})

    # ✅ Call your RAG backend API
    try:
        rag_response = requests.post(
            "https://sample-rag-rag-sample.apps.cluster-7lkbd.7lkbd.sandbox580.opentlc.com/chat",  # Your FastAPI RAG endpoint
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
