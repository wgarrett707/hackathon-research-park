from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import os

from dotenv import load_dotenv

load_dotenv(".env") 

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthInfo(BaseModel):
    code: str
    # state: str

class EndUser(BaseModel):
    endUserId: str
    organizationId: str = None

class NangoWebhook(BaseModel):
    type: str
    operation: str
    success: bool
    connectionId: str
    endUser: EndUser

@router.get("/callback", status_code=201)
def callback(code: str):
    print(code)

@router.get("/nango-session-token")
def nango_session_token(user_id: str):

    response = httpx.post(
        "https://api.nango.dev/connect/sessions",
        headers={
            "Authorization": f"Bearer {os.getenv('NANGO_SECRET_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "end_user": {
                "id": user_id,
            },
            "allowed_integrations": [
                "spotify"
            ]
        }
    )
    res = response.json()
    print(res)
    return res.get("data", {})["token"]

@router.post("/nango-webhook")
def nango_webhook(webhook_data: NangoWebhook):
    """
    Handle webhooks from Nango for connection creation notifications.
    This endpoint receives POST requests when users successfully authorize connections.
    """
    print(f"Received Nango webhook: {webhook_data}")
    
    # Check if this is a successful auth creation webhook
    if (webhook_data.type == "auth" and 
        webhook_data.operation == "creation" and 
        webhook_data.success):
        
        # Extract the important data
        connection_id = webhook_data.connectionId
        end_user_id = webhook_data.endUser.endUserId
        organization_id = webhook_data.endUser.organizationId
        
        print(f"New connection created - Connection ID: {connection_id}, User ID: {end_user_id}")
        
        # TODO: Persist the connectionId alongside the corresponding user/organization in your database
        # Example database operation (replace with your actual database logic):
        # db.update_user_connection(end_user_id, connection_id, organization_id)
        
        return {"status": "success", "message": "Webhook processed successfully"}
    
    else:
        print(f"Received non-creation webhook: {webhook_data}")
        return {"status": "received", "message": "Webhook received but not processed"}


