from semantic_search import SemanticSearch
from llm import LLMService

class RAGEngine:
    def __init__(self):
        self.search_engine = SemanticSearch()
        self.llm = LLMService()
        
    def ask(self, question):
        results = self.search_engine.search(question, k=3)
        context = ""
        for _, text in results:
            context += text + "\n\n"
        prompt = f"""
Use ONLY the information provided below.

Context:
{context}

Question:
{question}

If the answer is not found in the context,
reply:
"I don't know."

Answer:
"""
        return self.llm.ask(prompt)