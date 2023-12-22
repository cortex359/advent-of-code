import tiktoken
import os

from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv(".env")


def num_token_from_string(string: str, encoding_name: str = 'cl100k_base') -> int:
    """Returns the number of tokens in a text string."""
    # | Encoding name       | OpenAI models                                    |
    # |---------------------|--------------------------------------------------|
    # | cl100k_base         | gpt-4, gpt-3.5-turbo, text-embedding-ada-002     |
    # | p50k_base           | Codex models, text-davinci-002, text-davinci-003 |
    # | r50k_base (or gpt2) | GPT-3 models like davinci                        |
    # |---------------------|--------------------------------------------------|
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def print_token_usage(system_prompt: str, user_prompt: str, answer: str, model_config: dict):
    system_token = num_token_from_string(system_prompt)
    user_token = num_token_from_string(user_prompt)
    answer_token = num_token_from_string(answer)
    in_price = (system_token + user_token)/1000. * model_config['prompt_pricing'] * 1000
    out_price = answer_token/1000. * model_config['completion_pricing'] * 1000

    total_token = system_token + user_token + answer_token
    print(f"System + User Prompt: {system_token}+{user_token} = {system_token + user_token} token for {in_price:4.4f} m€")
    print(f"Answer: {answer_token} token for {out_price:4.4f} m€")
    print(f"Total: {total_token} token with {model_config['text_model']} -> {in_price + out_price:4.2f} m€")


model_configs: dict[str, dict] = {
    'high': {
        'text_model': 'gpt-4-turbo',
        'prompt_pricing': 0.010,
        'completion_pricing': 0.028,
        'context_max': 128_000,
    },
    'low': {
        'text_model': 'gpt-35-turbo-1106',
        'prompt_pricing': 0.003,
        'completion_pricing': 0.004,
        'context_max': 16_000,
    }
}

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15"
)