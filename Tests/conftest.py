import pytest
import subprocess
import time
import os
import sys

# Get the absolute path of the Week4 directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ensure the paths to include the directories
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'final-exercise-matanyaki', 'Client'))
sys.path.append(os.path.join(BASE_DIR, 'final-exercise-matanyaki', 'Config'))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(BASE_DIR, 'outputs'))

from client import GPTExplainerClient

@pytest.fixture(scope='session')
def start_web_api():
    process = subprocess.Popen(['python', os.path.join(BASE_DIR, 'final-exercise-matanyaki', 'Web-API', 'app.py')])
    time.sleep(3)  # Give the server some time to start
    yield
    process.terminate()

@pytest.fixture(scope='session')
def start_explainer():
    explainer_path = os.path.join(BASE_DIR, 'final-exercise-matanyaki', 'Explainer', 'PowerPointProject.py')
    process = subprocess.Popen(['python', explainer_path])
    time.sleep(3)  # Give the script some time to start
    yield
    process.terminate()

@pytest.fixture(scope='module')
def client():
    return GPTExplainerClient()

@pytest.fixture
def setup_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    yield
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

@pytest.fixture
def setup_output_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    yield
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))
