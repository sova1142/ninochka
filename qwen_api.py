import requests
import config

QWEN_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation "
HEADERS = {
    "Authorization": f"Bearer {config.QWEN_API_KEY}",
    "Content-Type": "application/json"
}

def generate_response(prompt):
    payload = {
        "model": "qwen-plus",
        "input": {"prompt": prompt}
    }

    response = requests.post(QWEN_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()['output']['text']
    else:
        return "Извини, я немного устала... давай чуть позже?"
