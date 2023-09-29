from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
import generic_helper

app = FastAPI()

inprogress_orders = {}



# session id : session id associated with user's ongoing conversation.


def add_to_order(session_id:str, parameters: dict):
    # parameters contains info about user's request , 
    # here , it contains the food items and quantities , that are to be added to the order
    # below are the food-items and numbers associated with user's request
    food_items = parameters["food-item"]
    quantities = parameters["number"]


# list of food_items and list of quatities should be the same , 
# if not we assume that user didnt provide a quantity for a food item
    if len(food_items) !=len(quantities):
        # fullfillment-text is like console.log
        fullfillment_text= "Sorry didnt get what you are trying to say. Can you specify food items and quantities clearly"
    else:
        # this new dict represents the corresponding food_items with their quantity
        new_food_dict = dict(zip(food_items,quantities))

# check - if session_id is already present in inprogress_orders
        if session_id in inprogress_orders:
            #this dict retrieves the existing order as a dict , this order is associated with the above session id 
            current_food_dict = inprogress_orders[session_id]
            # below line updates the current dict with any food_items that user might have added
            current_food_dict.update(new_food_dict)
# the updated dict is stored in the inprogress orders 
            inprogress_orders[session_id] = current_food_dict
        else:
# if session_id is not present in ongoing-orders , then store it as a new food dict
            inprogress_orders[session_id] = new_food_dict
        
        order_str= generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fullfillment_text = f"So far your order looks like this : {order_str}. Do you want to add anything else ? "

    return JSONResponse(content={
        "fullfillmentText": fullfillment_text
    })



def remove_from_order(session_id:str, parameters:dict):
    #logic 
    return f"Removing order for session{session_id}"

def track_order(session_id:str , parameters:dict):
    #logic
    return f"Tracking order for session {session_id}"


def complete_order(session_id:str, parameters:dict):
    return f"Order completed"



@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }




