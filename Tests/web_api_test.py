import os
import pytest
import requests
import subprocess
import time
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure the paths to include the directories
sys.path.insert(0, os.path.join(BASE_DIR, 'Config'))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1')
PORT = os.getenv('PORT', '5000')

def test_upload_file(start_web_api, setup_upload_folder):
    files = {'file': open('C:/Users/Asus/Downloads/Samplepptx.pptx', 'rb')}
    response = requests.post(f'{BASE_URL}:{PORT}/upload', files=files)
    assert response.status_code == 200
    response_data = response.json()
    assert 'uid' in response_data

    uid = response_data['uid']
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    assert any(uid in filename for filename in uploaded_files)

def test_check_status_pending(start_web_api, setup_upload_folder):
    files = {'file': open('C:/Users/Asus/Downloads/Samplepptx.pptx', 'rb')}
    response = requests.post(f'{BASE_URL}:{PORT}/upload', files=files)
    uid = response.json().get('uid')

    response = requests.get(f'{BASE_URL}:{PORT}/status', params={'uid': uid})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'pending'
