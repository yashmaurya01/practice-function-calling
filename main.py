from LanguageFeedback import *

if __name__ == "__main__":
    api_path = ".secrets"
    conversation = """1
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

49
00:01:34,653 --> 00:01:34,973
Speaker 1: Okay.

50
00:01:34,993 --> 00:01:35,293
Speaker 0: Fuck.

51
00:01:35,373 --> 00:01:35,853
Speaker 1: Fuck you.

52
00:01:35,934 --> 00:01:37,095
Speaker 1: I need to send flowers.

53
00:01:37,175 --> 00:01:38,776
Speaker 1: Come on.

"""
    # Create an instance of the LanguageFeedback class
    LF = LanguageFeedback(api_path, conversation)

    # Get the feedback for the given text
    feedback = LF.get_feedback()
    