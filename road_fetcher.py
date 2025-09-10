# road_fetcher.py
import requests
from config import AMAP_KEY

BASE_URL = "https://restapi.amap.com/v3/place/text"

def fetch_roads_in_fuzhou(keyword="道路", pages=5):
    """
    获取福州市的道路名称（POI检索）
    :param keyword: 搜索关键字，默认“道路”
    :param pages: 爬取页数（每页最多50条）
    :return: 道路名称列表
    """
    roads = []
    for page in range(1, pages + 1):
        params = {
            "key": AMAP_KEY,
            "keywords": keyword,
            "city": "福州市",
            "types": "1903",  # 城市道路
            "offset": 50,
            "page": page
        }
        response = requests.get(BASE_URL, params=params, timeout=10).json()
        if response.get("status") != "1":
            break
        pois = response.get("pois", [])
        if not pois:
            break
        for poi in pois:
            name = poi.get("name")
            if name and name not in roads:
                roads.append(name)
    return roads
