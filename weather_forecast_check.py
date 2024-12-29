import requests

try:
    # タイムアウトを5秒に設定
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/180010",timeout=5)

    # HTTPステータスコードをチェック
    response.raise_for_status()

    data = response.json()

    # 降水確率を取得（T12_18の値を取得）
    chanceOfRain_str = data["forecasts"][0]["chanceOfRain"]["T12_18"].strip("%")
    
    if chanceOfRain_str == "--":
        print("降水確率が未設定または不明です。")
    else:
        chanceOfRain = int(chanceOfRain_str)
        if chanceOfRain >= 50:
            print(f"T12_18の降水確率は{chanceOfRain}%です。雨の可能性があります。")
        else:
            print(f"T12_18の降水確率は{chanceOfRain}%です。雨の可能性は低いです。")

except requests.exceptions.Timeout:
    # タイムアウト処理
    print("天気予報の取得に失敗しました（タイムアウト）。")

except requests.exceptions.HTTPError as e:
    # HTTPエラー処理
    print(f"天気予報の取得に失敗しました（HTTPエラー: {e.response.status_code} {e.response.reason}）。")

except requests.exceptions.RequestException as e:
    # その他のリクエストエラー
    print(f"天気予報の取得中にエラーが発生しました: {str(e)}")