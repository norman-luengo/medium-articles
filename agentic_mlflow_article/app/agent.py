from schemas import QuestionRequest, AnswerResponse

class LocalModelAgent:
    """
    A simple Pydantic AI agent that receives a question
    and returns an answer using a local model.
    """

    def __init__(self):
        pass

    def get_response(self, question: QuestionRequest) -> AnswerResponse:
        answer = self._local_model_inference(question)
        return AnswerResponse(answer=answer)

    def _local_model_inference(self, question: str) -> str:

        return f"[LocalModel] Response to: {question}"
