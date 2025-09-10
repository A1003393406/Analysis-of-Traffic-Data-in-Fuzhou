# road_delay_analysis.py
# 道路拥堵指数统计条形图

import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
import os


def load_data(file_path="fuzhou_traffic.csv"):
    """读取交通数据CSV文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件 {file_path} 不存在")

    df = pd.read_csv(file_path)
    return df


def calculate_total_delay_index(df):
    """计算每条道路的拥堵指数总和"""
    # 按道路名称分组并求和
    road_delay = df.groupby('road_name')['delay_index'].sum().reset_index()
    # 按拥堵指数排序（从高到低）
    road_delay = road_delay.sort_values('delay_index', ascending=False)
    return road_delay


def create_minimalist_bar_chart(road_delay, title="福州道路拥堵指数前10"):
    """创建简约风格条形统计图"""
    # 提取道路名称和拥堵指数
    road_names = road_delay['road_name'].tolist()
    delay_values = [round(val, 2) for val in road_delay['delay_index'].tolist()]

    # 创建条形图 - 简约风格
    bar = (
        Bar(init_opts=opts.InitOpts(
            width="1000px",
            height="600px",
            bg_color="#FFFFFF"
        ))
            .add_xaxis(road_names)
            .add_yaxis(
            "",  # 不显示系列名称
            delay_values,
            itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),  # 蓝色条形
            label_opts=opts.LabelOpts(
                position="top",  # 数值显示在条形上方
                formatter="{c}",  # 只显示数值
                font_size=10
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#333"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 旋转x轴标签
                    font_size=10,
                    interval=0  # 显示所有标签
                ),
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name="拥堵指数之和",
                name_textstyle_opts=opts.TextStyleOpts(font_size=12),
                splitline_opts=opts.SplitLineOpts(is_show=True)  # 显示水平网格线
            ),
            # 移除图例和工具箱
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            # 添加数据区域缩放
            datazoom_opts=opts.DataZoomOpts(
                type_="inside",  # 内置型数据区域缩放组件
                range_start=0,
                range_end=100
            )
        )
            .set_series_opts(
            # 设置条形宽度
            bar_width="40%"
        )
    )

    return bar


def create_top_n_bar_chart(road_delay, n=15, title="福州道路24小时拥堵指数统计(TOP {})"):
    """创建前N条道路的条形统计图"""
    # 提取前N条道路
    top_roads = road_delay.head(n)
    road_names = top_roads['road_name'].tolist()
    delay_values = [round(val, 2) for val in top_roads['delay_index'].tolist()]

    # 创建条形图
    bar = (
        Bar(init_opts=opts.InitOpts(
            width="1000px",
            height="600px",
            bg_color="#FFFFFF"
        ))
            .add_xaxis(road_names)
            .add_yaxis(
            "",  # 不显示系列名称
            delay_values,
            itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),  # 蓝色条形
            label_opts=opts.LabelOpts(
                position="top",  # 数值显示在条形上方
                formatter="{c}",  # 只显示数值
                font_size=10
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title.format(n),
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#333"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 旋转x轴标签
                    font_size=10
                ),
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name="拥堵指数总和",
                name_textstyle_opts=opts.TextStyleOpts(font_size=12),
                splitline_opts=opts.SplitLineOpts(is_show=True)  # 显示水平网格线
            ),
            # 移除图例和工具箱
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(is_show=False)
        )
            .set_series_opts(
            # 设置条形宽度
            bar_width="40%"
        )
    )

    return bar


def create_full_rounded_bar_chart(road_delay, title="福州道路24小时拥堵指数统计"):
    """创建完整圆角条形统计图（所有道路）"""
    # 提取道路名称和拥堵指数
    road_names = road_delay['road_name'].tolist()
    delay_values = [round(val, 2) for val in road_delay['delay_index'].tolist()]

    # 创建条形图
    bar = (
        Bar(init_opts=opts.InitOpts(
            width="1000px",
            height="600px",
            bg_color="#FFFFFF"
        ))
            .add_xaxis(road_names)
            .add_yaxis(
            "",  # 不显示系列名称
            delay_values,
            itemstyle_opts=opts.ItemStyleOpts(
                color="#5470C6",  # 蓝色条形
                border_radius=[18, 18, 0, 0]  # 设置顶部圆角，底部直角
            ),
            label_opts=opts.LabelOpts(
                position="top",  # 数值显示在条形上方
                formatter="{c}",  # 只显示数值
                font_size=10
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#333"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 旋转x轴标签
                    font_size=10,
                    interval=0  # 显示所有标签
                ),
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name="拥堵指数总和",
                name_textstyle_opts=opts.TextStyleOpts(font_size=12),
                splitline_opts=opts.SplitLineOpts(is_show=True)  # 显示水平网格线
            ),
            # 移除图例和工具箱
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            # 添加数据区域缩放
            datazoom_opts=opts.DataZoomOpts(
                type_="inside",  # 内置型数据区域缩放组件
                range_start=0,
                range_end=100
            )
        )
            .set_series_opts(
            # 设置条形宽度
            bar_width="40%"
        )
    )

    return bar

def main():
    try:
        # 1. 读取数据
        print("正在读取数据...")
        df = load_data("fuzhou_traffic.csv")
        print(f"成功读取 {len(df)} 条记录")

        # 2. 计算每条道路的拥堵指数总和
        print("正在计算道路拥堵指数总和...")
        road_delay = calculate_total_delay_index(df)
        print(f"共统计了 {len(road_delay)} 条道路")

        # 3. 创建两种图表
        print("正在生成可视化图表...")

        # 简约风格完整图表（包含所有道路，可缩放）
        bar_chart_full = create_minimalist_bar_chart(road_delay)
        bar_chart_full.render("road_delay_full.html")
        print("完整图表已保存至: road_delay_full.html")

        # 前10条道路的图表
        bar_chart_top = create_top_n_bar_chart(road_delay, 10)
        bar_chart_top.render("road_delay_top10.html")
        print("TOP15图表已保存至: road_delay_top10.html")

        # 4. 打印统计结果
        print("\n道路拥堵指数统计（前10条）：")
        print(road_delay.head(10).to_string(index=False))

        # 5. 保存统计结果为CSV文件
        stats_file = "road_delay_summary.csv"
        road_delay.to_csv(stats_file, index=False, encoding="utf-8-sig")
        print(f"\n详细统计数据已保存至: {stats_file}")

    except Exception as e:
        print(f"程序执行出错: {str(e)}")


if __name__ == "__main__":
    main()