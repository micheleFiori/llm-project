from copy import deepcopy


class PromptGenerator:



    def __init__(self, system_message):
        self.messages = []
        self.messages.append(
            {
                "role": "system",
                "content": system_message
            }
        )
        return

    def add_few_shot_example(self, user_message, assistant_message):
        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )
        return

    def generate_prompt(self, context_description):
        user_message = {
            "role": "user",
            "content": "Context: "
                       + context_description
                       + "Use an open-world assumption: anything that is not "\
                         "explicit in the surrounding context of Bob may be possible. Do not exclude activities for which you "\
                         "cannot determine their likelihood. Your final answer should be the list of activities that are likely with "\
                         "respect to Bob's context, spelled exactly as I showed you, with this format ['<activity 1>', '<activity "\
                         "2>', '<activity 3>']."
        }
        messages_list = deepcopy(self.messages)
        messages_list.append(user_message)
        return messages_list
