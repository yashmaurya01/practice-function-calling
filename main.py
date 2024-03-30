# from code import FunctionCall
from openai import OpenAI
import time
import json

with open(".secrets", "r") as f:
    openai_key = f.read().strip()


client = OpenAI(
    api_key=openai_key,
    )

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


def ask_openai_functioncalling(system_prompt, user_dialog, function_call_name, function_template, ai_notes=None, timeout=1):
	messages=[
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user_dialog},
	]
	if ai_notes is not None:
		messages.append({"role": "system", "content": ai_notes})

	response = client.chat.completions.create(
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

def ask_openai(system_prompt, user_dialog, ai_notes=None, timeout=1):
	messages=[
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user_dialog},
	]
	if ai_notes is not None:
		messages.append({"role": "system", "content": ai_notes})
		
	response = client.chat.completions.create(
		model="gpt-3.5-turbo-1106",
		messages=messages,
		temperature=0.1,
		max_tokens=512,
	)
	answer = response.choices[0].message.content
	time.sleep(timeout)
	return answer

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

def build_context_and_response(cleaned_dialogues, context_length=4):
    """
    Builds a context for each of Speaker 0's dialogues from a list of cleaned dialogues.
    
    Args:
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
                  "summary": ask_openai("Give a one line summary of the conversation", condensed_context),
                "previous context": condensed_context,
                "current dialogue": dialogue
            }
            # print(dialogue_piece)

            current_user_dialog = "Summary: \n"+ dialogue_piece["summary"] + "\nPrevious conversation: \n" + dialogue_piece["previous context"] + "\nCurrent dialogue: \n" + dialogue_piece["current dialogue"]
            print(current_user_dialog)

            feedback = ask_openai_functioncalling(system_prompt2, current_user_dialog, "give_feedback", function_template2)
            print("\nBetter Dialogue: " + feedback['feedback']['better_dialogue']+ "\nReasoning: " + feedback['feedback']['reasoning'])
            print("\n\n")


            dialogue_pieces.append(dialogue_piece)
            # if len(dialogue_pieces) == 3:
            #     break
        
        dialogue_history.append(dialogue)

    return dialogue_pieces


context = """
1
00:00:00,000 --> 00:00:00,209
Speaker 1: Here?

2
00:00:00,649 --> 00:00:01,008
Speaker 1: CLI?

3
00:00:01,670 --> 00:00:02,150
Speaker 0: What do you mean?

4
00:00:02,930 --> 00:00:05,851
Speaker 1: Just ask, before recording ask for an input.

5
00:00:06,511 --> 00:00:07,592
Speaker 0: Yeah, yeah, yeah, sure.

6
00:00:08,672 --> 00:00:11,653
Speaker 0: As you need help from GPU to help me later.

7
00:00:13,474 --> 00:00:14,194
Speaker 1: You can do input.

8
00:00:14,615 --> 00:00:15,455
Speaker 1: You're not believing me?

9
00:00:17,296 --> 00:00:17,676
Speaker 0: Okay.

10
00:00:19,036 --> 00:00:19,637
Speaker 0: What do I do?

11
00:00:20,977 --> 00:00:21,197
Speaker 1: Come.

12
00:00:22,318 --> 00:00:22,638
Speaker 1: Where is it?

13
00:00:31,901 --> 00:00:32,040
Speaker 0: Oh.

14
00:00:33,442 --> 00:00:33,802
Speaker 0: Hmm.

15
00:00:35,082 --> 00:00:35,722
Speaker 1: See, I was fast.

16
00:00:35,742 --> 00:00:38,483
Speaker 0: Okay.

17
00:00:40,964 --> 00:00:41,224
Speaker 0: Hmm.

18
00:00:42,444 --> 00:00:42,724
Speaker 0: Good?

19
00:00:43,205 --> 00:00:43,485
Speaker 1: Mm-hmm.

20
00:00:47,606 --> 00:00:48,246
Speaker 0: Actually...

21
00:00:49,326 --> 00:00:52,147
Speaker 1: The duration can be... We don't have to get the duration.

22
00:00:53,668 --> 00:00:54,188
Speaker 0: Why not?

23
00:00:58,141 --> 00:00:58,841
Speaker 1: Okay, might as well.

24
00:00:59,321 --> 00:01:05,764
Speaker 0: Okay, I think this is working now, but next we need a streaming record.

25
00:01:07,665 --> 00:01:09,226
Speaker 1: You want to real-time stream?

26
00:01:10,086 --> 00:01:14,128
Speaker 0: Not real-time streaming, it's just now.

27
00:01:14,468 --> 00:01:21,011
Speaker 0: I will record for 30 minutes and then flush from the memory.

28
00:01:21,591 --> 00:01:27,088
Speaker 0: Memory once, only once, but I want it to be flush every second.

