import ollama

class LLMService:
    def ask(self, prompt):
        response = ollama.chat(
            model = 'phi3:mini',
            messages = [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        return response['message']['content']  



