from .openai_chat_api import OpenAIChatAPI
from .function_templates import function_template2
from .system_prompts import system_prompt2

class DialogueProcessor:
    @staticmethod
    def clean_dialogues(dialogue_text):
        """
        Cleans the input dialogue text by removing non-dialogue parts like timestamps and speaker labels,
        leaving only the dialogue content.
        
        Args:
        - dialogue_text (str): The raw dialogue text including timestamps, speaker labels, etc.
        
        Returns:
        - List[str]: A list of cleaned dialogues.
        """
        # Split the text into lines
        lines = dialogue_text.strip().split('\n')
        
        # Filter out lines that contain dialogues, and remove the speaker label
        cleaned_dialogues = [line for line in lines if line.startswith("Speaker")]

        return cleaned_dialogues


    @staticmethod
    def build_context_and_response(info, cleaned_dialogues, myopenai, context_length=4):
        """
        Builds a context for each of Speaker 0's dialogues from a list of cleaned dialogues.
        
        Args:
        - info (dict): A dictionary containing information about the conversation.
        - cleaned_dialogues (List[str]): A list of dialogues cleaned of timestamps and speaker labels.
        - context_length (int): The number of previous dialogues to include in the context.
        
        Returns:
        - List[dict]: A list of dictionaries, each containing 'previous context' and 'current dialogue'.
        """
        dialogue_pieces = []
        dialogue_history = []

        for dialogue in cleaned_dialogues:
            # Since the dialogues are already cleaned, we directly use them
            if "Speaker 0" in dialogue:
                context_dialogues = dialogue_history[-context_length:] if len(dialogue_history) >= context_length else dialogue_history[:]
                condensed_context = "\n".join(context_dialogues)
                
                dialogue_piece = {
                    "summary": myopenai.ask_openai("Give a one line summary of the conversation", condensed_context),
                    "previous context": condensed_context,
                    "current dialogue": dialogue
                }
                # print(dialogue_piece)

                current_user_dialog = "Summary: \n"+ dialogue_piece["summary"] + "\nPrevious conversation: \n" + dialogue_piece["previous context"] + "\nCurrent dialogue: \n" + dialogue_piece["current dialogue"]
                print(current_user_dialog)

                feedback = myopenai.ask_openai_functioncalling(system_prompt2(info), current_user_dialog, "give_feedback", function_template2(info))
                print("\nBetter Dialogue: " + feedback['feedback']['better_dialogue']+ "\nReasoning: " + feedback['feedback']['reasoning'])
                print("\n\n")


                dialogue_pieces.append(dialogue_piece)
                # if len(dialogue_pieces) == 3:
                #     break
            
            dialogue_history.append(dialogue)

        return dialogue_pieces
