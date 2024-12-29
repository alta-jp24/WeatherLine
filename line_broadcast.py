import os
import requests

def lambda_handler(event, context):
    # 環境変数の取得
    CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
    
    # LINEの返信APIにメッセージを送信
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    # メッセージ内容の作成
    body = {
        "messages": [
            {
                "type": "text",
                "text": "TEST Message!!"  # LINEに送信するメッセージ
            }
        ]
    }

    # リクエストの送信
    response = requests.post(
        'https://api.line.me/v2/bot/message/broadcast',
        headers=headers,
        json=body
    )

    return {
        'statusCode': response.status_code,
        'body': response.text
    }
