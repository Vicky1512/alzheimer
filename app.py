# app.py (Python Backend)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/start-recording', methods=['POST'])
def start_recording():
    # *** YOUR PYTHON LOGIC TO START RECORDING GOES HERE ***
    print("Backend received START command.")
    return jsonify({"status": "Recording started successfully"}), 200

@app.route('/api/stop-recording', methods=['POST'])
def stop_recording():
    # *** YOUR PYTHON LOGIC TO STOP RECORDING GOES HERE ***
    print("Backend received STOP command.")
    return jsonify({"status": "Recording stopped successfully"}), 200

if __name__ == '__main__':
    # Run the server on port 5000 (standard for Flask)
    app.run(debug=True, port=5000)
