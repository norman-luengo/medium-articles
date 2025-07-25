
from fastapi import FastAPI, HTTPException
from app.schemas import QuestionRequest, AnswerResponse
from pydantic_ai import Agent
import mlflow
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

app = FastAPI()


@app.post("/chat", response_model=AnswerResponse)
async def chat_agent(payload: QuestionRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    ollama_model = OpenAIModel(
    model_name='deepseek-r1:32b', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)
    system_prompt = 'You are a helpful assistant. Answer concisely.'
    agent = Agent(
        ollama_model,
        system_prompt=system_prompt
    )

    with mlflow.start_run(run_name="chat_agent_interaction"):
        mlflow.log_param("agent_model", ollama_model)
        mlflow.log_param("system_prompt", system_prompt)
        mlflow.log_param("question", question)
        result = await agent.run(question)
        mlflow.log_param("answer", result.output)
        return AnswerResponse(answer=result.output)
