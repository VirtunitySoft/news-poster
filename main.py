import webview
from enum import Enum
import env
import db
import re
import mailer

class DataType(Enum):
    RECEIVER = 0
    SENDER = 1
    SUPA = 2

class Api:

    def setup(self):
        # Load environment variables
        env.load(".env")
        db.load(env.get("SUPABASE_URL"), env.get("SUPABASE_SERVICE_ROLE_KEY"))
        mailer.load("smtp.gmail.com", 465)

        self.displayData(DataType.SUPA)
        self.displayData(DataType.RECEIVER)
        self.displayData(DataType.SENDER)
        print("🔧 API setup complete. Environment variables and database loaded.")

    def on_supa_config_changed(self, supaBaseKey, supaBaseUrl):
        db.load(supaBaseUrl, supaBaseKey)
        self.displayData(DataType.RECEIVER)
        print(f"🔧 Supabase configuration loaded: URL")

    def send_email(self, sender, password, receivers, subject, html_body):
        print(f"📧 Attempting to send email from: {sender}")
        print(f"📧 To: {receivers}")
        print(f"📧 Subject: {subject}")
        
        validation_errors = []
        row_num = 1

        # Validate email addresses
        for receiver in receivers:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", receiver):
                validation_errors.append(f"Row {row_num}: Invalid email format")
                print(f"❌ Validation Error: Row {row_num}: Invalid email format - {receiver}")
            row_num += 1

        # Validate subject
        if not subject.strip():
            validation_errors.append("Subject cannot be empty")
            print("❌ Validation Error: Subject cannot be empty")

        if validation_errors:
            print("❌ Validation failed, not sending email")
            return {"success": False, "errors": validation_errors}

        # Send email using the mailer module
        if (mailer.email(sender, password, receivers, subject, html_body)):
            print("✅ Email sent successfully!")
            return {"success": True, "message": "Email sent successfully!"}
        print("❌ Error sending email:")
        return {"success": False, "message": "Email sent unsuccessfully!"}
    
    def save_data(self, supaBaseKey, supaBaseUrl, sender, password):
        print(f"💾 Saving data...")
        if supaBaseKey or supaBaseUrl:
            # Save Supabase credentials
            env.set("SUPABASE_URL", supaBaseUrl)
            env.set("SUPABASE_SERVICE_ROLE_KEY", supaBaseKey)

        elif sender or password:
            # Save SENDER credentials
            if not re.match(r"[^@]+@[^@]+\.[^@]+", sender):
                print("❌ Invalid email format for sender")
                return None
            env.set("SENDER_EMAIL_ADDRESS", sender)
            env.set("SENDER_EMAIL_PASSWORD", password)

        print("✅ Credentials saved successfully!")
        return {"success": True, "message": "Data saved successfully!"}
    
    def displayData(self, enum):
        if enum == DataType.SUPA:
            # Display Supabase credentials
            js_code = f"displayData('{DataType.SUPA.value}', '{env.get("SUPABASE_URL")}', '{env.get("SUPABASE_SERVICE_ROLE_KEY")}')"
            window.evaluate_js(js_code)
        elif enum == DataType.SENDER:
            # Display SENDER credentials
            js_code = f"displayData('{DataType.SENDER.value}', '{env.get("SENDER_EMAIL_ADDRESS")}', '{env.get("SENDER_EMAIL_PASSWORD")}')"
            window.evaluate_js(js_code)
        elif enum == DataType.RECEIVER:
            # Display receiver emails
            emails = db.get_email()
            if emails:
                for email in emails:
                    js_code = f"displayData('{DataType.RECEIVER.value}', '{email}', '{None}')"
                    window.evaluate_js(js_code)
            else:
                print("❌ No emails found in the database")
        else:
            print("❌ Unknown enum value")

# Pass the window into the API instance
api = Api()
window = webview.create_window("Virtunity News-Sender", "ui/editor.html", js_api=api, width=800, height=600)

    # Run after the window loads
def on_loaded():
    api.setup()
    window.expose(api.save_data)
    window.expose(api.send_email)
    window.expose(api.on_supa_config_changed)

webview.start(on_loaded)