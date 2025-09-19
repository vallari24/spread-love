# Product Technical Requirements (PTR)
## Spread Love - Voice Message Chain Project

---

## 1. Project Overview

A prototype application that facilitates spreading positivity through voice messages between strangers via phone calls. The system creates a chain of love messages where participants can both record and receive heartfelt messages from others.

---

## 2. User Experience (UX) Journey

### Journey A: Initial Message Creator
1. **Receive Call**: User receives an automated call from the system
2. **Introduction**: AI voice explains the project - a 2-person team spreading love through voice messages
3. **Invitation**: User is invited to record a message for a stranger
4. **Recording Instructions**: User is asked to say their name and record a love/positivity message
5. **Recording**: After a beep, user records their message
6. **Confirmation**: System confirms message was received
7. **End of Day Reward**: User receives recordings of thank you messages from recipients

### Journey B: Message Recipient & Chain Participant
1. **Receive Call**: User receives an automated call from the system
2. **Project Explanation**: AI voice explains the Spread Love project
3. **Message Playback**: User hears a love message from a stranger
4. **Choice Point**: User can either:
   - Option A: Say thank you and end call
   - Option B: Say thank you AND record their own message for someone else
5. **If Option B**: User records their name and message after the beep
6. **Chain Continues**: Their message gets passed to the next person

### Journey C: Thank You Message Delivery
1. **End of Chain**: After defined number of calls, system reverses
2. **Message Selection**: System picks thank you messages from recipients
3. **Delivery**: Original message creators receive:
   - Text message with appreciation
   - Audio file containing thank you messages

---

## 3. Product Requirements

### 3.1 Core Features

#### Command Line Interface
- Accept phone number input via CLI
- Trigger outbound calls
- Monitor call status and progress
- Display call chain statistics

#### Telephony System
- **Outbound Calling**: Ability to place automated calls to provided numbers
- **Call Flow Management**: Handle different call states (ringing, answered, declined, voicemail)
- **Audio Playback**: Play pre-recorded AI voice instructions and user messages
- **Audio Recording**: Capture user voice messages with beep signal
- **DTMF/Voice Detection**: Detect user choices (continue chain or end)

#### AI Voice System
- Text-to-speech for dynamic script generation
- Natural-sounding voice for instructions
- Multiple script variations:
  - Initial caller script
  - Message recipient script
  - Thank you delivery script

#### Message Management
- **Storage**: Secure storage of recorded messages
- **Metadata Tracking**:
  - Sender name
  - Timestamp
  - Recipient phone number
  - Message status (delivered/pending)
- **Message Queue**: FIFO queue for message distribution
- **Thank You Pool**: Collection of thank you messages for end-of-day delivery

#### SMS Integration
- Send text notifications with thank you messages
- Include link or attachment to audio file
- Delivery confirmation

### 3.2 Technical Requirements

#### Technology Stack (Selected)
- **Web Framework**: FastAPI (Python)
- **AI Voice Platform**: VAPI.ai
  - Handles AI voice conversations
  - Manages conversation flow and state
  - Provides text-to-speech and speech-to-text
  - Assistant configuration for different call scenarios
- **Telephony Provider**: Twilio
  - Phone number management
  - Inbound/outbound call handling
  - SMS capabilities for thank you messages
  - Call routing via webhooks
- **Development Tools**:
  - ngrok for local development/testing
  - Python virtual environment
  - Environment variables for configuration

#### Infrastructure
- **Phone System**: Twilio API with VAPI integration
  - Twilio handles call infrastructure
  - VAPI manages AI conversation layer
  - Webhook-based communication between services
- **Database**: Store user data, messages, and call logs (TBD - PostgreSQL/MongoDB)
- **File Storage**: Cloud storage for audio recordings (AWS S3/Cloudinary)
- **Message Queue**: Handle asynchronous call processing (Redis/RabbitMQ)
- **Hosting**: Cloud deployment (AWS/GCP/Heroku)

#### Integration Architecture
```
User Phone → Twilio Number → FastAPI Webhook → VAPI Assistant → Response
                ↓                    ↓              ↓
           Call Received      Process Request   Generate AI Response
                                     ↓              ↓
                                Store Data    Record/Play Messages
```

#### Security & Privacy
- Phone number anonymization
- Secure audio file storage
- Consent recording at call start
- Data retention policy (auto-delete after X days)
- Opt-out mechanism
- VAPI token authentication
- Environment-based configuration

#### Configuration Parameters
- Maximum chain length (number of calls before reversal)
- Recording time limit (e.g., 30 seconds)
- Daily call limits
- Time window for calls (e.g., 9 AM - 8 PM)
- Geographic restrictions if needed

### 3.3 Call Flow States

```
1. INITIATED -> Call placed
2. RINGING -> Waiting for answer
3. ANSWERED -> Playing introduction
4. RECORDING -> Capturing message
5. PROCESSING -> Saving and queuing message
6. COMPLETED -> Call ended successfully
7. FAILED -> Call failed or user opted out
```

### 3.4 Data Model

#### User Record
- Phone number (hashed)
- Participation timestamp
- Role (initial_creator, chain_participant)
- Message IDs (sent/received)
- Consent status

#### Message Record
- Message ID
- Audio file URL
- Sender name
- Sender phone (hashed)
- Recipient phone (hashed)
- Recording timestamp
- Delivery timestamp
- Status (recorded, queued, delivered, thanked)
- Thank you messages received

#### Call Record
- Call ID
- Phone number (hashed)
- Call type (initial, chain, thank_you)
- Start time
- End time
- Duration
- Status
- Message IDs involved

