
function_template1 = [
    {
        "name": "get_tone",
        "description": "You are an AI assistant who is analyzing the tone of a conversation between two people. The conversation is between two people, Speaker 0 and Speaker 1. You are to understand whether this conversation is informal, formal or neutral. You are also required to list the main theme of the discussion.",
        "parameters": {
            "type": "object",
            "properties": {
                "conversation_info": {
					"type": "object",
					"properties": {
                        "tone": {
                            "type": "string",
                            "description": "Return the tone of the conversation. It can be informal, formal or neutral if it isn't either of formal or casual. For example, Informal conversation would be like friends talking casually with each other. Formal conversation would be like a boss talking to an employee. Neutral would be a mix of both.",
                            "enum": ["informal", "formal", "neutral"]
                            },
                        "theme": {
                            "type": "object",
                            "properties": {
                                    "main_theme": {
                                        "type": "string",
                                        "description": "Return the main theme of the conversation. It can be a general topic of the conversation. For example, if the conversation is about a new movie, the main theme would be 'Movies'."
                                    },
                                    "sub_themes": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "description": "Return the sub-themes of the conversation. It can be a specific topic of the conversation. For example, if the conversation is about a new movie, the sub-themes would be 'Action', 'Comedy', 'Romance'."
                                        }
                                    }
                                },
                            "required": ["main_theme", "sub_themes"]
                            },
                    },
                    "required": ["tone", "theme"],
                },
            },
			"required": ["conversation_info"],
        }
    }
]

def function_template2(info):
    # Your dynamic template generation logic here
    function_template2 = [
        {
            "name": "give_feedback",
            "description": f"You are a language teacher who helps non-native English speakers help get better in daily life conversations. You are to analyze the conversation between two people, Speaker 0 and Speaker 1. The main user is Speaker 0. This is a {info['conversation_info']['tone']} conversation. Informal conversation would be like between friends where slangs might even be used. Formal conversation would be like where a boss is talking to an employee but since it's a verbal conversation, punctuations would not be very reliable. Try to keep the conversation natural flowing. Neutral would be a mix of both. {info['conversation_info']['theme']['main_theme']} is the main theme of the conversation. The sub-themes are {info['conversation_info']['theme']['sub_themes']} of the conversation. Give constructive feedback to Speaker 0 on their 'Current dialog' and how they could they have better said it. Don't be very strict.",
            "parameters": {
                "type": "object",
                "properties": {
                    "feedback": {
                        "type": "object",
                        "properties": {
                            "better_dialogue": {
                                "type": "string",
                                "description": f"If the current dialogue is already perfect, return 'None'. Keep it concise and be lenient. Considering that the conversation is {info['conversation_info']['tone']}, return the better dialogue that Speaker 0 could have said while conveying the same idea as current dialogue. Keep the response natural. ",
                                },
                            "reasoning": {
                                "type": "string",
                                "description": "If the current dialogue is already perfect, return 'The dialogue is perfect'. Else, return a concise reasoning behind why your suggestion is better. .",
                                },
                                },
                                "required": ["better_dialogue", "reasoning"],
                        },
                        
                    },
                    "required": ["feedback"],
                },
            
        }
    ]
    return function_template2
