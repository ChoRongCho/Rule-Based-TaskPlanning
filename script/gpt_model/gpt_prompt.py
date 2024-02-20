import base64
import json
import os.path
import os
import time
from openai import OpenAI


class GPTInterpreter:
    def __init__(self,
                 api_json: str,
                 example_prompt_json: str or bool,
                 result_dir: str or bool = False,
                 version: str = "vision"):

        self.result_dir = result_dir
        self.api_json = api_json
        self.example_prompt_json = example_prompt_json
        self.version = version

        self.setting = {}
        self.api_key = self.get_api_key()
        self.message = []

        print(self.setting)

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            output = base64.b64encode(image_file.read()).decode('utf-8')
            return output

    def get_api_key(self):
        with open(os.path.join(self.BASE_PATH, self.api_json), "r") as file:
            setting = json.load(file)

            if self.version.lower() == "vision":
                self.setting = setting["setting_vision"]
            elif self.version.lower() == "pddl":
                self.setting = setting["setting_pddl"]
            else:
                raise KeyError("setting version must be a vision or a pddl.")
            api_key = setting["api_key"]
            file.close()

            return api_key

    def add_example_prompt(self, message_name: str):
        """
        Add example before run gpt-4

        :param message_name:
        :return:
        """

        if not self.example_prompt_json:
            raise ValueError("There is no example json file")

        with open(os.path.join(self.BASE_PATH, self.example_prompt_json), "r") as file:
            data = json.load(file)
            example_message = data[message_name]
            file.close()

        sorted_prompt = sorted(example_message, key=lambda x: x['index'])
        for i in range(len(sorted_prompt)):
            role = sorted_prompt[i]["role"]
            content_text = sorted_prompt[i]["content"]
            if sorted_prompt[i]["image_path"]:
                image_path = sorted_prompt[i]["image_path"]
                encoded_image = self.encode_image(image_path)
                content = [{"type": "text", "text": content_text},
                           {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]
                prompt = {"role": role, "content": content}
            else:
                prompt = {"role": role, "content": content_text}
            self.message.append(prompt)

    def log_prompt(self, name=""):
        result_dir_json = os.path.join(self.result_dir, name + "_prompt.txt")
        with open(result_dir_json, "w") as f:
            f.write(str(self.message))
            f.close()

    def log_answer(self, answer, name=""):
        # question = self.message[-1]["content"]
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
            print(f"Directory '{self.result_dir}' created successfully.")
        else:
            print(f"Directory '{self.result_dir}' already exists.")
        result_dir_json = os.path.join(self.result_dir, name + "_result.json")
        result_dir_txt = os.path.join(self.result_dir, name + "_result.pddl")

        json_object = {"name": name, "answer": answer}
        json_object = json.dumps(json_object, indent=4)

        # with open(result_dir_json, "w") as f:
        #     f.write(json_object)
        #     f.close()

        with open(result_dir_txt, "w") as f:
            f.write(answer)
            f.close()

    def add_message_manual(self, role, content, image_url: list[str] or str or bool = False):
        if not image_url:
            # Only text message
            prompt = {"role": role, "content": content}
        else:
            prompt = [{"type": "text", "text": content}]
            if type(image_url) is str:
                image_url = [image_url]
            for image in image_url:
                encoded_image = self.encode_image(image)
                prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
            prompt = {"role": role, "content": prompt}

        self.message.append(prompt)

    def delete_text_message_manual(self, index: int):
        if 0 <= index < len(self.message):
            print(f"Delete a message {self.message[index]}")
            del self.message[index]
        else:
            raise IndexError

    def run_manual_prompt(self, name, is_save=False):
        """
        after add_text_message_manual do run_manual_prompt
        for example:

        gpt4 = GPTInterpreter(...)
        gpt4.add_text_message_manual(role1, content1)
        gpt4.add_text_message_manual(role2, content2)
        ...
        gpt4.run_manual_prompt()
        """

        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.setting["model"],
            messages=self.message,
            max_tokens=self.setting["max_token"],
            temperature=self.setting["temperature"],
            top_p=self.setting["top_p"]
        )
        answer = response.choices[0].message.content

        if is_save:
            self.log_answer(answer=answer, name=name)
        return answer

    def run_json_prompt(self, name: str):
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

        if self.result_dir:
            self.log_answer(answer=answer, name=name)
        print(answer)
        return answer

    def reset_message(self):
        self.message = []

    def pop_message(self):
        self.message.pop()
