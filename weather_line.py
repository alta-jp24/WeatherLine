import os
import requests

def lambda_handler(event, context):
    # 環境変数の取得
    CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
    
    # LINE APIのヘッダー
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    # 天気予報APIを呼び出して降水確率を取得
    message = ""
    try:
        # タイムアウトを5秒に設定
        response = requests.get("https://weather.tsukumijima.net/api/forecast/city/180010", timeout=5)
        response.raise_for_status()

        data = response.json()

        # 降水確率を取得（T12_18の値を取得）
        chanceOfRain_str = data["forecasts"][0]["chanceOfRain"]["T12_18"].strip("%")
        
        if chanceOfRain_str == "--":
            message = "T12_18の降水確率が未設定または不明です。"
        else:
            chanceOfRain = int(chanceOfRain_str)
            if chanceOfRain >= 50:
                message = f"本日18時の降水確率は{chanceOfRain}%です。雨の可能性があります。"
            else:
                message = f"本日18時の降水確率は{chanceOfRain}%です。雨の可能性は低いです。"

    except requests.exceptions.Timeout:
        message = "天気予報の取得に失敗しました（タイムアウト）。"
    except requests.exceptions.HTTPError as e:
        message = f"天気予報の取得に失敗しました（HTTPエラー: {e.response.status_code} {e.response.reason}）。"
    except requests.exceptions.RequestException as e:
        message = f"天気予報の取得中にエラーが発生しました: {str(e)}"

    # LINEにメッセージを送信
    body = {
        "messages": [
            {
                "type": "text",
                "text": message  # 天気予報の結果をLINEに送信
            }
        ]
    }

    try:
        line_response = requests.post(
            'https://api.line.me/v2/bot/message/broadcast',
            headers=headers,
            json=body
        )
        line_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': f"Error sending message to LINE: {str(e)}"
        }

    # 正常終了
    return {
        'statusCode': line_response.status_code,
        'body': line_response.text
    }
