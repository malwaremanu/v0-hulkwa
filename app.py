from flask import Flask, jsonify, request
import secrets

app = Flask(__name__)

# Keep the original minimalist root route
@app.get("/")
def root():
    return jsonify({"msg": "ok"})

# --- In-memory database to store state (ported from FastAPI example) ---
db = {
    "reports": {},
    "contacts": {}
}

# Quick replies (ported)
@app.get("/quickreply")
def get_quick_replies():
    return jsonify([])

# Validate user (ported)
@app.post("/validateuser")
def validate_user():
    data = request.get_json(silent=True) or {}
    user_name = data.get("userName", "")
    # phoneNumber present in the original model but not strictly needed here
    return jsonify({
        "isAuthorized": True,
        "hasPermission": True,
        "isPaid": True,
        "availableMsgs": 100000,
        "availableContacts": 100000,
        "trialUser": False,
        "firstName": user_name,
        "lastName": "Baap Tera",
        "usedSpreadsheets": [],
        "planType": "Premium",
        "extensionUpgradeBtn": {
            "text": "",
            "defaultText": ""
        },
        "serverNotification": {},
        "settings": {
            "timeGap": 3
        },
        "addPoweredByMsg": False
    })

# Custom templates (ported)
@app.get("/custom_templates")
def get_custom_templates():
    return jsonify({
        "templates": [
            {
                "_id": "23423424",
                "name": "Good Morning",
                "message": "Good Morning Sir / Madam",
            }
        ]
    })

# Create message report (ported)
@app.post("/create-msg-report")
def create_message_report():
    data = request.get_json(silent=True) or {}
    campaign_name = data.get("campaignName", "")
    common_message = data.get("commonMessage", "")
    report_id = secrets.token_hex(12)

    db["reports"][report_id] = {
        "name": campaign_name,
        "message": common_message,
        "status": "pending",
        "contacts": []
    }

    return jsonify({
        "reportId": report_id,
        "availableMsgs": 100000,
        "unSubscribedNumbers": []
    })

# Upload contact list (ported)
@app.post("/upload-contact-list")
def upload_contact_list():
    data = request.get_json(silent=True) or {}
    report_id = data.get("reportId")
    contact_list = data.get("contactList", [])

    if not report_id or report_id not in db["reports"]:
        return jsonify({"detail": "Report ID not found"}), 404

    db["reports"][report_id]["contacts"] = contact_list
    db["contacts"][report_id] = list(contact_list)

    return jsonify({"message": "Contacts inserted successfully"})

# Update message report (ported)
@app.post("/update-msg-report")
def update_message_report():
    data = request.get_json(silent=True) or {}
    report_id = data.get("reportId")
    status_data = data.get("statusData", [])

    if not report_id or report_id not in db["reports"]:
        return jsonify({"detail": "Report ID not found"}), 404

    # Simulate successful status update
    contacts = db["contacts"].get(report_id, [])
    for status_update in status_data:
        index = status_update.get("index")
        if isinstance(index, int) and 0 <= index < len(contacts):
            contacts[index]["status"] = "Success"

    db["reports"][report_id]["status"] = "completed"
    return jsonify({"message": "Message report updated successfully"})
