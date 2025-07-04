import json
import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# 環境変数からキーとエンドポイントを取得
try:
    load_dotenv()  # .env ファイルを読み込む
    language_endpoint = os.environ["LANGUAGE_ENDPOINT"]
    language_key = os.environ["LANGUAGE_KEY"]
except KeyError:
    print("Missing environment variable 'LANGUAGE_KEY' or 'LANGUAGE_ENDPOINT'")
    print("Set them before running this sample.")
    exit()

# テキスト分析クライアントの作成
ta_credential = AzureKeyCredential(language_key)
client = TextAnalyticsClient(endpoint=language_endpoint, credential=ta_credential)

try:
    # ./docs.mdファイルを読み込み、documentsリストに格納
    with open("./docs.md", "r") as f:
        documents = [f.read()]

    # テキスト分析APIを使用して言語を検出
    response = client.detect_language(documents=documents, country_hint="us")[0]
    print("Language: ", response.primary_language.name)

    # responseをJson構造でresult.jsonに保存
    # 必要な情報を抽出してJSON構造に変換
    result = {
        "name": response.primary_language.name,
        "iso6391_name": response.primary_language.iso6391_name,
        "confidence_score": response.primary_language.confidence_score,
    }
    with open("./result.json", "w") as f:
        f.write(json.dumps(result, indent=4))

except Exception as err:
    print("Encountered exception. {}".format(err))
