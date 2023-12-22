import re
import json

from utils import print_token_usage, model_configs, client


model_config: dict = model_configs['high']

model_config['with_description'] = False
model_config['with_emoji_list'] = False


###
### Erstellt mit:
### < emoji-unicode.txt sed -Ee '/^#|^$/d ; s/\s+;\s+(minimally-qualified|fully-qualified|unqualified|component)\s+#([^E]+)\sE[0-9\.]+/\2/1' >| emoji-unicode.sed.txt
with open('var/emoji-unicode.sed.txt') as file:
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

with open('var/github-emojis.json') as file:
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


def create_system_prompt() -> str:
    system_prompt: str = ""
    if model_config['with_emoji_list']:
        system_prompt += "You will be given a story description and you will respond with up to 10 emojis that are representative of the story. Your answer should not contain anything else but the emojis. Each emoji is represented like this :emoji_name:. "

        if model_config['with_description']:
            system_prompt += "The following is a list of emojis you can choose from, followed by a short description.\n"
        else:
            system_prompt += "The following is a list of emojis you can choose from:\n"

        system_prompt += '\n'.join(descriptions)

        system_prompt += '\nRemember to only answer with up to 10 representative emojis, separated by a single whitespace.'
    else:
        system_prompt += "Based on a brief description of a story, provide a set of up to 10 emojis that capture the main plot elements. Ensure that the emojis are supported by GitHub Markdown. When the story's description does not specify certain details, aim for a diverse representation in your emoji choices. For example, use :elf_woman: instead of the more generic :elf:, or :couple_with_heart_man_man: instead of the broader :couple_with_heart:, where appropriate. Focus on capturing significant events, settings, or unique aspects of the narrative in a way that allows someone familiar with the story to recognize it. Remember, no text or explanations should be included, only the emojis that best convey the story's core plot points in a diverse and inclusive manner."

    return system_prompt

def generate_prompt(system_prompt: str, user_prompt: str) -> str:
    message_text: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model=model_config['text_model'],
        messages=message_text,
        temperature=0.4,
        max_tokens=100
    )

    answer = response.choices[0].message.content
    print_token_usage(system_prompt, user_prompt, answer, model_config)

    print('{}'.format(answer))
    return answer

def check_answer(answer: str) -> str:
    correct = []
    missing = []
    for m in re.findall(r':([a-z0-9_-]+):', answer):
        if github_emojis.get(m):
            correct.append(":"+m+":")
        else:
            missing.append(m)
    if len(missing) > 0:
        print(f"GitHub is missing {len(missing)}/{len(correct)} emojis: {missing}")

    return ' '.join(correct)


def emojify_str(text: str) -> str:
    for m in re.findall(r':([a-z0-9_-]+):', text):
        if github_emojis.get(m) and unicode_symbols.get(github_emojis[m]):
            text = text.replace(f":{m}:", unicode_symbols[github_emojis[m]])
    return text


with open(0) as stdin:
    story = '\n'.join(stdin.readlines())

answer = generate_prompt(create_system_prompt(), story)

answer = check_answer(answer)
print(answer)
print(emojify_str(answer))
