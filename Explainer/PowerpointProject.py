import os
import time
import asyncio
import sys
from SlideExtractor import SlideExtractor
from OpenAIClient import OpenAIClient
from JsonHandler import JsonHandler
from pptx import Presentation
import logging
from logging.handlers import TimedRotatingFileHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(BASE_DIR, 'outputs'))


# Create log directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs', 'explainer')
os.makedirs(log_dir, exist_ok=True)

# Set up Explainer logging
handler = TimedRotatingFileHandler(
    os.path.join(log_dir, 'explainer.log'),
    when='midnight',
    interval=1,
    backupCount=5
)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('explainer')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

PROCESSED_FILES = set()  # To keep track of processed files

def is_pptx_file(filename):
    return filename.endswith(".pptx") or ".pptx_" in filename
async def process_presentation(pptx_path : str , uid :str) -> str:
    try:
        #Initialization
        presentation = Presentation(pptx_path)
        extractor = SlideExtractor()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            return
        openai_client = OpenAIClient(openai_api_key)
        json_handler = JsonHandler(pptx_path ,uid)
        explanations = []

        #Sending slide by slide to the api using async function to preform better run time
        for slide in presentation.slides:
            slide_text = extractor.extract_text_from_slide(slide)
            if slide_text:
                explanation = await openai_client.get_explanation(slide_text)
                explanations.append(explanation)

        #Creating JSON file
        json_handler.save_explanations(explanations)

        logger.info(f"Processed file: {pptx_path}, saved JSON path: {json_handler.get_output_path()}")

        return json_handler.get_output_path()

    except FileNotFoundError:
        logger.error(f"File not found: {pptx_path}")
        return
    except Exception as e:
        logger.error(f"Error processing file: {pptx_path}, error: {e}")
        return


async def process_files_in_directory():
    while True:
        logger.info("Checking for new files...")
        print("Checking for new files...")
        for file_name in os.listdir(UPLOAD_FOLDER):
            if is_pptx_file(file_name) and file_name not in PROCESSED_FILES:
                pptx_path = os.path.join(UPLOAD_FOLDER, file_name)
                uid = file_name.split('_')[-1]
                logger.info(f"Processing file: {pptx_path}")

                # Process the presentation file
                saved_json_path = await process_presentation(pptx_path , uid)

                if saved_json_path:
                    # Move the processed file to the output folder
                    output_path = os.path.join(OUTPUT_FOLDER, file_name)
                    os.rename(pptx_path, output_path)
                    logger.info(f"Saved JSON file path: {saved_json_path}")
                    PROCESSED_FILES.add(file_name)
                else:
                    logger.info(f"Failed to process file: {pptx_path}")

        # Sleep for a few seconds before checking again
        time.sleep(10)

if __name__ == '__main__':
    # Ensure the folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    #Add to mange Event loop error(Windows common error)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(process_files_in_directory())
