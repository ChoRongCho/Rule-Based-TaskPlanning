import base64
import json
import os.path
import time
from openai import OpenAI


class GPTInterpreter:
    def __init__(self,
                 api_json: str,
                 prompt_json: str,
                 save_path: str or bool = False):

        self.save_path = save_path
        self.api_json = api_json
        self.prompt_json = prompt_json

        self.setting = {}
        self.api_key = self.get_api_key()
        self.name, self.description, self.instruction, self.prompt = self.get_prompt()
        self.message = []

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            output = base64.b64encode(image_file.read()).decode('utf-8')
            return output

    def get_api_key(self):
        with open(self.api_json, "r") as file:
            self.setting = json.load(file)["setting"]
            api_key = self.setting["api_key"]
            file.close()
            return api_key

    def get_prompt(self):
        with open(self.prompt_json) as file:
            data = json.load(file)
            name = data["name"]
            description = data["description"]
            instruction = data["instruction"]
            prompt = data["prompt"]
            file.close()
            return name, description, instruction, prompt

    def add_message(self):
        sorted_prompt = sorted(self.prompt, key=lambda x: x['index'])
        for i in range(len(sorted_prompt)):
            role = sorted_prompt[i]["role"]
            content_text = sorted_prompt[i]["content"]
            if sorted_prompt[i]["image_path"]:
                image_path = sorted_prompt[i]["image_path"]
                encoded_image = self.encode_image(image_path)
                content = [{"type": "text", "text": content_text},
                           {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]
                content = {"role": role, "content": content}

            else:
                content = {"role": role, "content": content_text}
            self.message.append(content)

    def log_answer(self, answer):
        # question = self.message[-1]["content"]

        json_object = {"answer": answer}
        json_object = json.dumps(json_object, indent=4)
        with open(self.save_path, "w") as f:
            f.write(json_object)
            f.close()

    def run(self):
        client = OpenAI(api_key=self.api_key)
        self.add_message()

        response = client.chat.completions.create(
            model=self.setting["model"],
            messages=self.message,
            max_tokens=self.setting["max_token"],
            temperature=self.setting["temperature"],
            top_p=self.setting["top_p"]
        )
        answer = response.choices[0].message.content

        if self.save_path:
            self.log_answer(answer=answer)

