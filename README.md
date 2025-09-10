# 福州交通数据采集系统 - Linux定时任务设置指南

## 概述

本文档指导您如何在Linux系统中设置定时任务，每隔10分钟自动运行交通数据采集脚本，并将数据追加到CSV文件中。

## 前提条件

1. Linux操作系统（Ubuntu/CentOS等）
2. Python 3.x 已安装
3. 必要的Python依赖已安装：`requests`

## 设置步骤

### 1. 确保Python脚本可执行

打开终端，导航到脚本所在目录，执行以下命令：

```bash
chmod +x main.py
```

### 2. 安装必要的Python依赖

```bash
pip install requests
```

### 3. 设置定时任务

1. 打开当前用户的crontab配置文件：

```bash
crontab -e
```

2. 在文件末尾添加以下行（请将`/path/to/your/script/`替换为您的实际脚本路径）：

```bash
*/10 * * * * /usr/bin/python3 /path/to/your/script/main.py >> /path/to/your/script/cron.log 2>&1
```

3. 保存并退出编辑器（在nano中按Ctrl+X，然后按Y确认，最后回车）

### 4. 验证定时任务

查看当前用户的定时任务列表，确认任务已添加：

```bash
crontab -l
```

### 5. 检查日志输出

定时任务运行后，您可以在指定的日志文件中查看运行结果：

```bash
tail -f /path/to/your/script/cron.log
```

## 文件说明

- `main.py` - 主程序，负责协调数据采集和保存
- `config.py` - 配置文件，包含API密钥和道路自由流速度设置
- `road_fetcher.py` - 道路名称获取模块
- `traffic_fetcher.py` - 交通数据获取和处理模块
- `amap_api.py` - 高德地图API调用模块
- `csv_utils.py` - CSV文件操作模块，已实现数据追加功能
- `fuzhou_traffic.csv` - 自动生成的交通数据CSV文件（首次运行后创建）
- `cron.log` - 定时任务日志文件（首次运行后创建）

## 数据追加说明

系统已默认实现数据追加功能：
- CSV文件使用追加模式（`mode="a"`）打开
- 首次运行会创建文件并写入表头
- 后续运行会将新数据追加到文件末尾
- 每条记录都包含时间戳，便于区分不同时间点的数据

## 故障排除

如果定时任务未按预期运行，可以检查以下方面：

1. 确保Python路径正确（使用`which python3`命令查看）
2. 检查脚本路径是否正确
3. 查看日志文件中的错误信息
4. 手动运行脚本测试是否正常工作：

```bash
python3 main.py
```

5. 检查cron服务是否运行：

```bash
sudo service cron status
```

## 注意事项

1. 确保高德地图API密钥有效且未超过调用限制
2. 系统会每10分钟采集一次数据，请确保网络连接稳定
3. CSV文件会随时间增长，定期备份或清理旧数据
4. 如需修改采集频率，可调整crontab中的时间设置

## 支持

如有问题，请检查日志文件或联系系统管理员。