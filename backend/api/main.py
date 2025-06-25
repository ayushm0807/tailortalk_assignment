from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import run_agent

app = FastAPI()

class UserInput(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
def chat(input: UserInput):
    result = run_agent(input.message, input.session_id)
    return {"response": result}
