import sys
import asyncio
import aiohttp
import SlideExtractor
import OpenAIClient
import JsonHandler
from pptx import Presentation
async def process_presentation(pptx_path : str , api_key : str) -> str:
    presentation = Presentation(pptx_path)
    extractor = SlideExtractor(presentation)
    openai_client = OpenAIClient(api_key)
    json_handler = JsonHandler(pptx_path)
    explanations = []

    async with aiohttp.ClientSession() as session:
        for slide in presentation.slides:
            slide_text = extractor. extract_text_from_slide(slide)
            if slide_text:
                explanation = await openai_client.get_explanation(session, slide_text)
                explanations.append(explanation)

    json_handler.save_explanations(explanations)
    print(f"Explanations saved to {json_handler.get_output_path()}")

    return json_handler.get_output_path()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python -m slides_explainer.main <path_to_pptx> <openai_api_key>")
        sys.exit(1)

    pptx_path = sys.argv[1]
    api_key = sys.argv[2]

    saved_json_path = asyncio.run(process_presentation(pptx_path, api_key))
    print(f"Saved JSON file path: {saved_json_path}")