import logging
import os

from dotenv import load_dotenv
from openai import AzureOpenAI

from utils import print_token_usage, model_configs

logging.basicConfig(filename='queries.log', encoding='utf-8', level=logging.INFO)

load_dotenv(".env")

# high
model_config = model_configs['low']

with open(0) as file:
    file_content: str = '\n'.join([line.removesuffix('\n').strip() for line in file])

def generate_prompt(system_prompt: str, user_prompt: str) -> str:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15"
    )

    message_text: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model=model_config['text_model'],
        messages=message_text,
        temperature=0.3,
    )

    answer = response.choices[0].message.content
    print_token_usage(system_prompt, user_prompt, answer, model_config)

    return answer


v6 = "You will be given a markdown file with a title, narrative text, examples, and instructions for one or two parts of a daily puzzle. Ignore the puzzle and the examples. Ignore the instructions for solving the puzzles, along with the puzzle answers and the puzzle itself. Only the storyline is important. Your task is to extract the story and tell it in your own words. Describe the visual atmosphere and character actions of the Christmas elves who must solve a puzzle to save Christmas. Highlight the setting, such as a snow-covered village, a bustling workshop, or a magical forest. Detail the elves' appearances and expressions, showing their determination, joy, or frustration. Illustrate key moments like an elf pondering over a clue, teamwork in action, or the celebration of a breakthrough. Include recognizable objects from the story in your description. Avoid mentioning the puzzle's specifics, text, names, or direct speech. Include unique elements like festive decorations, tools used by elves, or special traits of the setting. Keep the description under 200 words, focusing on painting a vivid picture of the story's atmosphere and the elves' journey. Format your response with markdown and use the same titel as given by the user."

v7 = [
    "Given a markdown file containing a Christmas-themed narrative, your task is to creatively retell the story, focusing solely on the narrative elements. Disregard any puzzle-related content, including instructions, examples, and answers.",
    "Concentrate on depicting the visual atmosphere and actions of the Christmas elves involved in the narrative. Vividly describe settings like a snow-covered village, a lively workshop, or an enchanted forest. Characterize the elves in detail, capturing their emotions – be it determination, joy, or frustration – as they engage in their quest.",
    "Illustrate key moments vividly, such as an elf deep in thought, the camaraderie of teamwork, or the exuberance of a pivotal discovery. Include distinctive objects or scenery mentioned in the story, enriching the narrative with festive elements, elf tools, or unique traits of the environment.",
    "Aim for a rich, engaging retelling under 200 words. Avoid specific puzzle details, direct speech, and names. Format your response in markdown, adhering to the original title provided. Let your imagination paint a lively, festive picture of the elves' adventure."
]

v8 = "Transform a Christmas-themed narrative from a markdown file into a compelling short story. Focus on vividly depicting the environment and actions of Christmas elves, while completely omitting any puzzle-related elements such as instructions, examples, and answers.\n" + \
"Your retelling should richly describe scenes such as a snow-covered village, a bustling workshop, or a magical forest, and characterize the elves with attention to their emotions and actions. Highlight key moments like an elf's thoughtful moment, teamwork dynamics, or the joy of a significant discovery. Be sure to include unique aspects of the story, such as festive elements, elf tools, or distinctive environmental features.\n" + \
"The narrative should be engaging, concise (under 200 words), and formatted in markdown, maintaining the original title provided. Avoid including specific puzzle details, direct speech, and character names, and let your creativity vividly bring to life the elves' adventure."


print(generate_prompt('\n'.join(v8), file_content))
