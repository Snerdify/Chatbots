from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

class WebhookRequest(BaseModel):
    response: str
    session: str
    queryResult: dict


def add_order(session_id:str, parameters: dict):
    # logic
    return f"Adding Order for session {session_id}"

def remove_order(session_id:str, parameters:dict):
    #logic 
    return f"Removing order for session{session_id}"

def track_order(session_id:str , parameters:dict):
    #logic
    return f"Tracking order for session {session_id}"



# 
@app.post('/webhook')
async def webhook_handler(request:WebhookRequest):
    session_id = request.session
    intent = request.queryResult.get("intent",{}).get("displayName")
    parameters = request.queryResult.get("parameters",{})

    if intent == "Add order":
        response = add_order(session_id,parameters)
    if intent == "Remove_order":
        response = remove_order(session_id , parameters)
    if intent == "Track Order":
        response == track_order(session_id,parameters)

    return {"FullfillmentText":response}




