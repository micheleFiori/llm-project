import pickle as pkl
from context_descriptor import ContextDescriptor
from prompt_generator import PromptGenerator
from model_request_handler import ModelRequestHandler
import pandas as pd

import time

if __name__ == '__main__':
    extrasensory_path = "datasets/extrasensory/extrasensory.pkl"

    # with open(extrasensory_path, "rb") as f:
    #    extrasensory = pkl.load(f)

    with open("datasets/extrasensory/extrasensory_unique_contexts.pkl", "rb") as file:
        unique_contexts = pkl.load(file)
    with open("datasets/extrasensory/extrasensory_unique_contexts_labels.pkl", "rb") as file:
        unique_contexts_labels = pkl.load(file)
    with open("datasets/extrasensory/extrasensory_unique_contexts_ontology_consistencies.pkl", "rb") as file:
        unique_contexts_ontology_consistencies = pkl.load(file)

    # context, labels, ontology_consistencies = extrasensory['context'], extrasensory['labels'], extrasensory[
    #    'ontology_consistencies']

    classes = ['Bicycling', 'laying down', 'moving by car', 'on transport', 'sitting', 'standing', 'walking']

    cd = ContextDescriptor()

    #print(system_message)

    system_message = "You are a domain expert in charge of checking which human activities are likely with respect to " \
                     "the current surrounding context of a user. You will receive as input a description of the " \
                     "surrounding context of the user. You have to determine which are the activities that are " \
                     "likely to be performed by the user in the given context. This is the list of the possible user " \
                     "activities that you have to consider: 'Bicycling','laying down', 'moving by car', 'on transport'" \
                     ", 'sitting', 'standing', 'walking'.  Accomplish the task by following the steps below: " \
                     "Step 1: Analyze the context. Step 2: Determine which activities are likely in the given context, " \
                     "by analyzing each activity. Step 3: Provide the result in the form of a list. Think about the " \
                     "answer and step by step analyze each activity."



    system_message += "In the following i'll give you some examples of contexts that you can receive and the answer " \
                      "that i would expect: "

    examples = pd.read_csv("examples.csv")
    for c, o in list(zip(examples.context.to_list(), examples.expected_output.to_list()))[3:]:
        #pg.add_few_shot_example("context: " + c, o)
        system_message += f"\nContext: {c}. Expected output: {o}."

    pg = PromptGenerator(system_message)
    #print(system_message)
    #exit(0)

    handler = ModelRequestHandler()

    start_time = time.time()

    all_responses = []

    i = 0
    for c, l, o in list(zip(unique_contexts, unique_contexts_labels, unique_contexts_ontology_consistencies))[:10]:
        print(i)
        i += 1
        print(l, o)
        description = cd.create_extrasensory_context_description(c)
        print(description)
        print(pg.generate_prompt(description))
        responses = handler.handle_request(pg.generate_prompt(description), repetitions=1, return_all=True)
        print(responses)
        all_responses.append(responses)
        print("---------------------------------------------------------------------------------")


    n_results = 102
    with open(f"results_{n_results}.pkl", "wb") as file:
        pkl.dump(all_responses, file)

    print("--- %s seconds ---" % (time.time() - start_time))





    for c, o in list(zip(unique_contexts, unique_contexts_ontology_consistencies)):
        print(o)
        print(cd.create_extrasensory_context_description(c))



