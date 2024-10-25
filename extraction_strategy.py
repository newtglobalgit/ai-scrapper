from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class ExtractionStrategy(ABC):
    @abstractmethod
    async def extract(self, content):
        pass

class LLMExtractionStrategy(ExtractionStrategy):
    def __init__(self, instruction, model_name="llama3.1"):
        self.instruction = instruction
        self.model_name = model_name
        self.template = (
            "You are tasked with extracting specific information from the following content. "
            "Instruction: {instruction}\n\n"
            "Content: {content}\n\n"
            "Return the extracted information in JSON format. If no relevant information is found, "
            "return an empty array []."
        )
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.0,
            top_k=10,
            top_p=0.95
        )
        
    async def extract(self, content):
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.llm
        response = chain.invoke({
            "instruction": self.instruction,
            "content": content
        })
        return response