---

## 4. Implementation Plan with VAPI + Twilio

### 4.1 VAPI Assistant Configuration
The VAPI assistant needs to be configured with different conversation flows:

#### Initial Caller Assistant
- **Greeting**: "Hi! We're a team of two spreading love through voice messages. Would you like to record a message for a stranger?"
- **Instructions**: "Please say your name and then share a message of love or positivity"
- **Recording Trigger**: Detect consent → Play beep → Start recording
- **Completion**: "Thank you! You'll receive thank you messages at the end of the day"

#### Chain Participant Assistant
- **Introduction**: "Hi! This is the Spread Love project"
- **Play Message**: Retrieve and play message from queue
- **Choice Detection**: Voice prompt for user choice
  - If "thank you only" → End call gracefully
  - If "continue chain" → Trigger recording flow
- **Recording Flow**: Same as initial caller

#### Thank You Delivery Assistant
- **Greeting**: "Hi! People loved your message from earlier today"
- **Play Messages**: Play collected thank you messages
- **Closing**: "Thank you for spreading love!"

### 4.2 Technical Implementation Steps

#### Step 1: VAPI Setup
1. Create VAPI account and obtain API token
2. Configure three distinct assistants in VAPI dashboard:
   - `initial_caller_assistant`
   - `chain_participant_assistant`
   - `thank_you_assistant`
3. Set up conversation flows with appropriate prompts
4. Configure recording capabilities and storage

#### Step 2: Twilio Configuration
1. Purchase Twilio phone number(s)
2. Configure webhook to point to FastAPI endpoint
3. Set up SMS capabilities for text notifications
4. Configure call recording settings

#### Step 3: FastAPI Application Development
1. **Endpoints needed**:
   - `/twilio/inbound_call` - Handle incoming calls (existing)
   - `/initiate_call` - CLI endpoint to start outbound calls
   - `/vapi/webhook` - Handle VAPI callbacks
   - `/messages/store` - Store recorded messages
   - `/messages/retrieve` - Get next message in queue
   - `/thank_you/send` - Trigger thank you delivery

2. **Database Models**:
   ```python
   class Message:
       id: str
       sender_phone: str
       sender_name: str
       recipient_phone: str
       audio_url: str
       recorded_at: datetime
       delivered_at: datetime
       thank_you_count: int

   class CallChain:
       id: str
       initial_caller: str
       participants: List[str]
       message_ids: List[str]
       status: str  # active, completed
       created_at: datetime
   ```

3. **Core Functions**:
   - `initiate_outbound_call(phone_number, assistant_type)`
   - `handle_recording_complete(call_sid, recording_url)`
   - `queue_message(message)`
   - `get_next_message()`
   - `send_thank_you_messages(phone_number)`

#### Step 4: Message Queue Implementation
1. Implement FIFO queue for message distribution
2. Track message delivery status
3. Implement chain length counter
4. Handle queue reversal for thank you messages

## 5. MVP Scope

### Phase 1: Basic Prototype (Current Focus)
1. Set up VAPI + Twilio integration (✓ Started)
2. Configure single VAPI assistant for basic flow
3. Implement CLI tool to initiate calls
4. Basic call flow with recording
5. Manual message queue management
6. Local file storage for recordings
7. Test with 10-20 numbers

### Phase 2: Automated Chain
1. Automatic call chaining
2. Thank you message collection
3. End-of-day delivery system
4. Basic analytics dashboard

### Phase 3: Enhanced Features
1. SMS integration
2. Multiple language support
3. Web interface for monitoring
4. Advanced analytics
5. Scheduled calling windows

---

## 5. Success Metrics

- Call completion rate
- Message recording rate
- Chain continuation rate (% who choose to leave their own message)
- Thank you message generation rate
- User sentiment (based on message content analysis)
- Technical metrics (call quality, recording quality, system uptime)

---

## 6. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Spam/unwanted calls perception | Clear opt-out, time restrictions, initial SMS warning |
| Inappropriate content | Content moderation, reporting mechanism |
| Technical failures mid-call | Graceful error handling, callback option |
| Privacy concerns | Clear consent, data minimization, encryption |
| Scalability issues | Queue management, rate limiting, cloud infrastructure |

---

## 7. Future Enhancements

- Web portal for participants to replay messages
- Social media integration for sharing (with consent)
- Themed campaigns (holidays, special events)
- Corporate/organizational partnerships
- Analytics dashboard for impact measurement
- Multi-language support
- Voice emotion analysis for matching messages

---

## 8. Next Implementation Steps

### Immediate Actions Required:
1. **VAPI Configuration**:
   - Create VAPI account
   - Design conversation flows for each assistant type
   - Set up webhooks for call events

2. **Update Existing Code**:
   - Replace placeholder values in `main.py`:
     - `"your-phone-number-id"` with actual Twilio phone number ID
     - `"your-assistant-id"` with VAPI assistant ID
   - Add environment variables for all configuration

3. **Extend FastAPI Application**:
   - Add outbound call initiation endpoint
   - Implement message storage and retrieval
   - Add VAPI webhook handlers for recording events
   - Create CLI interface for phone number input

4. **Database Setup**:
   - Choose and configure database (PostgreSQL recommended)
   - Implement data models
   - Create migration scripts

5. **Testing Infrastructure**:
   - Set up ngrok for local testing
   - Create test phone numbers
   - Implement logging and monitoring

---

## Document Version
- Version: 2.0
- Date: 2025-09-19
- Authors: Spread Love Team (2 members)
- Status: Updated with Technical Implementation Details
- Stack: FastAPI + VAPI + Twilio