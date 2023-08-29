
from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)
current_progress = 0

@app.route('/')
def index():
    return render_template('simple_index.html')

@app.route('/start-process', methods=['POST'])
def start_process():
    global current_progress
    current_progress = 0
    for _ in range(10):  # Simulating a process that updates the progress in 10 steps
        time.sleep(3)  # Simulating some processing time
        current_progress += 10
    return "Process finished", 200

@app.route('/get-progress', methods=['GET'])
def get_progress():
    global current_progress
    return jsonify({"progress": current_progress})

if __name__ == "__main__":
    app.run(debug=True)
