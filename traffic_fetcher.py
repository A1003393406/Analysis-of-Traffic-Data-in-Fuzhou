# traffic_fetcher.py
from amap_api import get_traffic_status
from config import FREE_FLOW_SPEEDS


def get_free_flow_speed(road_name):
    """
    根据道路名称获取自由流速度
    :param road_name: 道路名称
    :return: 自由流速度 (km/h)
    """
    # 首先检查是否有特定道路的配置
    for key in FREE_FLOW_SPEEDS:
        if key in road_name:
            return FREE_FLOW_SPEEDS[key]

    # 检查道路类型关键词
    road_type_keywords = {
        "高速": "高速公路",
        "快速": "快速路",
        "高架": "高架路",
        "大道": "主干道",
        "路": "主干道",
        "街": "主干道"
    }

    for keyword, road_type in road_type_keywords.items():
        if keyword in road_name:
            return FREE_FLOW_SPEEDS.get(road_type, FREE_FLOW_SPEEDS["default"])

    # 默认值
    return FREE_FLOW_SPEEDS["default"]


def calculate_delay_index(speed, status, free_flow_speed):
    """
    计算道路交通延时指数
    :param speed: 当前速度
    :param status: 交通状态
    :param free_flow_speed: 自由流速度
    :return: 延时指数
    """
    if speed is None or free_flow_speed is None or free_flow_speed == 0:
        # 根据状态估算
        status_mapping = {
            "0": 1.0,  # 未知，默认1.0
            "1": 1.0,  # 畅通
            "2": 1.5,  # 缓行
            "3": 2.0,  # 拥堵
            "4": 2.5,  # 严重拥堵
            "error": 1.0  # 错误，默认1.0
        }
        return status_mapping.get(str(status), 1.0)

    # 基于速度比计算
    speed_ratio = free_flow_speed / float(speed)
    return round(speed_ratio, 2)


def fetch_fuzhou_traffic(roads):
    """
    获取福州多个道路的交通状况
    :param roads: 道路列表
    :return: 道路交通信息字典
    """
    city = "福州市"
    results = []
    for road in roads:
        data = get_traffic_status(city, road)
        if data.get("status") == "1":
            for r in data.get("trafficinfo", {}).get("roads", []):
                # 获取自由流速度
                free_flow_speed = get_free_flow_speed(r.get("name", road))

                # 计算延时指数
                delay_index = calculate_delay_index(
                    r.get("speed"),
                    r.get("status"),
                    free_flow_speed
                )

                results.append({
                    "road_name": r.get("name"),
                    "direction": r.get("direction"),
                    "speed": r.get("speed"),
                    "status": r.get("status"),  # 0=未知,1=畅通,2=缓行,3=拥堵,4=严重拥堵
                    "description": r.get("description"),
                    "delay_index": delay_index,  # 新增延时指数
                    "free_flow_speed": free_flow_speed  # 添加自由流速度用于调试
                })
        else:
            # 对于请求失败的道路，使用默认自由流速度
            free_flow_speed = get_free_flow_speed(road)
            delay_index = calculate_delay_index(None, "error", free_flow_speed)

            results.append({
                "road_name": road,
                "direction": None,
                "speed": None,
                "status": "error",
                "description": data.get("info", "请求失败"),
                "delay_index": delay_index,
                "free_flow_speed": free_flow_speed
            })
    return results