import json
from pathlib import Path

class JsonHandler:
    def __init__(self , pptx_path : str):
        self.output_path = Path(pptx_path).with_suffix('.json')

    def save_explanations(self, explanations : list):
        with open(self.output_path, 'w') as output_file:
            json.dump(explanations, output_file, indent=4)

    def get_output_path(self) -> str:
        return str(self.output_path)