from .dialogue_processor import DialogueProcessor
from .function_templates import function_template1, function_template2
from .openai_chat_api import OpenAIChatAPI
from .system_prompts import system_prompt1, system_prompt2
from .utils import load_api_key

class LanguageFeedback:
    def __init__(self, api_key_file_path, conversation):
        self.api_key = load_api_key(api_key_file_path)
        self.dialogue_processor = DialogueProcessor()
        self.openai = OpenAIChatAPI(self.api_key)
        self.conversation = conversation

    def get_feedback(self):
        cleaned_dialogues = self.dialogue_processor.clean_dialogues(self.conversation)
        info = self.openai.ask_openai_functioncalling(system_prompt1, "\n".join(cleaned_dialogues), "get_tone", function_template1)
        feedback = self.dialogue_processor.build_context_and_response(info, cleaned_dialogues, self.openai)
        
        return feedback
