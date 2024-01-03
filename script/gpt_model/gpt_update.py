import base64
import json

from openai import OpenAI


class GPT4:
    def __init__(self,
                 api_json_path: str,
                 prompt_file_path: str,
                 max_token: int = 100):
        self.api_json_path = api_json_path
        self.prompt_file_path = prompt_file_path
        self.max_token = max_token

        self.api_key = self.get_api_key()
        self.message = []
        self.message_file = open(self.prompt_file_path, "r")

    def get_api_key(self):
        with open(self.api_json_path, "r") as file:
            data = json.load(file)
            api_key = data["changmin_api"][0]["api_key"]
        return api_key

    def get_prompt(self):
        prompt = self.message_file.readline()
        return prompt

    def add_message(self, image_path: str):
        prompt = self.get_prompt()
        content = prompt
        self.message.append({"role": "user", "content": content})

    def run(self):
        # client = OpenAI(api_key=self.api_key)
        print(0)

    def log(self):
        pass

    def get_instruction(self):
        pass

class GPT4Vision(GPT4):
    def __init__(self, api_json_path, prompt_file_path, max_token=100):
        super().__init__(api_json_path, prompt_file_path, max_token)