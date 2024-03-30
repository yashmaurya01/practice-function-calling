from openai import OpenAI
import json
import time

class OpenAIChatAPI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def ask_openai_functioncalling(self,system_prompt, user_dialog, function_call_name, function_template, timeout=1):
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_dialog},
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0.1,
            max_tokens=512,
            functions=function_template,
            function_call={"name": function_call_name},
        )
        answer = response.choices[0].message.function_call.arguments
        generated_response = json.loads(answer)
        time.sleep(timeout)
        
        return generated_response

    def ask_openai(self, system_prompt, user_dialog, timeout=1):
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_dialog},
        ]
            
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0.1,
            max_tokens=512,
        )
        answer = response.choices[0].message.content
        time.sleep(timeout)
        return answer
