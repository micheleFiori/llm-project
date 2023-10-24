import pickle as pkl
from context_descriptor import ContextDescriptor
from prompt_generator import PromptGenerator
from model_request_handler import ModelRequestHandler
import pandas as pd
import numpy as np
from examples_manager import Examples_manager

import time

def derive_context(context_vector):
    context_mapper = {
        "Indoor": 0, "Outdoor": 1,
        "Home": 2, "Office": 3, "University": 4, "Mall": 5, "Station": 6, "Museum": 7, "Gym": 8, "Shop": 9, "Bar": 10,
        "Restaurant": 11, "Barbershop": 12, "Bank": 13, "Church": 14, "NullSemanticPlace": 15,
        "NullSpeed": 16, "LowSpeed": 17, "MediumSpeed": 18, "HighSpeed": 19,
        "Sunny": 20, "Rainy": 21, "Misty": 22, "Cloudy": 23, "Drizzly": 24, "Stormy": 25,
        "NotOnPublicTransportationRoute": 26, "OnPublicTransportationRoute": 27,
        "NegativeHeightVariation": 28, "NullHeightVariation": 29, "PositiveHeightVariation": 30,
        "LowAudioLevel": 31, "MediumAudioLevel": 32, "HighAudioLevel": 33
    }
    inverse_context_mapper = {index: name for name, index in context_mapper.items()}
    context_vector = np.where(np.array(context_vector) == 1)[0]  # returns the indices of the elements equal to 1
    context_vector = [inverse_context_mapper[index] for index in context_vector]
    return context_vector

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



    f_contexts = open(f"./datasets/domino/domino-segmented-w4-hz50.txt", "rb")
    f_consistencies = open(f"./datasets/domino/consistencies.txt", "rb")

    dataset = pkl.load(f_contexts)
    consistencies = pkl.load(f_consistencies)
    contexts = dataset["enhanced_context"]
    labels = dataset['labels']

    unique_instances_dict = {}
    unique_contexts = []
    # Iterate through the rows of the input array
    for idx, row in enumerate(contexts):
        # Convert the row to a tuple to make it hashable
        row_tuple = tuple(row)

        # If the row is not in the dictionary, add it with its index
        if row_tuple not in unique_instances_dict:
            unique_contexts.append(derive_context(list(row_tuple)))
            unique_instances_dict[row_tuple] = {'occurrences': [], 'labels': []}
        unique_instances_dict[row_tuple]['occurrences'].append(idx)
        if labels[idx] not in unique_instances_dict[row_tuple]['labels']:
            unique_instances_dict[row_tuple]['labels'].append(labels[idx])


 
    # context, labels, ontology_consistencies = extrasensory['context'], extrasensory['labels'], extrasensory[
    #    'ontology_consistencies']

    extrasensory_classes = ['BICICLYNG', 'LAYING DOWN', 'MOVING BY CAR', 'ON TRANSPORT', 'SITTING', 'STANDING', 'WALKING']
    domino_classes = ['BRUSHING_TEETH', 'CYCLING', 'ELEVATOR_DOWN', 'ELEVATOR_UP', 'LYING', 'MOVING_BY_CAR', 'RUNNING', 'SITTING', 'SITTING_ON_TRANSPORT', 'STAIRS_DOWN', 'STAIRS_UP', 'STANDING', 'STANDING_ON_TRANSPORT', 'WALKING']
    cd = ContextDescriptor()

    #print(system_message)

    system_message = f'''You are a domain expert in charge of checking which human activities are suitable with respect to the current surrounding context of a user. 
                    You will receive as input a description of the surrounding context of the user. You have to determine which are the activities that are suitable in the given context. 
                    This is the list of the possible user activities that you have to consider: {', '.join(domino_classes)}

                    Accomplish the task by following the steps below:

                    Step 1: Analyze the context.
                    Step 2: Determine which activities are likely in the given context, by analyzing each activity. Apply the open-world assumption: anything that is not explicit in the surrounding context of the user may be possible. Do not exclude activities for which you cannot determine their likelihood or the ones for which there are no specific information about objects and vehicles that the user is using.
                    Step 3: Provide the result in the form of a list.
                                    
                   '''

    #Think about the "answer and step by step analyze each activity.
    #system_message += "In the following i'll give you some examples of contexts that you can receive and the answer " \
    #                  "that i would expect: "


    pg = PromptGenerator(system_message)
    #print(system_message)
    #exit(0)

    handler = ModelRequestHandler()

    start_time = time.time()

    all_responses = []

    i = 0
    #model_examples = Examples_manager('extrasensory_examples.csv')
    model_examples = Examples_manager('domino_examples.csv')
    for c, l, o in list(zip(unique_contexts, unique_contexts_labels, unique_contexts_ontology_consistencies))[:10]:
        i += 1
        
        #description = cd.create_extrasensory_context_description(c)
        description = cd.create_domino_context_description(c)
        print('CURRENT: ', description  )
        most_similar_examples = model_examples.get_most_similar_examples(description)
        #print('SIMILAR: \n', most_similar_examples) 
        print(description)
        print(pg.generate_prompt(description, most_similar_examples))
        responses = handler.handle_request(pg.generate_prompt(description, most_similar_examples), repetitions=1, return_all=True)
        print(responses)
        #all_responses.append(responses)
        print("---------------------------------------------------------------------------------")

    '''
    n_results = 102
    with open(f"results_{n_results}.pkl", "wb") as file:
        pkl.dump(all_responses, file)

    print("--- %s seconds ---" % (time.time() - start_time))
    '''



