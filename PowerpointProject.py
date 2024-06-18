import os
import asyncio
import sys
from SlideExtractor import SlideExtractor
from OpenAIClient import OpenAIClient
from JsonHandler import JsonHandler
from pptx import Presentation

async def process_presentation(pptx_path : str) -> str:
    try:
        #Initialization
        presentation = Presentation(pptx_path)
        extractor = SlideExtractor()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            return
        openai_client = OpenAIClient(openai_api_key)
        json_handler = JsonHandler(pptx_path)
        explanations = []

        #Sending slide by slide to the api using async function to preform better run time
        for slide in presentation.slides:
            slide_text = extractor.extract_text_from_slide(slide)
            if slide_text:
                explanation = await openai_client.get_explanation(slide_text)
                explanations.append(explanation)

        #Creating JSON file
        json_handler.save_explanations(explanations)

        return json_handler.get_output_path()

    except FileNotFoundError:
        print(f"Error: File '{pptx_path}' not found.")
        return
    except Exception as e:
        print(f"Error opening PowerPoint file: {e}")
        return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python -m slides_explainer.main <path_to_pptx>")
        sys.exit(1)

    #Takes path from Configurations
    pptx_path = sys.argv[1]

    #Add to mange Event loop error(Windows common error)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    saved_json_path = asyncio.run(process_presentation(pptx_path))

    print(f"Saved JSON file path: {saved_json_path}")