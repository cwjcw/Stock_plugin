import json
import requests
import pandas as pd
import akshare as ak

# 读取保存的csv文件,并转为字典
df = pd.read_csv('stock.csv', dtype={'id': str, 'name': str})
stock_dict = pd.Series(df.name.values, index=df.id).to_dict()

translation_dict = {
    "symbol": "股票代码",
    "current": "当前价",
    "percent": "涨跌百分比",
    "chg": "涨跌额",
    "timestamp": "时间戳"
}

# 处理雪球网站返回的股票数据，转换为DataFrame格式，并进行初步加工
def xueqiu_data(json_data):
    # 将JSON字符串转换为Python字典
    data_dict = json.loads(json_data) # 文本文件，需要转为json格式
    # 根据字典中的"data"键值创建DataFrame
    df = pd.DataFrame(data_dict['data'])
    # 将DataFrame的列名根据翻译字典进行转换
    df.rename(columns=translation_dict, inplace=True)
    # 根据股票代码查找并添加股票名称
    df["股票名称"] = df["股票代码"].map(stock_dict)
    
    # 筛选保留所需的列
    # 保留所需的列
    df = df[["股票代码", "股票名称", "当前价", "涨跌百分比", "涨跌额"]]
    
    # 初始化成本价、持仓数量、当前市值、盈亏列
    # 添加新的字段
    df["成本价"] = 0  # 假设成本价为0，可以根据实际情况修改
    df["持仓数量"] = 0  # 假设持仓数量为0，可以根据实际情况修改
    # 计算当前市值
    df["当前市值"] = df["当前价"] * df["持仓数量"]
    # 计算盈亏
    df["盈亏"] = (df["当前价"] - df["成本价"]) * df["持仓数量"]
    
    # 返回加工后的DataFrame
    return df

# 调用雪球API，得到返回的json数据
def xueqiu_api(lis):
    """
    根据提供的股票代码列表，通过雪球API获取实时股票数据。
    
    参数:
    lis: 股票代码列表，每个元素是一个股票代码。
    
    返回:
    请求结果的文本响应。
    """
    # 设置请求头，模拟浏览器访问
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }
    
    # 初始化股票代码参数
    # 雪球API的URL后，股票可以用逗号隔开，并一次性返回所有股票的值
    url_parameter = ""
    
    # 构建请求的股票代码参数
    for shares in lis:
        url_parameter = url_parameter + shares + ","
    
    # 完整的API请求URL
    # 发送API请求
    url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=" + url_parameter
    
    # 发送GET请求并获取响应
    r = requests.get(url, headers=headers)
    r_dat = r.text
    
    # 返回响应文本
    return r_dat

result = ak.stock_individual_spot_xq('SZ000981')
print(result)

stock = ['SZ000981', 'SH600078', 'SH600096']
stock_data = xueqiu_api(stock)
print(xueqiu_data(stock_data))

