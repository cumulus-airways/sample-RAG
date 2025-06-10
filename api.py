from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import answer_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_endpoint(query: QueryRequest):
    try:
        response = answer_query(query.question)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
