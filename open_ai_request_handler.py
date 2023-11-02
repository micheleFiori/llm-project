import time

import openai
import re
import ast
from collections import Counter
class OpenAiRequestHandler:

    def __init__(self, api_key, model="gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        return

    def get_completion_from_message(self, messages):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0
        )
        #print(completion.usage)
        return completion.choices[0].message.content, completion.usage

    def find_vector_in_reply(self, reply):
        find = re.findall(r'\[.*?\]', reply)[0]
        output = ast.literal_eval(find)
        return output

    def handle_request(self, messages, repetitions=1, min_include=0, return_all=False):

        if return_all and min_include>0:
            raise ValueError("if return_all is True min_include must be 0")
        responses = []
        usages = []
        for i in range(repetitions):
            while True:
                try:
                    response, usage = self.get_completion_from_message(messages)
                    print("MODEL RESPONSE:\n"+response)
                    responses.append([s.lower() for s in self.find_vector_in_reply(response)])
                    usages.append(usage)
                    time.sleep(20)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(60)
                    #print("exception")
                    continue

        if return_all:
            return responses, usages
        else:
            activities = [activity for sublist in responses for activity in sublist]
            #print(activities)
            act_count = Counter(activities)
            #print(act_count)
            filtered_act_count = [act for act, count in act_count.items() if count > min_include]
            #print(filtered_act_count)
            return filtered_act_count, usages
