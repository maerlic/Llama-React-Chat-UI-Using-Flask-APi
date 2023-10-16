# Import necessary modules
from flask import Flask
import subprocess
from flask_cors import CORS  # Import the CORS package

# Initialize Flask app
app = Flask(__name__)

CORS(app)  # Enable CORS for your Flask app and specify allowed origins

# Function to run the desired code
def run_desired_code():
    command = "torchrun --nproc_per_node 1 ../../chat.py --ckpt_dir ../../llama-2-7b-chat/ --tokenizer_path ../../tokenizer.model --max_seq_len 512 --max_batch_size 4"
    command_args = command.split()
    
    try:
        subprocess.run(command_args, check=True)
    except subprocess.CalledProcessError as e:
        print("Error: Command failed to execute.")

# Endpoint to trigger running the code
@app.route('/run_code', methods=['GET'])
def trigger_code_run():
    run_desired_code()
    return "Code execution triggered."

# Run the API
if __name__ == '__main__':
    app.run(host="localhost", port=8025, debug=True)
