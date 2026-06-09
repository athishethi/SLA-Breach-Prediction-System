import os
from twilio.rest import Client
from dotenv import load_dotenv

# Initialize and pull credentials from the local environment file
load_dotenv()

def send_sla_sms_alert(customer_name: str, ticket_id: str, minutes_left: int, risk_level: str) -> bool:
    """
    Sends an automated, real-time WhatsApp warning message to the on-call support team
    whenever an active incident drops below safe SLA remaining time thresholds.
    """
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = os.getenv('TWILIO_PHONE_NUMBER')
    to_phone = os.getenv('ALERT_RECIPIENT_PHONE')

    if not all([account_sid, auth_token, from_phone, to_phone]):
        print("[Twilio Bypass] Missing credentials in local .env file. Skipping Alert.")
        return False

    try:
        client = Client(account_sid, auth_token)
        
        # WhatsApp supports clean markdown formatting like bold text
        message_body = (
            f"🚨 [SLA OUTAGE EMERGENCY DISPATCH] 🚨\n\n"
            f"👤 Customer: {customer_name}\n"
            f"🆔 Ticket ID: {ticket_id}\n"
            f"⚠️ Current Risk State: {risk_level.upper()}\n"
            f"⏳ Time Left: {int(minutes_left)} Minutes remaining before breach!"
        )

        # 🛠️ FORCED WHATSAPP PREFIX RULE:
        # This guarantees Twilio converts the payload into an internet chat message
        sender = f"whatsapp:{from_phone.replace('whatsapp:', '')}"
        recipient = f"whatsapp:{to_phone.replace('whatsapp:', '')}"

        message = client.messages.create(
            body=message_body,
            from_=sender,
            to=recipient
        )
        print(f"[Twilio WhatsApp Active] Dispatched Notification SID: {message.sid}")
        return True
    except Exception as e:
        print(f"[Twilio Dispatch Error] WhatsApp API Connection Failed: {str(e)}")
        return False