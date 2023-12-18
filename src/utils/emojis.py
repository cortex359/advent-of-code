import re
import json
import os
import sys

from dotenv import load_dotenv
from openai import AzureOpenAI
import tiktoken
from utils import num_token_from_string

load_dotenv(".env")

model_config: dict = {
    'text_model': 'gpt-35-turbo-1106',
    'pricing': 0.003,
    'with_description': False
}
# model_config: dict = {
#    'text_model': 'gpt-4-turbo',
#    'pricing': 0.010,
#    'with_description': False
# }


###
### Erstellt mit:
### < emoji-unicode.txt sed -Ee '/^#|^$/d ; s/\s+;\s+(minimally-qualified|fully-qualified|unqualified|component)\s+#([^E]+)\sE[0-9\.]+/\2/1' >| emoji-unicode.sed.txt
with open('ext/emoji-unicode.sed.txt') as file:
    data: list[str] = [line.removesuffix("\n") for line in file]

unicode_cldr: dict[str, str] = {}
unicode_symbols: dict[str, str] = {}
for line in data:
    code_point = ""
    for s in re.findall('[0-9A-Z]{3,5}', line):
        if len(code_point) == 0:
            code_point = s.lower()
        else:
            code_point += '-' + s.lower()
    emoji_symbol = line[len(code_point):len(code_point) + 3]
    description = line[len(code_point) + 2:].strip()
    unicode_cldr[code_point] = description
    unicode_symbols[code_point] = emoji_symbol

with open('ext/github-emojis.json') as file:
    github_emojis: dict[str, str] = json.load(file)

descriptions: list[str] = []
for k, url in github_emojis.items():
    match = re.match(r'^.*/emoji/(unicode/([0-9a-f-]+)|([^\.]+))\.png.*$', url)
    if match:
        code_point = match.group(2)
    else:
        continue
    github_emojis[k] = code_point
    if model_config['with_description']:
        descriptions.append(f":{k}: {unicode_cldr.get(code_point, k)}")
    else:
        descriptions.append(f":{k}:")


def generate_prompt(descriptions: list[str], user_prompt: str) -> str:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15"
    )

    system_prompt = "You are a simple and helpful AI. You will be given a story description and you will respond with up to six emojis that are representative of the story. Your answer should not contain anything else but the emojis. Each emoji is represented like this :emoji_name:. "
    if model_config['with_description']:
        system_prompt += "The following is a list of emojis you can choose from, followed by a short description.\n"
        system_prompt += '\n'.join(descriptions)
    else:
        system_prompt += "The following is a list of emojis you can choose from:\n"
        system_prompt += ' '.join(descriptions)

    system_prompt += '\nRemember to only answer with up to six representative emojis, separated by a single whitespace.'

    message_text: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    system_token = num_token_from_string(system_prompt)
    user_token = num_token_from_string(user_prompt)
    print(f"System: {system_token} token")
    print(f"User: {user_token} token")
    print(
        f"Total: {system_token + user_token} token at {model_config['pricing']:.4f} €/1kToken ({model_config['text_model']}) -> {(system_token + user_token) / 1000 * model_config['pricing']:4.2f} €")

    response = client.chat.completions.create(
        model=model_config['text_model'],
        messages=message_text,
        temperature=0.3,
        # max_tokens=800
    )

    answer = response.choices[0].message.content
    print('{}'.format(answer))
    return answer


def test_answer(answer: str) -> bool:
    emojis = 0
    correct = 0
    for m in re.findall(r':([a-z0-9_-]+):', answer):
        emojis += 1
        if github_emojis.get(m):
            correct += 1
        else:
            print(f"github is missing {m}")
    print(f"{correct} / {emojis}")


def emojify_str(text: str) -> str:
    for m in re.findall(r':([a-z0-9_-]+):', text):
        if github_emojis.get(m):
            text = text.replace(f":{m}:", unicode_symbols[github_emojis[m]])
    return text


with open(0) as stdin:
    story = '\n'.join(stdin.readlines())

answer = generate_prompt(descriptions, story)

test_answer(answer)
print(emojify_str(answer))
