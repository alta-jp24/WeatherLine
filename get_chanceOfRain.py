import requests

try:
    # タイムアウトを5秒に設定
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/18001",timeout=5)

    # HTTPステータスコードをチェック
    response.raise_for_status()

    data = response.json()

    # 降水確率を取得（T12_18の値を取得）
    chanceOfRain_str = data["forecasts"][0]["chanceOfRain"]["T12_18"].strip("%")
    chanceOfRain = int(chanceOfRain_str)
    
    if int(chanceOfRain) >= 50:
        print(f"T12_18の降水確率は{chanceOfRain}%です。雨の可能性があります。")

except requests.exceptions.Timeout:
    # タイムアウト処理
    print("リクエストがタイムアウトしました。")

except requests.exceptions.HTTPError as e:
    # HTTPエラー処理（例: 404 Not Found, 500 Internal Server Error
    print(f"HTTPエラーが発生しました: {e.response.status_code} {e.response.reason}")

except requests.exceptions.RequestException as e:
    # その他のリクエストエラー
    print(f"リクエスト中にエラーが発生しました: {e}")

except KeyError:
    print("KeyError")