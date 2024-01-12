import subprocess
import psutil
from pyuac import main_requires_admin


def get_pid_by_service(service_name):
    try:
        # Run the sc queryex command to get information about the service
        result = subprocess.run(['sc', 'queryex', service_name], capture_output=True, text=True, check=True)
        output_lines = result.stdout.split('\n')

        # Find the line containing "PID"
        pid_line = next(line for line in output_lines if 'PID' in line)

        # Extract the PID from the line
        pid_num = int(pid_line.split(':')[1].strip())

        return pid_num
    except Exception as e:
        print(f"Error: {e}")
        return None


@main_requires_admin
def kill_process_by_pid(pid_to_kill):
    try:
        # Get the process by PID
        process = psutil.Process(pid_to_kill)

        # Kill the process
        process.terminate()

        print(f"Process with PID {pid_to_kill} terminated successfully.")
    except Exception as e:
        print(f"Error terminating process with PID {pid_to_kill}: {e}")
