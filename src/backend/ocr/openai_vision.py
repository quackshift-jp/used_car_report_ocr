import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(verbose=True)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI()


def convert_base64(path: str) -> str:
    with open(path, mode="rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def reshape_response(path: str):
    url = f"data:image/jpeg;base64,{convert_base64(path)}"
    prompt = f"""
    次のOCRテキストを、JSON形式にしてください。
    JSONのキーは固定で、値を画像から抽出してください。
    [出力形式]
    {{
        "排気量": [integer型],
        "型式": [string型],
        "車名": [string型],
        "形状・ドア数": [integer型],
        "走行": [string型]キロメートル,
        "セールスポイント": [string型],
        "注意事項": [string型],
        "希望価格": [integer型]000円,
        "スタート価格": [integer型]000円,
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content


print(reshape_response("data/IMG_0272.jpg"))
