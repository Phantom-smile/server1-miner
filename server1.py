from flask import Flask, request, jsonify
import threading
import time
import os

app = Flask(__name__)

wallet_address = "Not Set"
status = "Starting"
logs = []

def fake_miner():
    global status, logs
    while True:
        time.sleep(5)
        if wallet_address != "Not Set":
            status = "Mining to " + wallet_address
            logs.append(f"Mining round @ {time.strftime('%H:%M:%S')} -> Wallet: {wallet_address}")
        else:
            status = "Idle"
            logs.append(f"Waiting for wallet @ {time.strftime('%H:%M:%S')}")
        if len(logs) > 50:
            logs.pop(0)

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({"status": status})

@app.route("/wallet", methods=["POST"])
def set_wallet():
    global wallet_address
    data = request.get_json()
    wallet_address = data.get("wallet", "Not Set")
    logs.append(f"Wallet updated to {wallet_address}")
    return jsonify({"message": "Wallet updated"})

@app.route("/log", methods=["GET"])
def get_log():
    return jsonify({"log": logs[-10:]})  # Return last 10 log lines

if __name__ == "__main__":
    # Start mining simulation in background
    miner_thread = threading.Thread(target=fake_miner)
    miner_thread.daemon = True
    miner_thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