29
00:01:27,528 --> 00:01:31,170
Speaker 1: okay this is this is just a script for us.

30
00:01:31,551 --> 00:01:38,355
Speaker 1: right we will have to write it in the client app where whichever we are building hello.

31
00:01:38,395 --> 00:01:39,516
Speaker 1: how are we building the client app?

32
00:01:43,499 --> 00:01:44,199
Speaker 0: i don't understand.

33
00:01:44,900 --> 00:01:46,141
Speaker 0: what do what?

34
00:01:46,341 --> 00:01:47,582
Speaker 0: what are you trying to?

35
00:01:48,182 --> 00:01:58,882
Speaker 1: i'm trying to say like if if we use python to build the client app yes this makes sense too But will we be writing the client app in Python?

36
00:02:00,902 --> 00:02:01,862
Speaker 0: What's the options?

37
00:02:02,303 --> 00:02:02,763
Speaker 0: Flutter?

38
00:02:03,443 --> 00:02:04,163
Speaker 1: React Native.

39
00:02:05,303 --> 00:02:06,524
Speaker 0: We were talking about Flutter.

40
00:02:06,984 --> 00:02:08,404
Speaker 1: We were talking about Flutter.

41
00:02:08,503 --> 00:02:13,385
Speaker 1: I'm saying examples of where which, none of which include Python is what I meant to say.

42
00:02:13,485 --> 00:02:14,326
Speaker 0: Which one is best?

43
00:02:15,066 --> 00:02:15,966
Speaker 0: I think Flutter is doable.

44
00:02:17,475 --> 00:02:19,577
Speaker 0: Because you just mentioned React.

45
00:02:20,037 --> 00:02:21,858
Speaker 1: I'm saying I was giving you options.

46
00:02:22,238 --> 00:02:23,139
Speaker 0: Which one is the best?

47
00:02:23,519 --> 00:02:24,160
Speaker 0: Flutter is good.

48
00:02:24,660 --> 00:02:25,381
Speaker 0: Then Flutter?

49
00:02:25,601 --> 00:02:26,001
Speaker 1: Flutter.

50
00:02:26,541 --> 00:02:27,662
Speaker 0: Is it the fastest?

51
00:02:28,483 --> 00:02:29,083
Speaker 1: It's the fastest.
"""
context = """1
00:00:00,060 --> 00:00:00,670
Speaker 0: Say it again.

2
00:00:01,050 --> 00:00:01,710
Speaker 1: Say what again?

3
00:00:02,531 --> 00:00:03,612
Speaker 0: It never happened.

4
00:00:04,011 --> 00:00:04,833
Speaker 0: After you get a job?

5
00:00:05,294 --> 00:00:09,037
Speaker 1: First job is to think about getting you guys to Hawaii.

6
00:00:10,938 --> 00:00:12,980
Speaker 1: How much do you think it will cost?

7
00:00:12,980 --> 00:00:14,161
Speaker 1: $10,000?

8
00:00:14,161 --> 00:00:14,922
Speaker 0: Each person?

9
00:00:15,262 --> 00:00:15,542
Speaker 0: Overall.

10
00:00:15,562 --> 00:00:16,283
Speaker 0: I'm flattered.

11
00:00:16,643 --> 00:00:17,064
Speaker 1: Overall.

12
00:00:18,005 --> 00:00:20,927
Speaker 0: How many people?

13
00:00:21,367 --> 00:00:21,988
Speaker 0: How many people?

14
00:00:22,008 --> 00:00:23,109
Speaker 0: I actually searched for it.

15
00:00:23,509 --> 00:00:23,930
Speaker 0: How many people?

16
00:00:23,950 --> 00:00:24,230
Speaker 0: Seven.

17
00:00:25,091 --> 00:00:25,671
Speaker 0: Seven people.

18
00:00:26,132 --> 00:00:27,413
Speaker 0: Not including your bride?

19
00:00:30,965 --> 00:00:31,165
Speaker 0: Eight?

20
00:00:31,185 --> 00:00:35,608
Speaker 0: Or maybe not include yourself.

21
00:00:38,249 --> 00:00:38,970
Speaker 0: Ticket is not...

22
00:00:39,750 --> 00:00:40,911
Speaker 1: Ticket is what?

23
00:00:41,071 --> 00:00:41,951
Speaker 1: Oh, you guys?

24
00:00:42,812 --> 00:00:48,075
Speaker 0: How much is it?

25
00:00:48,555 --> 00:00:50,476
Speaker 1: They are seeing tickets for Hawaii.

26
00:00:50,656 --> 00:00:51,497
Speaker 1: Tickets to Hawaii.

27
00:00:53,738 --> 00:00:54,959
Speaker 1: Okay, wait for three more years.

