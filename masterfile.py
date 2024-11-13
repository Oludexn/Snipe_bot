import os

# Path to the folder containing your Python scripts
folder_path = '/storage/emulated/0/Python'

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.py'):  # Only .py files
        file_path = os.path.join(folder_path, filename)
        print(f"Running script: {filename}")
        try:
            exec(open(file_path).read())
        except Exception as e:
            print(f"Error running {filename}: {e}")
