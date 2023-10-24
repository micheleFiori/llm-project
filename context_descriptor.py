class ContextDescriptor:

    def __init__(self):
        return

    def create_extrasensory_context_description(self, context_vector):
        if context_vector[13] == 1:
            indoors_outdoors = "indoor"
        elif context_vector[14] == 1:
            indoors_outdoors = "outdoor"
        else:
            indoors_outdoors = None
        # TODO gestire caso se tutti e due sono a 1

        if context_vector[15] == 1:
            place = "at home"
        elif context_vector[16] == 1:
            place = "at the workplace"
        elif context_vector[17] == 1:
            place = "at school"
        elif context_vector[18] == 1:
            place = "at the gym"
        elif context_vector[19] == 1:
            place = "at the restaurant"
        elif context_vector[20] == 1:
            place = "doing shopping"
        elif context_vector[21] == 1:
            place = "at the bar"
        elif context_vector[22] == 1:
            place = "at the beach"
        else:
            place = None
        # TODO gestire caso se due o più sono a 1

        # Casi in cui velocità minima e massima sono uguali
        if context_vector[0] == 1 and context_vector[4] == 1:
            speed = "weather still or moving at a speed of less than 1 km/h"
        elif context_vector[1] == 1 and context_vector[5] == 1:
            speed = "moving at a speed between 1 and 4 km/h"
        elif context_vector[2] == 1 and context_vector[6] == 1:
            speed = "moving at a speed between 4 and 12 km/h"
        elif context_vector[3] == 1 and context_vector[7] == 1:
            speed = "moving at a speed of more than 12 km/h"
        # Casi in cui velocità minima e massima sono diversi
        else:
            speed = "moving at a speed ranging from"
            if context_vector[0]:
                speed += " less than 1 km/h"
            elif context_vector[1]:
                speed += " 1 km/h"
            elif context_vector[2]:
                speed += " 4 km/h"
            elif context_vector[3]:
                speed += " 12 km/h"
            speed += " to"
            if context_vector[4]:
                speed += " less than 1 km/h"
            elif context_vector[5]:
                speed += " 4 km/h"
            elif context_vector[6]:
                speed += " 12 km/h"
            elif context_vector[7]:
                speed += " 12 km/h"
            else:
                speed = None

        if context_vector[8] == 1:
            location_diameter = "in a fixed area"
        elif context_vector[9] == 1:
            location_diameter = "within an area with a diameter of less than 50 meters"
        elif context_vector[10] == 1:
            location_diameter = "within an area with a diameter between 50 and 100 meters"
        elif context_vector[11] == 1:
            location_diameter = "within an area with a diameter of more than 100 meters"
        else:
            location_diameter = None

        if context_vector[12] == 1:
            public_transportation = "following a public transportation route"
        else:
            public_transportation = "not following a public transportation route"

        description = "In the last 4 seconds,"
        # Costruzione della frase
        if indoors_outdoors is not None or place is not None:
            description += f" the user Bob was in an"
            if indoors_outdoors is not None:
                description += f" {indoors_outdoors}"
            description += " location"
            if place is not None:
                description += f" {place}"
            description += f", where he"
        else:
            description += " the user Bob"

        if location_diameter is not None:
            description += f" was {location_diameter}"
            if speed is not None:
                description += ","

        if indoors_outdoors is None and place is None and location_diameter is None:
            description += " was"

        if speed is not None:
            description += f" {speed}"

        description+=f", Bob was {public_transportation}"

        return description
    
    def create_domino_context_description(self, context_vector):
        list_at_the = ["Office", "Mall", "Station", "Museum", "Gym", "Shop", "Bar", "Restaurant", "Barbershop",
                       "Bank", "Church"]
        list_at = ["Home"]
        list_in = ["University"]
        list_null = ["NullSemanticPlace"]
        prop = ''
        speed = context_vector[2].split('S')[0]
        range_speed = {
            'Low': " between 1 and 4 km/h",
            'Medium': " between 4 and 12 km/h",
            'High': " above 12 km/h "
        }
        if context_vector[1] in list_null:
            place = ''
        else:
            if context_vector[1] in list_at_the:
                prop = 'at the'
            if context_vector[1] in list_at:
                prop = 'at'
            if context_vector[1] in list_in:
                prop = 'in'
            if context_vector[1] == 'Office':
                context_vector[1] = 'workplace'
            place = ' ' + prop + ' ' + context_vector[1] + ''

        if 'Not' in context_vector[4]:
            transportation = 'not following/close to a public transportation route'
        else:
            transportation = 'currently following/close to a public transportation route'

        if 'Null' in context_vector[5]:
            height = 'neither going up nor down'
        if 'Positive' in context_vector[5]:
            height = 'moving upwards' if speed != 'Null' else 'experiencing a positive elevation change'
        if 'Negative' in context_vector[5]:
            height = 'moving downwards' if speed != 'Null' else 'experiencing a negative elevation change'

        if speed == 'Null':
            travel = 'not moving'
        else:
            travel = 'moving/travelling at a speed' + range_speed[context_vector[2].split('S')[0]] + ''

        #return ''' Given a user's current ''' + context_vector[0] + ''' environment''' + place + ''', where they are ''' + travel + ''', experiencing ''' + context_vector[3] + ''' weather, ''' + transportation + ''', and ''' + height + ''','''
        return ''' In the last 4 seconds the user Bob was in an ''' + context_vector[0] + ''' environment''' + place + ''', where he was ''' + travel + ''', experiencing ''' + context_vector[3] + ''' weather, ''' + transportation + ''', and ''' + height + '''.'''
