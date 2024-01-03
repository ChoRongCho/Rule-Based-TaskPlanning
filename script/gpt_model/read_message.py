import json

from openai import OpenAI


def get_api_key(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
        api_key = data["setting"]["api_key"]

    file.close()
    return api_key, data


api_key, _ = get_api_key(json_file="../../instructions/vision_prompt.json")
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4.0",
    response_format={"type": "json_object"},
    messages=[{"role": "system", "content": "You are a helpful assistant designed to output JSON."},
              {"role": "user", "content": "Who won the world series in 2020?"}],
)

print(response.choices[0].message.content)
