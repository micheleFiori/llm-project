import logging
import re
import ast
from collections import Counter
import vercel_ai

class ModelRequestHandler:

    def __init__(self):
        vercel_ai.logger.setLevel(logging.ERROR)
        self.client = vercel_ai.Client()
        self.params = {
            "maxTokens": 700,  # dimensione massima in token della conversazione
            "temperature": 0
        }
        return

    def get_completion_from_message(self, messages):
        result = ""
        for chunk in self.client.chat("openai:gpt-3.5-turbo-16k", messages, self.params):
            result += chunk
        return result

    def find_vector_in_reply(self, reply):
        find = re.findall(r'\[.*?\]', reply)[0]
        output = ast.literal_eval(find)
        return output

    def handle_request(self, messages, repetitions=1, min_include=0, return_all=False):

        if return_all and min_include>0:
            raise ValueError("if return_all is True min_include must be 0")
        responses = []
        for i in range(repetitions):
            while True:
                try:
                    response = self.get_completion_from_message(messages)
                    #print(response)
                    responses.append([s.lower() for s in self.find_vector_in_reply(response)])
                    break
                except Exception as e:
                    print(e)
                    #print("exception")
                    continue

        if return_all:
            return responses
        else:
            activities = [activity for sublist in responses for activity in sublist]
            #print(activities)
            act_count = Counter(activities)
            #print(act_count)
            filtered_act_count = [act for act, count in act_count.items() if count > min_include]
            #print(filtered_act_count)
            return filtered_act_count
