import json
import base64


class GetAPI:
    def __init__(self, api_json: str, version: str):
        self.api_json = api_json
        self.version = version
        self.setting = None

    def get_api_key(self):
        with open(self.api_json, "r") as file:
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

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            output = base64.b64encode(image_file.read()).decode('utf-8')
            return output
