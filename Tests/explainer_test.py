import pytest
import time
import os
import shutil
import sys

# Get the absolute path of the Week4 directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ensure the paths to include the directories
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'final-exercise-matanyaki', 'Config'))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(BASE_DIR, 'outputs'))

def test_explainer_processes_files(start_explainer, setup_upload_folder, setup_output_folder):
    # Place a sample file in the uploads folder
    sample_file_path = 'C:/Users/Asus/Downloads/Samplepptx.pptx'
    destination = os.path.join(UPLOAD_FOLDER, 'Samplepptx.pptx')
    shutil.copy(sample_file_path, destination)  # Use shutil.copy instead of os.copy

    time.sleep(15)  # Wait for the explainer to process the file

    processed_files = os.listdir(OUTPUT_FOLDER)
    assert len(processed_files) > 0
