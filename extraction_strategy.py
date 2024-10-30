from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup

class ExtractionStrategy(ABC):
    @abstractmethod
    async def extract(self, content):
        """
        Extract relevant information from the given content according to the instruction.

        Args:
            content (str): The content to extract information from.

        Returns:
            dict: A dictionary containing the extracted information, or an empty object if no information is found.
        """

        pass

class LLMExtractionStrategy(ExtractionStrategy):
    def __init__(self, instruction, model_name="llama3.2"):
    """
    Initializes the LLMExtractionStrategy with the provided instruction
    and model name.

    Args:
        instruction (str): The instructions to be followed for extracting
            information from content.
        model_name (str, optional): The name of the LLM model to be used.
            Defaults to "llama2".
    """
        self.instruction = instruction
        self.model_name = model_name
        self.template = (
            "Extract information from the following content according to these instructions:\n"
            "Instructions: {instruction}\n\n"
            "Content: {content}\n\n"
            "Format the response as JSON with relevant fields. If no information is found, "
            "return an empty object {{}}."
        )
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.0
        )
        
    async def extract(self, content):
        """
        Extract relevant information from the given content according to the instruction.

        Args:
            content (str): The content to extract information from.

        Returns:
            dict: A dictionary containing the extracted information, or an empty object if no information is found.
        """
        cleaned_content = self._clean_content(content)
        max_length = 4000
        if len(cleaned_content) > max_length:
            cleaned_content = cleaned_content[:max_length]
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "instruction": self.instruction,
                "content": cleaned_content
            })
            return response
        except Exception as e:
            print(f"Error in LLM extraction: {str(e)}")
            return {}

    def _clean_content(self, content):
        """Clean HTML content before processing"""
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return text

class SimpleTextExtractionStrategy(ExtractionStrategy):
    async def extract(self, content):
        """Simple text extraction without LLM"""
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return {"text": text}
