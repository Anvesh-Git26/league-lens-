from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import app_graph
from app.commentary import LiveCommentaryEngine

app = FastAPI(title="LeagueLens API")
commentary_engine = LiveCommentaryEngine()

class QueryRequest(BaseModel):
    question: str

class CommentaryRequest(BaseModel):
    batter: str
    bowler: str
    outcome: str

@app.get("/")
def read_root():
    return {"message": "LeagueLens AI Sports Chatbot is Live 🏏"}

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    """
    Main endpoint for the Self-RAG Chatbot.
    """
    inputs = {"question": request.question}
    result = app_graph.invoke(inputs)
    return {
        "response": result.get("generation"),
        "steps": "Retrieve -> Grade -> Generate" 
    }

@app.post("/live-commentary")
async def commentary_endpoint(request: CommentaryRequest):
    """
    Generates audio commentary for live match events.
    """
    text_commentary = commentary_engine.generate_commentary(request.dict())
    audio_file = commentary_engine.text_to_speech(text_commentary)
    return {"text": text_commentary, "audio_url": audio_file}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)