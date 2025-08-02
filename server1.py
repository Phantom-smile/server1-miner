from flask import Flask, request, jsonify

app = Flask(__name__)

running = False
wallet = ""
user = ""

@app.route("/")
def home():
    return "Server is running."

@app.route("/start-mining", methods=["POST"])
def start_mining():
    global running, wallet, user
    data = request.get_json()
    wallet = data.get("wallet")
    user = data.get("username")
    pw = data.get("password")
    
    if user != "admin" or pw != "402393":
        return jsonify({"status": "unauthorized"}), 403

    running = True
    return jsonify({"status": "mining_started", "wallet": wallet})

@app.route("/stop-mining", methods=["POST"])
def stop_mining():
    global running
    running = False
    return jsonify({"status": "mining_stopped"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "running" if running else "stopped",
        "wallet": wallet,
        "user": user
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
