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

    def generate_prompt(self, context_description, examples = None):
        examples_prompt = ""
        if examples is not None:
            for ex in examples:
                examples_prompt+=f'''- Context: {ex['context']} \n Likely activities: {ex['expected_output']}\n'''
        user_message = {
            "role": "user",
            "content": f"{examples_prompt}\
                       -Context: {context_description} \n-Likely activities: "
        }
        messages_list = deepcopy(self.messages)
        messages_list.append(user_message)
        return messages_list
