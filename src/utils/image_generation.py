# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import logging
import os
import shutil
import sys

import requests
from dotenv import load_dotenv
import openai
from openai import AzureOpenAI
import json

logging.basicConfig(filename='queries.log', encoding='utf-8', level=logging.INFO)

load_dotenv(".env")

# high
performance_settings: dict = {
    'size': '1792x1024',
    'quality': 'hd',
    'text_model': 'gpt-4-turbo',
}
# low
performance_settings: dict = {
    'size': '1024x1024',
    'quality': 'standard',
    'text_model': 'gpt-35-turbo-1106',
}

performance_settings: dict = {
    'size': '1792x1024',
    'quality': 'standard',
    'text_model': 'gpt-35-turbo-1106',
}

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15"
    #api_version="2023-12-01-preview"
)

file = sys.argv[1]
if not os.path.isfile(file):
    logging.error("File not found")
    exit(1)


folder = file.removesuffix("puzzle.md")

with open(file) as file:
    file_content: str = ' '.join([line.removesuffix('\n').strip() for line in file])


v1 = "You will be given a file with a puzzle and a story about Christmas elf who have to solve it in order to safe Christmas. Visually describe a single, remarkable scene from that story. The description should be epic but not too long. Do not describe the puzzle itself. Describe the scene that is happening around the elfs. Describe what the elfs are doing and the challenge they are facing. Do not describe any text or names and do not use direct or indirect speech. Focus on the visual appearance. Make sure that you use the word 'Christmas' in your description. Make clear, that the scene is fictional. Focus on key elements of the scene. Do not violate DALLE-3 content guidelines. Keep it under 800 characters."

v2 = "You will be given a file with a puzzle and a story about Christmas elves who have to solve the puzzle in order to save Christmas. Visually describe one remarkable scene from that story. Include recognizable objects from the story in your description. Do not describe any text or names, and do not use direct or indirect speech. Keep it under 800 characters."

v3 = "Create an image of a [general subject or theme], focusing on [specific elements or characteristics]. The scene should be set in [type of environment or setting], and include [specific objects, creatures, or characters, ensuring diversity and inclusivity where applicable]. The overall mood of the image should be [describe the mood or atmosphere], with colors that are [describe the color palette]. Ensure that the image is imaginative and vibrant, without depicting any sensitive or prohibited content."

v4 = "You will be given a file with a puzzle and a story about Christmas elves who have to solve the puzzle in order to save Christmas. Summarize the story, but do not describe the puzzle itself.  Visually describe a remarkable scene from that story. Include recognizable objects from the story in your description. Do not describe any text or names, and do not include direct speech. Focus on specific key elements from the story.  Keep it under 800 characters."

v5 = "You will be given a file with a puzzle and a story about Christmas elves who have to solve the puzzle in order to save Christmas. Summarize the story, but do not describe the puzzle itself.  Visually describe remarkable aspects from that story. Include recognizable objects from the story in your description. Do not describe any text or names, and do not include direct speech. Focus on specific key elements from the story.  Keep it under 800 characters."


message_text: list[dict] = [
    {"role": "system", "content": v5},
    {"role": "user", "content": file_content}
]

response = client.chat.completions.create(
    model=performance_settings['text_model'],
    messages=message_text,
    temperature=0.5,
    #max_tokens=800,
    #top_p=0.95,
    #frequency_penalty=0,
    #presence_penalty=0,
    #stop=None
)

#pre_prompt = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:\n"
pre_prompt = "Generate a image from the following description. Do not display text, letters or words. Ensure that the image is imaginative and vibrant, without depicting any sensitive or prohibited content. Description: "

scene_description = response.choices[0].message.content

combined_prompt = pre_prompt + scene_description
print('Länge des kombinierten Prompts = {}'.format(len(combined_prompt)))
print('Scene Description: {}'.format(scene_description))
logging.info("Send prompt: " + combined_prompt)

dalle_endpoint = os.getenv("AZURE_ENDPOINT") + "openai/deployments/Dalle3/images/generations?api-version=2023-06-01-preview"

dalle_client = AzureOpenAI(
    api_version="2023-12-01-preview",
    azure_endpoint=dalle_endpoint,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

try:
    result = dalle_client.images.generate(
        model="dall-e-3",
        prompt=combined_prompt,
        size=performance_settings['size'],
        quality=performance_settings['quality'],
        style="vivid"
    )
    result_data = json.loads(result.model_dump_json())['data'][0]
    revised_prompt = result_data['revised_prompt']
    print('Revised Prompt: {}'.format(revised_prompt))
    logging.info("Revised Promped: " + revised_prompt)

except openai.OpenAIError as e:
    print(e.http_status)
    print(e.error)
    exit(1)


def get_next_free_filename(folder: str, prefix:str = "img_", suffix: str = ".png") -> str:
    for i in range(1, 100):
        image_savepath = '{}{}{:02d}{}'.format(folder, prefix, i, suffix)
        if not os.path.isfile(image_savepath):
            break
    return image_savepath


def download_and_save_img(folder: str, image_url: str):
    res = requests.get(image_url, stream=True)
    image_save_path = get_next_free_filename(folder)
    logging.info("Save image to: " + image_save_path)
    if res.status_code == 200:
        with open(image_save_path, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', image_save_path)
    else:
        print('Image Couldn\'t be retrieved')


download_and_save_img(folder, result_data['url'])