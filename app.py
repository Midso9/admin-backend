from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ADMIN_CODE = "13794680"

orders = []
maintenance = False

@app.route("/")
def home():
    return {"status":"online"}

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    orders.append({
        "id": len(orders)+1,
        "plan": data.get("plan"),
        "text": data.get("text"),
        "reply": None,
        "pdf": None
    })
    return {"ok":True}

@app.route("/orders")
def get_orders():
    return jsonify(orders)

@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    for o in orders:
        if o["id"] == data["id"]:
            o["reply"] = data.get("reply")
            o["pdf"] = data.get("pdf")
    return {"ok":True}

@app.route("/maintenance", methods=["POST"])
def maint():
    global maintenance
    if request.json.get("code") != ADMIN_CODE:
        return {"error":"no"}

    maintenance = not maintenance
    return {"maintenance": maintenance}

@app.route("/status")
def status():
    return {"maintenance": maintenance}

@app.route("/login", methods=["POST"])
def login():
    if request.json.get("code") == ADMIN_CODE:
        return {"token":"ok"}
    return {"error":"no"}

app.run(host="0.0.0.0", port=5000)
