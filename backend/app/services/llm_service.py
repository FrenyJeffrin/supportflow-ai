from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from app.core.config import settings
from app.services.prompts import (
    RAG_INSTRUCTIONS,
    SYSTEM_PROMPT,
)

class LLMService:

    def __init__(self):
        self.llm= ChatOllama(
            model= settings.ollama_model,
            base_url= settings.ollama_base_url,
            temperature= 0.2,
        )

    async def generate_response(
            self,
            history: list[dict[str, str]],
            context: str | None = None,
    ) -> str:

        system_content = (SYSTEM_PROMPT)


        if context:
          system_content += ("\n\n" + RAG_INSTRUCTIONS.format(context=context))


        messages = [SystemMessage(content=system_content)]

        for item in history:
            if item['role'] == 'user':
                messages.append(
                    HumanMessage(content=item["content"])
                )
            elif item['role'] == 'assistant':
                messages.append(
                    AIMessage(content=item['content'])
                )

        response = await self.llm.ainvoke(messages)
        return str(response.content)