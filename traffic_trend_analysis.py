# traffic_trend_analysis.py
# 交通拥堵指数时间序列分析与可视化
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import os
from datetime import datetime


def load_data(file_path="fuzhou_traffic.csv"):
    """读取交通数据CSV文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件 {file_path} 不存在")

    df = pd.read_csv(file_path)
    # 转换时间戳列为datetime类型
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def calculate_hourly_traffic_index(df):
    """计算每小时的总拥堵指数"""
    # 按小时分组并求和
    df['hour'] = df['timestamp'].dt.hour
    hourly_traffic = df.groupby('hour')['delay_index'].sum().reset_index()
    return hourly_traffic


def find_peak_hours(hourly_traffic, n=3):
    """找出拥堵高峰时段"""
    # 按拥堵指数排序，找出最高的n个小时
    peak_hours = hourly_traffic.nlargest(n, 'delay_index')
    return peak_hours


def create_traffic_trend_chart(hourly_traffic, peak_hours, title="福州交通拥堵指数24小时趋势"):
    """创建交通拥堵趋势折线图"""
    # 提取小时和拥堵指数
    hours = [f"{int(h):02d}:00" for h in hourly_traffic['hour']]
    traffic_values = [round(val, 2) for val in hourly_traffic['delay_index']]

    # 标记高峰时段
    peak_points = []
    for _, row in peak_hours.iterrows():
        hour_idx = int(row['hour'])
        peak_points.append({
            "coord": [hour_idx, row['delay_index']],
            "value": f"高峰时段: {hour_idx:02d}:00\n拥堵指数: {row['delay_index']:.2f}"
        })

    # 创建折线图
    line = (
        Line(init_opts=opts.InitOpts(
            width="1200px",
            height="600px",
            bg_color="#FFFFFF"
        ))
            .add_xaxis(hours)
            .add_yaxis(
            "拥堵指数",
            traffic_values,
            is_smooth=True,  # 平滑曲线
            symbol="circle",  # 数据点样式
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=3, color="#5470C6"),
            itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(
                        coord=[int(row['hour']), row['delay_index']],
                        name=f"{int(row['hour']):02d}:00",
                        value=round(row['delay_index'], 2),
                        itemstyle_opts=opts.ItemStyleOpts(color="#EE6666")
                    ) for _, row in peak_hours.iterrows()
                ],
                label_opts=opts.LabelOpts(
                    position="top",
                    formatter=JsCode(
                        "function (params) { return params.data.value; }"
                    )
                )
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(
                        x=int(row['hour']),
                        name=f"{int(row['hour']):02d}:00",
                        symbol="none"
                    ) for _, row in peak_hours.iterrows()
                ],
                linestyle_opts=opts.LineStyleOpts(
                    type_="dashed",
                    color="#EE6666",
                    width=1
                ),
                label_opts=opts.LabelOpts(
                    position="middle",
                    formatter=JsCode(
                        "function (params) { return '高峰时段'; }"
                    )
                )
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                subtitle="数据来源: 高德地图API",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#333"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                name="时间",
                name_textstyle_opts=opts.TextStyleOpts(font_size=12),
                axislabel_opts=opts.LabelOpts(font_size=10)
            ),
            yaxis_opts=opts.AxisOpts(
                name="拥堵指数总和",
                name_textstyle_opts=opts.TextStyleOpts(font_size=12),
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                formatter=JsCode(
                    """function (params) {
                        return params[0].name + '<br/>' + 
                               '拥堵指数: ' + params[0].value;
                    }"""
                )
            ),
            datazoom_opts=[opts.DataZoomOpts()],
            toolbox_opts=opts.ToolboxOpts(
                feature={
                    "saveAsImage": {"title": "下载图片"},
                    "restore": {"title": "还原"},
                    "dataView": {"title": "数据视图"},
                }
            )
        )
    )

    return line


def main():
    try:
        # 1. 读取数据
        print("正在读取数据...")
        df = load_data("fuzhou_traffic.csv")
        print(f"成功读取 {len(df)} 条记录")

        # 2. 计算每小时的总拥堵指数
        print("正在计算每小时拥堵指数总和...")
        hourly_traffic = calculate_hourly_traffic_index(df)

        # 3. 找出高峰时段
        peak_hours = find_peak_hours(hourly_traffic, 3)
        print("高峰时段:")
        for _, row in peak_hours.iterrows():
            print(f"  {int(row['hour']):02d}:00 - 拥堵指数: {row['delay_index']:.2f}")

        # 4. 创建趋势图表
        print("正在生成趋势图表...")
        line_chart = create_traffic_trend_chart(hourly_traffic, peak_hours)

        # 5. 保存图表
        output_file = "traffic_trend_analysis.html"
        line_chart.render(output_file)
        print(f"趋势图表已保存至: {output_file}")

        # 6. 保存统计数据
        stats_file = "hourly_traffic_summary.csv"
        hourly_traffic.to_csv(stats_file, index=False, encoding="utf-8-sig")
        print(f"每小时统计数据已保存至: {stats_file}")

    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()