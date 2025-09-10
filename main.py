# main.py (修改后的版本)
from road_fetcher import fetch_roads_in_fuzhou
from traffic_fetcher import fetch_fuzhou_traffic
from csv_utils import save_to_csv
import traceback


def calculate_average_delay_index(traffic_data):
    """
    计算平均延时指数
    :param traffic_data: 交通数据列表
    :return: 平均延时指数
    """
    valid_data = [item for item in traffic_data if
                  item.get("delay_index") is not None and item.get("status") != "error"]
    if not valid_data:
        return 0

    total_delay = sum(float(item["delay_index"]) for item in valid_data)
    return round(total_delay / len(valid_data), 2)


if __name__ == "__main__":
    try:
        # 先获取福州道路名称
        roads = fetch_roads_in_fuzhou(pages=10)  # 页数可调，越大抓取越多
        print(f"共获取到 {len(roads)} 条道路")

        # 获取交通数据
        traffic_data = fetch_fuzhou_traffic(roads)

        # 计算平均延时指数
        avg_delay = calculate_average_delay_index(traffic_data)
        print(f"福州市平均交通延时指数: {avg_delay}")

        # 打印到控制台
        for record in traffic_data:
            print(record)

        # 保存到 CSV
        save_to_csv(traffic_data, "fuzhou_traffic.csv")
        print("数据已保存到 fuzhou_traffic.csv")

        # 打印延时指数最高的5条道路
        sorted_by_delay = sorted(
            [r for r in traffic_data if r.get("delay_index") is not None and r.get("status") != "error"],
            key=lambda x: x["delay_index"],
            reverse=True
        )[:5]

        print("\n延时指数最高的5条道路:")
        for i, road in enumerate(sorted_by_delay, 1):
            print(
                f"{i}. {road['road_name']}: 延时指数 {road['delay_index']} (速度: {road['speed']}km/h, 状态: {road['status']})")

    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        traceback.print_exc()