import subprocess
import time
import os
import sys
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Client')))

from client import GPTExplainerClient

def start_process(command):
    """Starts a subprocess and returns the process handle."""
    process = subprocess.Popen(command, shell=True)
    return process

def stop_process(process):
    """Stops a subprocess."""
    process.terminate()
    process.wait()

def main():
    # Paths to the scripts
    web_api_path = os.path.join(os.path.dirname(__file__), '..','Web-API', 'app.py')
    explainer_path = os.path.join(os.path.dirname(__file__),'..' ,'Explainer','PowerpointProject.py')

    # Start the Web API
    print("Starting the Web API...")
    web_api_process = start_process(f'python {web_api_path}')
    time.sleep(5)  # Wait for the server to start

    # Start the Explainer
    print("Starting the Explainer...")
    explainer_process = start_process(f'python {explainer_path}')
    time.sleep(5)  # Wait for the explainer to start

    # Initialize the client
    client = GPTExplainerClient()

    # Path to your sample presentation file
    sample_pptx_path = 'C:/Users/Asus/Downloads/Samplepptx.pptx'

    try:
        # Step 1: Upload a file
        print("Uploading the sample presentation...")
        uid = client.upload(sample_pptx_path)
        print(f'File uploaded successfully, UID: {uid}')

        # Step 2: Check the status of the uploaded file
        print("Checking the status of the uploaded file...")
        while True:
            status = client.get_status(uid)
            print(f'Status: {status.status}')
            print(f'Filename: {status.filename}')
            print(f'Timestamp: {status.timestamp}')
            if status.is_done:
                print(f'Explanation: {status.explanation}')
                break
            else:
                print('File is still being processed. Waiting for 10 seconds...')
                time.sleep(10)

    finally:
        # Stop the processes
        print("Stopping the Web API and Explainer...")
        stop_process(web_api_process)
        stop_process(explainer_process)
        print("System test completed.")

if __name__ == '__main__':
    main()
