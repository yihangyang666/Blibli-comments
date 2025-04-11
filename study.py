import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
# ----------------------------
# 1. 获取视频的 cid（弹幕池 ID）
# ----------------------------
def get_cid(bvid):
    """通过视频 BV 号获取 cid"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["cid"]
    else:
        raise Exception("获取 cid 失败")

# ----------------------------
# 2. 获取弹幕数据（XML 格式）
# ----------------------------
def get_danmaku(cid):
    """通过 cid 获取弹幕 XML 数据"""
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode("utf-8")
    else:
        raise Exception("获取弹幕失败")

# ----------------------------
# 3. 解析 XML 弹幕数据
# ----------------------------
def parse_danmaku(xml_data):
    """解析 XML 格式的弹幕数据"""
    soup = BeautifulSoup(xml_data, "xml")
    danmaku_list = []
    for d in soup.find_all("d"):
        # 解析弹幕属性（如时间、颜色、用户等）
        attrs = d["p"].split(",")
        danmaku = {
            "text": d.text,
            "time": float(attrs[0]),  # 弹幕出现时间（秒）
            "mode": int(attrs[1]),    # 弹幕类型（滚动、顶部、底部等）
            "color": f"#{hex(int(attrs[3]))[2:].zfill(6)}",  # 颜色代码
            "user_hash": attrs[6]     # 用户匿名哈希（非真实用户 ID）
        }
        danmaku_list.append(danmaku)
    return danmaku_list

# ----------------------------
# 4. 连接 MongoDB 并保存数据
# ----------------------------
def save_to_mongodb(data, collection_name="comment1"):
    client = MongoClient("mongodb://Useradmin:Userpwd@localhost:27017/?authSource=admin")
    db = client["articledb"]
    collection = db[collection_name]
    # 批量插入数据
    result = collection.insert_many(data)
    print(f"成功插入 {len(result.inserted_ids)} 条弹幕")


from urllib.parse import urlparse, parse_qs


def extract_bvid_from_url(url):
    """
    从给定的B站视频URL中提取BV号。

    参数:
        url (str): B站视频的完整URL。

    返回:
        str: 提取出的BV号，如果未找到则返回None。
    """
    # 解析URL
    parsed_url = urlparse(url)
    # 检查路径部分以获取可能的BV号
    path_parts = parsed_url.path.split('/')
    # BV号通常位于路径中，形如 '/video/BV1QA94YPEMK'
    for part in path_parts:
        if part.startswith('BV'):
            return part
    # 如果在路径中没有找到，则检查查询参数
    query_dict = parse_qs(parsed_url.query)
    for value_list in query_dict.values():
        for value in value_list:
            if value.startswith('BV'):
                return value
    # 如果既不在路径也不在查询参数中，则返回None
    # bvid = extract_bvid_from_url(url)
    if value:
        print(f"提取的BV号是: {value}")
    else:
        print("未能从URL中提取BV号")

    return None




if __name__ == "__main__":
    # 目标视频 BV 号（从链接中提取）
    # bvid = "BV1Ud99YkEjW"


    # print("请输入b站链接：")
    url = input("请输入b站链接：")
    bvid = extract_bvid_from_url(url);
    if bvid:
        print(f"提取的BV号是: {bvid}")
    else:
        print("未能从URL中提取BV号")


    try:
        # 获取 cid
        cid = get_cid(bvid)
        print(f"视频的 cid 为: {cid}")

        # 获取弹幕 XML 数据
        xml_data = get_danmaku(cid)

        # 解析弹幕
        danmaku_list = parse_danmaku(xml_data)

        print(f"共爬取到 {len(danmaku_list)} 条弹幕")

        text_list = [item["text"] for item in danmaku_list]

        for text in text_list:
            print(text)

        # generate_word_cloud_from_danmaku(danmaku_list)
        # # print(danmaku_list[:5])  # 打印前5个元素以进行检查
        # # 保存到 MongoDB
        save_to_mongodb(danmaku_list)

    except Exception as e:
        print(f"程序出错: {e}")



