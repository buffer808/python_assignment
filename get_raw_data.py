import subprocess

# Command to execute
command = "./financial/manage.py get_raw_data"

# Execute the command
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output
print(result.stdout)