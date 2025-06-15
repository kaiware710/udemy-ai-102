import os

import requests
from dotenv import load_dotenv

# 環境変数からAPIキーとエンドポイントを取得
try:
    load_dotenv()  # .env ファイルを読み込む
    endpoint = os.environ["VISION_ENDPOINT"] + "computervision/imageanalysis:segment"
    # endpoint = os.environ["VISION_ENDPOINT"]
    api_key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# 画像ファイルのパス
# image_path = './image-001.png'
image_path = "../lizard.jpeg"

# リクエストヘッダーとパラメータ
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/octet-stream",
}
params = {"api-version": "2023-02-01-preview", "mode": "backgroundRemoval"}

# 画像データを読み込む
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# リクエストを送信
response = requests.post(endpoint, headers=headers, params=params, data=image_data)

# 結果を保存
if response.status_code == 200:
    with open("./output_lizard.png", "wb") as output_image:
        output_image.write(response.content)
    print("背景が削除された画像が 'output_lizard.png' に保存されました。")
else:
    print(f"Error: {response.status_code}, {response.text}")
