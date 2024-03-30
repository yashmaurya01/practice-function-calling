from openai import OpenAI

class FunctionCall:
    def __init__(self, function_name, description, apiKey):
        self.function_name = function_name
        self.description = description
        self.apiKey = apiKey

    def create(self):
        client = OpenAI(
            apiKey=self.apiKey,
            model = "gpt3.5-turbo-1106",
            )
        
        function_template = [
            {
                "name": self.function_name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        
                    }
                }
            }
        ]
