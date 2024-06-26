import json
from pathlib import Path
import sys
import os

# Update sys.path to reflect the new structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(BASE_DIR, 'outputs'))


class JsonHandler:
    def __init__(self , pptx_path : str, uid :str):
        base_name = Path(pptx_path).stem
        json_filename = f"{base_name}_{uid}.json"
        self.output_path = Path(OUTPUT_FOLDER) / json_filename


    def save_explanations(self, explanations : list):
        slide_numbers = range(1, len(explanations) + 1)  # Slide numbers start from 1
        data = {"Slide no." +str(slide_num): explanation for slide_num, explanation in zip(slide_numbers, explanations)} # Creating JSON data format
        with open(self.output_path, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def get_output_path(self) -> str:
        return str(self.output_path)