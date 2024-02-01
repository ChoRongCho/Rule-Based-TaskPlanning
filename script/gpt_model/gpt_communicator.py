import json

from openai import OpenAI

TOTAL_TOKEN_USED = 0


def get_api(api_json):
    with open(api_json, "r") as f:
        key = json.load(f)
        api_key = key["api_key"]
        f.close()
    return api_key


def estimate_token_count(text):
    return len(text) // 4


def update_total_tokens(estimated_tokens):
    global TOTAL_TOKEN_USED
    TOTAL_TOKEN_USED += estimated_tokens


def chat_with_gpt(messages, model="gpt-4", stop_sequences=None):
    api_key = get_api("/home/changmin/PycharmProjects/GPT_examples/setting.json")

    client = OpenAI(api_key=api_key)
    request_data = {
        "model": model,
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 1,
        "stop": stop_sequences
    }

    response = client.chat.completions.create(**request_data)
    response_text = response.choices[0].message.content

    messages.append({"role": "assistant", "content": response_text})
    estimated_tokens = estimate_token_count(response_text)
    update_total_tokens(estimated_tokens)

    return response_text, messages


def main():
    messages = [{"role": "system",
                 "content": "You are a compassionate and knowledgeable therapist.Listen carefully and provide thoughtful, empathetic responses."}]

    while True:
        user_input = input("You: ")
        messages.append({"role": "user", "content": user_input})
        response, messages = chat_with_gpt(messages, stop_sequences=["Thank you", "End"])
        print("You, ", messages)
        print("Assistant:", response)
        if "Thank you" in user_input or "End" in user_input:
            break

        print(f"Total estimated tokens used so far: {TOTAL_TOKEN_USED}")


if __name__ == '__main__':
    main()
