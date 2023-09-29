from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
import generic_helper
import db_helper
app = FastAPI()

inprogress_orders = {}


def save_to_db(order:dict):
    return ""


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
    # to remove something from an order , the order must be already initiated
    # i.e the order must already be present in the existing orders
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fullfillmentText": "Im having trouble finding your order , could you please start a new order"
        })
    # if the order is present in inprogress orders then , get user's info
    # here we get food_items that are to be removed  and the session_id of that order
    food_items= parameters["food_item"]
    current_order = inprogress_orders[session_id]
    # initialize two empty dicts , one for populating all the items user removes
    # another one for items that are not present in the current order list
    removed_items = []
    no_such_items = []
    # now we know that food_items here is a list that contains all the preexisting items that are present in the user's list
    # so if user requests to remove an item that is not present in the food_items then ,
    # send a msg that such item is not in the list , hence user cant remove it
    for item in food_items:
        if item not in food_items:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

# if the items were successfully removed then , send a fullfillment text
    if len(removed_items) > 0 :
        fullfillment_text = f'Removed {",".join(removed_items)} from your order'
# when user wants to remove an item that is not present in the current order list
    if len(no_such_items)>0:
        fullfillment_text = f'Your current order does not have {",".join(no_such_items)}'

# if the current order has been started by the user but nothinh has been added yet
    if len(current_order.keys())==0:
        fullfillment_text += "Nothing has been added yet"
    else:
        order_str= generic_helper.get_str_from_food_dict(current_order)
        fullfillment_text += f"Your order currently contains :{order_str}"

    return JSONResponse(content={
        "fullfillmentText" : fullfillment_text
    })




    
    
def track_order(session_id:str , parameters:dict):
    # to track the order , we need to extract the id from the parameters
    order_id = int(parameters['order_id'])
# we retrieve the status of the order given the order id
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fullfillment_text = f"The order status for {order_id} is : {order_status}"
    else:
        fullfillment_text = f"No order found with order id :{order_id}"
    return JSONResponse(content={
        "fullfillmentText" : fullfillment_text
    })



 
def complete_order(session_id:str, parameters:dict):
    if session_id not in inprogress_orders:
        fullfillment_text=f"Sorry couldn't fetch your order.Can you please place a new order."
    else:
        order = inprogress_orders[session_id]
        # since the order is available and is in progress
        # we can use the save_to_db function to fetch the order_id of that order
        order_id= save_to_db(order)
# order_id = -1 typically indicates the failure in saving the order to the db
# or could be a failure in fetching the order_id
        if order_id == -1 :
            fullfillment_text= f"Sorry, Couldn't process your order due to a backend error,please place a new order"
        else:
            # if the id is found in the database
            # then prepare the order total for the user
            order_total = db_helper.get_total_order_price(order_id)
            fullfillment_text = f"Excellent! your order is in progress."\
                                f"This is your order_id #{order_id}" \
                                f"Your bill is {order_total}"
# this indicates that the order is no longer in progress.
        del(inprogress_orders[session_id])

        return JSONResponse(content={
            "fullfillmentText":fullfillment_text
        })







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




