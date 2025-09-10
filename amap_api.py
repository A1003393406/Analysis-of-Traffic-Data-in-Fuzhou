# amap_api.py
import requests
from config import AMAP_KEY

BASE_URL = "https://restapi.amap.com/v3/traffic/status/road"

def get_traffic_status(city, road_name):
    """
    调用高德交通路况API
    :param city: 城市名，例如 "福州市"
    :param road_name: 道路名，例如 "五四路"
    :return: JSON 数据
    """
    params = {
        "key": AMAP_KEY,
        "city": city,
        "name": road_name,
        "extensions": "all"
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    return response.json()
