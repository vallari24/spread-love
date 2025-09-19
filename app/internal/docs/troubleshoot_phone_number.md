# 🔧 Phone Number Troubleshooting Guide

## ❌ "Number Not Found on Twilio" Error

This error means VAPI can't find your phone number in Twilio. Here are the solutions:

## 🎯 **Solution 1: Use VAPI Phone Number ID (Recommended)**

### Step 1: Register Your Phone Number in VAPI
1. Go to [VAPI Dashboard](https://dashboard.vapi.ai/)
2. Navigate to **Phone Numbers** section
3. Click **"Add Phone Number"**
4. Select **"Twilio"** as provider
5. Enter your phone number: `+16282502830`
6. Enter your Twilio Account SID and Auth Token
7. Save and copy the generated **Phone Number ID**

### Step 2: Update Your .env File
```bash
VAPI_PRIVATE_TOKEN=your_actual_vapi_token_here
VAPI_PHONE_NUMBER_ID=your_phone_number_id_from_vapi_dashboard
```

### Step 3: Test the Call
```bash
curl -X POST "http://localhost:8000/make_outbound_call" \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "+17247327261"}'
```

---

## 🎯 **Solution 2: Direct Twilio Integration (Alternative)**

### Step 1: Verify Phone Number in Twilio Console
1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Phone Numbers** → **Manage** → **Active numbers**
3. Confirm `+1 (628) 250-2830` is listed and active
4. If not listed, you need to purchase/port this number

### Step 2: Get Required Twilio Credentials
```bash
# From Twilio Console Dashboard:
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
```

### Step 3: Update Your .env File
```bash
VAPI_PRIVATE_TOKEN=your_actual_vapi_token_here
TWILIO_PHONE_NUMBER=+16282502830
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔍 **Common Issues & Solutions**

### Issue: "Phone number not owned by your account"
- **Solution**: The number `+16282502830` must be purchased/active in YOUR Twilio account
- **Check**: Twilio Console → Phone Numbers → Active Numbers

### Issue: "Invalid phone number format"
- **Solution**: Ensure format is `+16282502830` (E.164 format)
- **No spaces, dashes, or parentheses**

### Issue: "Twilio credentials invalid"
- **Solution**: Double-check Account SID and Auth Token from Twilio Console
- **Make sure**: No extra spaces or characters when copying

### Issue: "VAPI integration not working"
- **Solution**: In VAPI Dashboard, ensure Twilio integration is properly connected
- **Check**: Phone Numbers section shows your number as "Active"

---

## 🧪 **Quick Test Commands**

### Test 1: Check if phone number is registered in VAPI
```bash
curl -H "Authorization: Bearer your_vapi_token" \
     https://api.vapi.ai/phone-number
```

### Test 2: Verify Twilio number ownership
```bash
curl -u "your_account_sid:your_auth_token" \
     "https://api.twilio.com/2010-04-01/Accounts/your_account_sid/IncomingPhoneNumbers.json"
```

---

## 📞 **Expected Success Response**
```json
{
  "success": true,
  "message": "Call initiated successfully",
  "call_id": "call_12345678-1234-1234-1234-123456789abc",
  "status": "queued"
}
```

## 🆘 **Still Having Issues?**

1. **Check VAPI Dashboard**: Ensure phone number shows as "Active"
2. **Check Twilio Console**: Confirm number ownership and active status
3. **Verify Integration**: VAPI → Settings → Integrations → Twilio (should be connected)
4. **Contact Support**: If all above steps are correct, contact VAPI support with your phone number ID

The most reliable approach is **Solution 1** using VAPI Phone Number ID! 🎯
