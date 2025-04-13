from pathlib import Path
import os
import requests
from datetime import datetime

script_dir = Path (__file__).resolve().parent
os.chdir(script_dir)
weather_file = script_dir / "weather.txt"

API_KEY = "API_KEY" # Get from website
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        city_map = {"台北": "Taipei,TW", "台中": "Taichung,TW", "高雄": "Kaohsiung,TW"}
        api_city = city_map.get(city, city)
        params = {"q": api_city, "appid": API_KEY, "units": "metric", "lang": "zh_tw"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data["cod"] != 200:
            return f"找不到 {city} 的天氣！錯誤：{data.get('message', '未知')}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        advice = "帶把傘！" if "雨" in desc else "穿件外套！" if temp < 20 else "輕鬆出門！"
        result = f"{city}：{temp}°C，{desc}，{advice}"
        save_weather(result)
        return result
    except requests.exceptions.RequestException as e:
        return f"網路問題，晚點試！錯誤：{str(e)}"
    except KeyError as e:
        return f"資料解析錯誤，欄位缺！錯誤：{str(e)}"
    except Exception as e:
        return f"天氣服務壞掉了，晚點試！錯誤：{str(e)}"

def save_weather(result):
    with open(weather_file, "a", encoding="utf-8") as file:
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        file.write(f"{time} | {result}\n")

def show_history():
    if not weather_file.exists():
        return "還沒查過天氣"
    with open(weather_file, "r", encoding="utf-8") as file:
        return "\n".join(file.readlines()) if file else "沒紀錄！"
    
def main():
    print("天氣提醒器！")
    while True:
        print("\n指令: check <city>/history/exit")
        cmd = input("輸入指令: ").strip().lower()
        if cmd == "exit":
            print("See you!")
            break
        elif cmd.startswith("check "):
            city = cmd[6:].strip()
            if city:
                print(get_weather(city))
            else:
                print("City can't be blanked")
        elif cmd == "history":
            print(show_history())
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()