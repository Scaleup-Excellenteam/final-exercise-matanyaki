import pytest
import os
import sys


# Get the absolute path of the Week4 directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure the paths to include the directories
sys.path.insert(0, os.path.join(BASE_DIR, 'Client'))
sys.path.insert(0, os.path.join(BASE_DIR, 'Config'))

from client import GPTExplainerClient
def test_upload_file(start_web_api, setup_upload_folder, client):
    uid = client.upload('C:/Users/Asus/Downloads/Samplepptx.pptx')
    assert uid is not None

def test_check_status_pending(start_web_api, setup_upload_folder, client):
    uid = client.upload('C:/Users/Asus/Downloads/Samplepptx.pptx')
    response = client.get_status(uid)
    assert response.status == 'pending'
    assert response.filename == 'Samplepptx.pptx'