import os
import subprocess

def is_render_environment():
    return os.path.exists("/opt/render/project/src")

# Set folder_path based on the environment
if is_render_environment():
    # Render environment path
    folder_path = "/opt/render/project/src/Snipe_bot"
else:
    # Local Android path
    folder_path = "/storage/emulated/0/Python/Snipe_bot"

# Check if the folder_path exists
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

# Run each .py file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith(".py") and filename != "masterfile.py":  # Exclude the master file itself
        file_path = os.path.join(folder_path, filename)
        print(f"Running {filename}...")
        # Run the Python file using subprocess
        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        print(f"Output of {filename}:\n{result.stdout}")
        if result.stderr:
            print(f"Errors in {filename}:\n{result.stderr}")
