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

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            output = base64.b64encode(image_file.read()).decode('utf-8')
            return output

    def add_message(self, image_path):
        prompt = self.get_prompt()
        encoded_image = self.encode_image(image_path)
        content = [{"type": "text", "text": prompt},
                   {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]
        self.message.append({"role": "user", "content": content})

    def add_message_text_only(self, role="user"):
        prompt = self.get_prompt()
        content = {"role": role, "content": prompt}
        self.message.append(content)

    def run(self):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=self.message,
            max_tokens=self.max_token,
        )
        answer = response.choices[0].message.content
        print(answer)
        self.message_file.close()

    # def prompt_engineering(self):
    #     """
    #     prompt_file: content + file_path
    #     :return:
    #     """
    #     while True:
    #         prompt = self.get_prompt()
    #         if "image_path:" in prompt:
    #             try:
    #                 text_content = prompt.split("image_path:")[0]
    #                 image_path = prompt.split("image_path:")[1]
    #                 self.add_message(image_path=image_path)
    #
    #             except:
    #                 raise TypeError("No 'image_path:' or wrong image_path")
    #
    #         else:
    #             self.add_message_text_only("")


class GPT4Text(GPT4):
    def __init__(self, api_json_path, prompt_file_path, max_token=100):
        super().__init__(api_json_path, prompt_file_path, max_token)

    def add_message(self, role="user"):
        prompt = self.get_prompt()
        content = {"role": role, "content": prompt}
        self.message.append(content)

    def run(self):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=self.message,
            max_tokens=self.max_token,
        )
        answer = response.choices[0].message.content
        print(answer)
        self.message_file.close()


class GPT4VisionNew(GPT4):
    def __init__(self):
        pass