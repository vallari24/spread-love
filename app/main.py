from fastapi import FastAPI, Form, HTTPException
from .types import CallData
import requests
from twilio.twiml.voice_response import VoiceResponse
from fastapi.responses import PlainTextResponse
import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel


load_dotenv()

app = FastAPI()
api_key = os.environ.get("VAPI_PRIVATE_TOKEN")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER", "+16282502830")
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
vapi_phone_number_id = os.environ.get("VAPI_PHONE_NUMBER_ID")

class OutboundCallRequest(BaseModel):
    phone_number: str


@app.post("/twilio/inbound_call", response_class=PlainTextResponse)
async def receive_call_data(
        AccountSid: str = Form(...),
        ApiVersion: str = Form(...),
        Called: str = Form(...),
        CalledCity: Optional[str] = Form(None),
        CalledCountry: str = Form(...),
        CalledState: str = Form(...),
        CalledZip: Optional[str] = Form(None),
        Caller: str = Form(...),
        CallerCity: str = Form(...),
        CallerCountry: str = Form(...),
        CallerState: str = Form(...),
        CallerZip: str = Form(...),
        CallSid: str = Form(...),
        CallStatus: str = Form(...),
        CallToken: str = Form(...),
        Direction: str = Form(...),
        From: str = Form(...),
        FromCity: str = Form(...),
        FromCountry: str = Form(...),
        FromState: str = Form(...),
        FromZip: str = Form(...),
        StirVerstat: str = Form(...),
        To: str = Form(...),
        ToCity: Optional[str] = Form(None),
        ToCountry: str = Form(...),
        ToState: str = Form(...),
        ToZip: Optional[str] = Form(None)
):
    call_data = CallData(
        AccountSid=AccountSid,
        ApiVersion=ApiVersion,
        Called=Called,
        CalledCity=CalledCity,
        CalledCountry=CalledCountry,
        CalledState=CalledState,
        CalledZip=CalledZip,
        Caller=Caller,
        CallerCity=CallerCity,
        CallerCountry=CallerCountry,
        CallerState=CallerState,
        CallerZip=CallerZip,
        CallSid=CallSid,
        CallStatus=CallStatus,
        CallToken=CallToken,
        Direction=Direction,
        From=From,
        FromCity=FromCity,
        FromCountry=FromCountry,
        FromState=FromState,
        FromZip=FromZip,
        StirVerstat=StirVerstat,
        To=To,
        ToCity=ToCity,
        ToCountry=ToCountry,
        ToState=ToState,
        ToZip=ToZip
    )

    r = requests.post("https://api.vapi.ai/call", json={
        "phoneNumberId": "your-phone-number-id",
        "phoneCallProviderBypassEnabled": True,
        "customer": {
            "number": call_data.Caller
        },
        "assistantId": "your-assistant-id"
    }, headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    result = r.json()

    return result["phoneCallProviderDetails"]["twiml"]


@app.post("/make_outbound_call")
async def make_outbound_call(request: OutboundCallRequest):
    """Make an outbound call to spread kindness"""
    if not api_key:
        raise HTTPException(status_code=500, detail="VAPI_PRIVATE_TOKEN not configured")
    
    # Prepare call request - try phoneNumberId first, then fallback to direct Twilio config
    call_request = {
        "customer": {
            "number": request.phone_number
        },
        "assistant": {
            "model": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a kind AI assistant helping to spread love and positivity around the world. 

Your role is to:
1. Greet the person warmly
2. Say: "Hi! We are here to spread love, not hate. Do you want to leave a message for the next caller?"
3. If they say yes, ask them to record a 30-60 second positive message
4. Thank them for participating in spreading kindness
5. If they say no, thank them for their time and wish them a wonderful day

Keep the conversation brief, warm, and focused on spreading positivity. Be respectful if they want to end the call."""
                    }
                ]
            },
            "voice": {
                "provider": "playht",
                "voiceId": "jennifer"
            },
            "firstMessage": "Hi! We are here to spread love, not hate. Do you want to leave a message for the next caller?",
            "recordingEnabled": True,
            "endCallMessage": "Thank you for helping spread kindness! Have a wonderful day!",
            "maxDurationSeconds": 300
        }
    }
    
    # Add phone number configuration - prefer phoneNumberId if available
    if vapi_phone_number_id:
        call_request["phoneNumberId"] = vapi_phone_number_id
    elif twilio_account_sid:
        call_request["phoneNumber"] = {
            "twilioPhoneNumber": twilio_phone_number,
            "twilioAccountSid": twilio_account_sid
        }
    else:
        raise HTTPException(
            status_code=500, 
            detail="Either VAPI_PHONE_NUMBER_ID or TWILIO_ACCOUNT_SID must be configured"
        )
    
    # Make the call via VAPI
    try:
        response = requests.post("https://api.vapi.ai/call", 
            json=call_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        
        if response.status_code == 201:
            result = response.json()
            return {
                "success": True, 
                "message": "Call initiated successfully",
                "call_id": result.get("id"),
                "status": result.get("status")
            }
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Failed to initiate call: {response.text}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error making API call: {str(e)}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Kindness Chain API is running", "status": "healthy"}


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to check configuration"""
    return {
        "vapi_token_configured": bool(api_key),
        "vapi_phone_number_id_configured": bool(vapi_phone_number_id),
        "twilio_phone_number": twilio_phone_number,
        "twilio_account_sid_configured": bool(twilio_account_sid),
        "recommended_approach": "Use VAPI_PHONE_NUMBER_ID for best results",
        "help": "See troubleshoot_phone_number.md for setup instructions"
    }