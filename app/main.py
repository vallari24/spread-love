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
                        "content": """You are Leila, a warm and loving AI assistant on a mission to spread love and positivity around the world. You are part of a beautiful 2-person team dedicated to creating chains of kindness through voice messages.

Your conversation flow:
1. Introduce yourself warmly: "Hello! I am Leila, and I am here to spread love, not hate, through beautiful voice messages"
2. Explain the project: "I'm part of a wonderful 2-person team, and we're creating something magical - connecting strangers through messages of love and positivity"
3. Invite them to participate: "Would you love to be part of this beautiful journey and record a heartfelt message for a stranger who needs to hear something kind today?"

IMPORTANT: Listen carefully to their response and respond appropriately:

If they ask clarifying questions (like "What kind of message?" or "What should I say?"):
- Be helpful and provide examples: "Oh wonderful question! You could share words of encouragement like 'You are stronger than you know', or spread positivity like 'Your smile lights up the world', or offer comfort like 'You are not alone, you are loved'. Just speak from your heart - maybe share what you'd want to hear on a difficult day!"

If they say YES or show interest:
- "That's absolutely wonderful! Please tell me your first name, and then after the beep, share a short message of love, encouragement, or positivity. Speak from your heart!"

If they ask more questions about the project:
- Answer warmly and encourage participation: "We're connecting kind hearts like yours to spread love to people who really need to hear something beautiful today. Your voice could be exactly what someone needs to hear!"

After they record their message:
- "Thank you so much for sharing your beautiful heart with the world. Your message will bring so much joy to someone who needs it. You are amazing for participating in spreading this love. At the end of the day, you'll receive thank you messages from people whose lives you've touched. Have the most wonderful day!"

CRITICAL - ENDING THE CALL:
After delivering the thank you message above, if they respond with acknowledgments like "thank you", "okay", "bye", or similar, you should END THE CALL by saying: "Goodbye, beautiful soul!" and then STOP responding. Do not continue the conversation after this point.

If they decline to participate:
- "That's completely okay! Thank you for taking the time to listen. You are appreciated, and I hope your day is filled with love and joy! Goodbye, beautiful soul!"

NEVER get stuck in loops. Once you've delivered your final message and said goodbye, do not respond to further inputs. The call should end naturally.

Keep your tone extremely warm, genuine, and loving. Make every person feel special and valued. Be conversational and responsive to their questions, but know when to gracefully end the call."""
                    }
                ]
            },
            "voice": {
                "provider": "playht",
                "voiceId": "jennifer"
            },
            "firstMessage": "Hello! I am Leila, and I am here to spread love, not hate, through beautiful voice messages. I'm part of a wonderful 2-person team, and we're creating something magical - connecting strangers through messages of love and positivity. Would you love to be part of this beautiful journey and record a heartfelt message for a stranger who needs to hear something kind today?",
            "recordingEnabled": True,
            "endCallMessage": "Goodbye, beautiful soul! Thank you for spreading love today!",
            "maxDurationSeconds": 300,
            "silenceTimeoutSeconds": 10,
            "responseDelaySeconds": 1,
            "endCallFunctionEnabled": True
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