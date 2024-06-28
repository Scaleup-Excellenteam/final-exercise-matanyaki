import requests
from datetime import datetime
from status import Status
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1')
PORT = os.getenv('PORT', '5000')


class GPTExplainerClient:
    def __init__(self):
        self.base_url = f"{BASE_URL}:{PORT}"

    def upload(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            response = requests.post(f'{self.base_url}/upload', files={'file': f})
        if response.status_code == 200:
            return response.json().get('uid')
        else:
            raise Exception(f"Failed to upload file: {response.status_code}, {response.text}")

    def get_status(self, uid: str) -> Status:
        response = requests.get(f'{self.base_url}/status', params={'uid': uid})
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.strptime(data['timestamp'], "%Y%m%d%H%M%S")
            return Status(
                status=data['status'],
                filename=data['filename'],
                timestamp=timestamp,
                explanation=data.get('explanation', None)
            )
        elif response.status_code == 404:
            raise Exception("UID not found")
        else:
            raise Exception(f"Failed to get status: {response.status_code}, {response.text}")

# Example usage:
if __name__ == '__main__':
    client = GPTExplainerClient()

    # Upload a file
    uid = client.upload(r'PutAFile')
    print(f'File uploaded successfully, UID: {uid}')

    # Check the status of the uploaded file
    status = client.get_status(uid)
    print(f'Status: {status.status}')
    print(f'Filename: {status.filename}')
    print(f'Timestamp: {status.timestamp}')
    if status.is_done:
        print(f'Explanation: {status.explanation}')
    else:
        print('File is still being processed.')
