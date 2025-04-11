
# 📺 Bilibili 弹幕爬取与存储工具

一个基于 Python 的工具，可以通过输入 B 站视频链接，提取视频弹幕（弹幕池），并将弹幕数据解析后保存至本地 MongoDB 数据库中。

## ✨ 功能亮点

- 支持从 B 站视频链接自动提取 BV 号
- 调用官方 API 获取视频的 CID（弹幕池 ID）
- 抓取并解析 XML 格式的弹幕数据
- 将弹幕文本及属性（时间、模式、颜色、用户哈希）保存到 MongoDB
- 可拓展支持词云生成（已预留接口）

## 📦 项目结构

```bash
bilibili_danmaku/
│
├── study.py        # 主程序文件
├── README.md                 # 项目说明文件
└── requirements.txt          # 依赖库列表（可选）
```

## 🛠️ 环境依赖

请确保已安装以下 Python 库：

```bash
pip install requests beautifulsoup4 pymongo wordcloud matplotlib
```

## 🧠 使用说明

1. 确保本地已正确启动 MongoDB，并设置用户名、密码与数据库名（默认配置如下）：
   ```python
   MongoClient("mongodb://Useradmin:Userpwd@localhost:27017/?authSource=admin")
   ```

2. 运行主程序：

```bash
python study.py
```

3. 按提示输入 B 站视频链接，如：

```
请输入b站链接：https://www.bilibili.com/video/BV1Ud99YkEjW/
```

程序将依次输出：

- 提取出的 BV 号
- 获取的 CID
- 爬取到的弹幕条数
- 部分弹幕内容
- MongoDB 插入数据统计

## 🧩 示例输出

```
提取的BV号是: BV1Ud99YkEjW
视频的 cid 为: 872411296
共爬取到 4321 条弹幕
成功插入 4321 条弹幕
```

## 📌 可拓展功能

本项目已集成词云库 `WordCloud`，你可添加如下函数进行词频分析与可视化：

```python
def generate_word_cloud_from_danmaku(danmaku_list):
    text = ' '.join([item['text'] for item in danmaku_list])
    wc = WordCloud(font_path='msyh.ttc', background_color='white', width=800, height=600).generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
```



欢迎使用、修改、Star ⭐️ 或 Fork 本项目！

