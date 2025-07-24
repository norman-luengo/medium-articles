from fastapi import FastAPI, HTTPException
from schemas import QuestionRequest, AnswerResponse
from agent import LocalModelAgent
from pydantic_ai import Agent

app = FastAPI()


@app.post("/chat", response_model=AnswerResponse)
async def chat_agent(payload: QuestionRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    agent = Agent(
            'google-gemini:gemini-1.5-flash',
            system_prompt='You are a helpful assistant. Answer concisely.'
        )
    result = await agent.run(question)
    return AnswerResponse(answer=result.output)
