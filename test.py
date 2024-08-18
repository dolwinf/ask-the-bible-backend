from fastapi import FastAPI, Request, Response, Depends
from uuid import uuid4

app = FastAPI()

# A simple in-memory store for session data (for production, use a database)
session_store = {}

def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
    return session_id

@app.middleware("http")
async def add_session_id_to_cookies(request: Request, call_next):
    response = await call_next(request)
    session_id = get_session_id(request)
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.get("/ask")
async def ask_question(request: Request, question: str):
    session_id = get_session_id(request)
    
    # Initialize history if it doesn't exist
    if session_id not in session_store:
        session_store[session_id] = []

    # Get the history for this session
    history = session_store[session_id]

    # Process the question (this is where you'd integrate with your system)
    # For this example, we'll just echo the question back as the "answer"
    answer = f"Answer to: {question}"
    
    # Store the question and answer in the session history
    history.append({"question": question, "answer": answer})
    
    # Return the answer (and optionally the history)
    return {"answer": answer, "history": history}