28
00:00:56,220 --> 00:00:57,180
Speaker 0: Three more years?

29
00:00:57,821 --> 00:00:58,281
Speaker 1: What?

30
00:00:58,961 --> 00:00:59,762
Speaker 1: I should get a job.

31
00:01:00,444 --> 00:01:02,405
Speaker 1: I mean, I'll get a job in 8 months.

32
00:01:02,605 --> 00:01:04,646
Speaker 1: See, it's not too expensive.

33
00:01:04,825 --> 00:01:05,346
Speaker 0: Yeah, it's fine.

34
00:01:05,887 --> 00:01:09,648
Speaker 0: So, ticket for 8 people is 8,000.

35
00:01:09,648 --> 00:01:10,649
Speaker 1: Ah, fuck you.

36
00:01:13,990 --> 00:01:15,651
Speaker 0: And 3 hotel rooms.

37
00:01:15,711 --> 00:01:16,632
Speaker 0: Is it like one-way?

38
00:01:17,112 --> 00:01:17,992
Speaker 1: Yeah, this is one-way.

39
00:01:18,533 --> 00:01:20,413
Speaker 0: Hey, no, I think it's... No, this is one-way.

40
00:01:20,473 --> 00:01:21,314
Speaker 0: I selected one-way.

41
00:01:21,534 --> 00:01:23,495
Speaker 0: Wait, did I select the one-way?

42
00:01:24,364 --> 00:01:25,725
Speaker 0: So you still have 2000 just there.

43
00:01:25,765 --> 00:01:27,727
Speaker 0: Where are you going?

44
00:01:27,847 --> 00:01:28,067
Speaker 1: Where?

45
00:01:28,107 --> 00:01:30,649
Speaker 1: We'll just let you stranded and we'll see.

46
00:01:30,669 --> 00:01:31,150
Speaker 0: Fuck.

47
00:01:31,710 --> 00:01:32,130
Speaker 1: Oh my God.

48
00:01:32,150 --> 00:01:34,532
Speaker 1: This guy is recording.
"""

system_prompt1 = "You are a language teacher who helps non-native English speakers help get better in daily life conversations. You are to analyze the conversation between two people, Speaker 0 and Speaker 1. The main user is Speaker 0. Understand what kind of social setting is the user in currently based on the conversation. Based on this analysis, get the tone of the conversation and the main theme and sub_themes of the discussion. This information should help give the user constructive feedback on their dialogs."

user_dialog = "Conversation: "+ context

info = ask_openai_functioncalling(system_prompt1, user_dialog, "get_tone", function_template1)
print(info)

'''
Example of info:
info =
    {
        "conversation_info": {
            "tone": "informal",
            "theme": {
                "main_theme": "Building a client app",
                "sub_themes": [
                    "Python",
                    "Flutter",
                    "React Native"
                ]
            }
        }
    }
'''

system_prompt2 = f"You are a language teacher who helps non-native English speakers help get better in daily life conversations. You are to analyze the conversation between two people, Speaker 0 and Speaker 1. The main user is Speaker 0. This is a {info['conversation_info']['tone']} conversation. Informal conversation would be like between friends where slangs might even be used. Formal conversation would be like where a boss is talking to an employee but since it's a verbal conversation, punctuations would not be very reliable. Try to keep the conversation natural flowing. Neutral would be a mix of both. {info['conversation_info']['theme']['main_theme']} is the main theme of the conversation. The sub-themes are {info['conversation_info']['theme']['sub_themes']} of the conversation. Give constructive feedback to Speaker 0 on their 'Current dialog' and how they could they have better said it. Don't be very strict."

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


# def user_dialog_template(context_response_pairs, i):
#     return "Summary: \n"+ context_response_pairs[i]["previous context"] + "Previous conversation: \n" + context_response_pairs[i]["previous context"] + "\nCurrent dialogue: \n" + context_response_pairs[i]["current dialogue"]

# # # Now we use the cleaned dialogues to build context and current dialogue
context_response_pairs = build_context_and_response(clean_dialogues(context), context_length=4)

# print(context_response_pairs[0])
# # Displaying the context and response pairs
# for index, pair in enumerate(context_response_pairs, 1):
#     print(f"Pair {index}:")
#     print("Previous Context:\n", pair["previous context"])
#     print("Current Dialogue:\n", pair["current dialogue"])
#     print("\n---\n")


# for i in range(6, len(context_response_pairs)):
#     current_user_dialog = user_dialog_template(context_response_pairs, i)
#     print(current_user_dialog)
#     print()
#     feedback = ask_openai_functioncalling(system_prompt2, current_user_dialog, "give_feedback", function_template2)
#     print("Better Dialogue: " + feedback['feedback']['better_dialogue']+ "\nReasoning: " + feedback['feedback']['reasoning'])
#     print("\n\n")

