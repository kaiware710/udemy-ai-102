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

ta_credential = AzureKeyCredential(language_key)
ta_client = TextAnalyticsClient(endpoint=language_endpoint, credential=ta_credential)

try:
    # docs.mdファイルを読み込み、documentsリストに格納
    with open("docs.md", "r") as f:
        documents = [f.read()]

    # テキスト分析APIを使用して名前付きエンティティを抽出
    result = ta_client.recognize_entities(documents=documents)[0]

    entities_list = []
    for entity in result.entities:
        entity_info = {
            "Text": entity.text,
            "Category": entity.category,
            "SubCategory": entity.subcategory,
            "Confidence Score": round(entity.confidence_score, 2),
            "Length": entity.length,
            "Offset": entity.offset,
        }
        entities_list.append(entity_info)

    # 結果をJSON形式でresult.jsonに出力
    with open("./result.json", "w") as f:
        f.write(json.dumps(entities_list, ensure_ascii=False, indent=2))

except Exception as err:
    print("Encountered exception. {}".format(err))
    print("Encountered exception. {}".format(err))
