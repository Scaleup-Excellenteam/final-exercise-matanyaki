import json
from pathlib import Path

class JsonHandler:
    def __init__(self , pptx_path : str):
        self.output_path = Path(pptx_path).with_suffix('.json')

    def save_explanations(self, explanations : list):
        slide_numbers = range(1, len(explanations) + 1)  # Slide numbers start from 1
        data = {"Slide no." +str(slide_num): explanation for slide_num, explanation in zip(slide_numbers, explanations)} # Creating JSON data format
        with open(self.output_path, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def get_output_path(self) -> str:
        return str(self.output_path)