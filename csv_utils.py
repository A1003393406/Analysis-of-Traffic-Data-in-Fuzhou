# csv_utils.py
import csv
import os
from datetime import datetime

def save_to_csv(data, filename="fuzhou_traffic.csv"):
    """
    将交通数据保存为 CSV 文件
    :param data: 交通数据列表
    :param filename: 输出文件名
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        # 更新字段列表，添加delay_index和free_flow_speed
        fieldnames = ["timestamp", "road_name", "direction", "speed", "status", "description", "delay_index", "free_flow_speed"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in data:
            row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row)