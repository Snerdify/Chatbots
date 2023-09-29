# create a func that summarizes the contents of food_dict in a human readable format
# create a func that could extract the session_id from a larger string. 
# this id could then be presented to the user , so that they could use it
# in conversations and to track orders

import re

def get_str_from_food_dict(food_dict: dict):
    result = ".".join([f"{int(value)}{key}" for key , value in food_dict.items()])
    return result 


def extract_session_id(session_str : str):
    # searches for a string that starts with /sessions/ and ends with /contexts/
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)

    if match:
        # if the session_id is found within the string , 
        # i.e if the match is found , then extract the entire matched string and store it in the variable called 
        # extracted_string
        extracted_string = match.group(0)
        return extracted_string
    # if no match is found then return an empty string
    return ""
    