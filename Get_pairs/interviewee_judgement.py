import openai
import os
import nltk
import re
import requests
import time


# nltk.download('punkt')


def check_interviewee(conversation, messages):
    message = conversation
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=1.0,
    )
    reply = ''
    for choice in response.choices:
        reply += choice.message.content

    print(reply)
    return reply
    # print(reply)


def count_tokens(text):
    tokens = nltk.word_tokenize(text)
    return len(tokens)


def truncate_text(text, max_tokens):
    token_count = count_tokens(text)
    if token_count <= max_tokens:
        return text

    tokens = nltk.word_tokenize(text)
    truncated_tokens = tokens[:max_tokens]
    truncated_text = ' '.join(truncated_tokens)
    return truncated_text


def judge_interviewee(key):
    # Set up OpenAI API credentials and max tokens
    openai.api_key = os.getenv('OPENAI_KEY', default=key)
    openai.api_base = "https://ai-yyds.com/v1"
    max_tokens = 10000

    # Directory path
    directory_path = '../Handle/'
    # # Iterate over subdirectories
    count = len(os.listdir(directory_path))
    for i in range(count):
        subdir = os.listdir(directory_path)[i]
        subdir_path = os.path.join(directory_path, subdir)
        messages = []
        messages.append({"role": "system",
                         "content": "You can help to distinguish different people from their conversations in text."})
        prompt = "The following text contains 2-4 people's conversation in text, the conversation is typically an interview, the people are interviewer, interviewee or other uncertaion persons, each sentence will be labled by [00:01:048.38 --> 00:01:051.90] [SPEAKER_00], [00:01:046.61 --> 00:01:046.99] [SPEAKER_01], [00:00:023.99 --> 00:00:028.43][SPEAKER_02] etc, in the first bracket, the number means time, in the second bracket, the label means the speaker, can you help me to distinguish which speaker is interviewee? Please answer like this format: Based on the given text, the speakers can be labeled as follows: [SPEAKER_0x] - Interviewer, [SPEAKER_0x] - Interviewee, [SPEAKER_0x] - Uncertain/Other persons, Note: The labels [SPEAKER_01], [SPEAKER_02], and [SPEAKER_00] are assigned based on the order of appearance in the text. The text is shown as follows: "

        # Check if it's a directory
        if os.path.isdir(subdir_path):
            file_path = os.path.join(subdir_path, 'capspeaker.txt')
            # Read the file contents
            with open(file_path, 'r') as file:
                conversation = file.read()
                conversation = prompt + conversation
                truncated_text = truncate_text(conversation, max_tokens)

                # tokens = nltk.word_tokenize(truncated_text)
                # print(len(tokens))

                result = check_interviewee(truncated_text, messages)
                # print(result)

                with open(os.path.join(subdir_path, "Interviewee_Cap.txt"), "w") as file:
                    print(os.path.join(subdir_path, "Interviewee_Cap.txt"))
                    file.write(result)


def findSpeakers(handle_path):
    speaker_path_interviewee_dic = {}
    speaker_path_interviewer_dic = {}
    # handle_path = f"{path}/1-50-transcript/handle"
    video_lst = os.listdir(handle_path)
    for video in video_lst:
        specific_video_path = f"{handle_path}/{video}"
        with open(f"{specific_video_path}/Interviewee_Cap.txt", 'r') as f:
            answer = f.read()
            f.close()
        pattern_interviewee = r"\[(\s?)(SPEAKER_0[0-9])(\s?)\] - Interviewee"
        match_ee = re.search(pattern_interviewee, answer)
        speaker_path_interviewee_dic[video] = []
        if not match_ee:
            speaker_path_interviewee_dic[video].append("Don't know who")
        else:
            interviewee = match_ee.group(2)
            speaker_path_interviewee_dic[video].append(interviewee.strip())
        pattern_interviewer = r"\[(\s?)(SPEAKER_0[0-9])(\s?)\] - Interviewer"
        match_er = re.search(pattern_interviewer, answer)
        speaker_path_interviewer_dic[video] = []
        if not match_er:
            speaker_path_interviewee_dic[video].append("Don't know who")
        else:
            interviewer = match_er.group(2)
            speaker_path_interviewer_dic[video].append(interviewer.strip())
    return speaker_path_interviewee_dic, speaker_path_interviewer_dic
