from fastapi import FastAPI, HTTPException
from schemas import QuestionRequest, AnswerResponse
from agent import LocalModelAgent

app = FastAPI()


@app.post("/chat", response_model=AnswerResponse)
async def chat_agent(payload: QuestionRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    agent = LocalModelAgent()
    answer = agent.get_response(question)
    return AnswerResponse(answer=answer)
