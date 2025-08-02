from flask import Flask, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)
miner_process = None

def start_mining(wallet):
    global miner_process

    stop_mining()

    print(f"[+] Starting mining for wallet: {wallet}")
    miner_process = subprocess.Popen([
        "./cpuminer",  # Make sure the cpuminer binary is executable and named correctly
        "-a", "sha256d",
        "-o", "stratum+tcp://stratum.slushpool.com:3333",  # Use a public pool or your own
        "-u", wallet
    ])

def stop_mining():
    global miner_process

    if miner_process:
        print("[!] Stopping current miner process.")
        miner_process.terminate()
        try:
            miner_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            miner_process.kill()
        miner_process = None

@app.route("/")
def status():
    wallet = get_current_wallet()
    return f"Server is running. Mining to: {wallet if wallet else 'Not set'}"

@app.route("/set_wallet", methods=["POST"])
def set_wallet():
    data = request.get_json()
    wallet = data.get("wallet")

    if not wallet:
        return jsonify({"error": "No wallet provided"}), 400

    with open("wallet.txt", "w") as f:
        f.write(wallet)

    start_mining(wallet)
    return jsonify({"message": "Wallet updated and mining started."})

def get_current_wallet():
    if os.path.exists("wallet.txt"):
        with open("wallet.txt", "r") as f:
            return f.read().strip()
    return None

if __name__ == "__main__":
    wallet = get_current_wallet()
    if wallet:
        start_mining(wallet)
    app.run(host="0.0.0.0", port=10000)
