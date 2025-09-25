import os
from openai import OpenAI

client = OpenAI(
    # api_key=os.getenv("8799881013535bdf4bbb1a65cca5b0be"),
    api_key="xxx",
    base_url="https://xxx/api/openai/v1",
)
completion = client.chat.completions.create(
    model="DeepSeek-R1-671B", # 此处以DeepSeek-R1-671B为例，可按需更换模型名称。
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)

print(completion.model_dump_json())