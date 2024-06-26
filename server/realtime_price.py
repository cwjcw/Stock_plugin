import json
import requests
import akshare as ak
import pandas as pd
import time
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

translation_dict = {
    "symbol": "股票代码",
    "current": "当前价",
    "percent": "涨跌百分比",
    "chg": "涨跌额",
    "timestamp": "时间戳"
}

# 获取两市股票的名单
def get_stock_list():
    while True:
        try:
            df = ak.stock_info_a_code_name()
            df['code'] = df['code'].apply(
                lambda x: 'SZ' + x if x.startswith(('0', '3')) else ('SH' + x if x.startswith('6') else x))
            result_dict = df.set_index('code').to_dict()['name']
            break  # 如果成功，跳出循环
        except:
            print("Encountered TimeoutError. Retrying in 10 seconds...")
            time.sleep(2)  # 等待10秒再次尝试
    return result_dict

stock_list = get_stock_list()

# 处理雪球返回的JSON数据
def xueqiu_data(json_data):
    data_dict = json.loads(json_data) # 文本文件，需要转为json格式
    df = pd.DataFrame(data_dict['data'])
    df.rename(columns=translation_dict, inplace=True)
    df["股票名称"] = df["股票代码"].map(stock_list)
    
    # 保留所需的列
    df = df[["股票代码", "股票名称", "当前价", "涨跌百分比", "涨跌额"]]
    
    # 添加新的字段
    df["成本价"] = 0  # 假设成本价为0，可以根据实际情况修改
    df["持仓数量"] = 0  # 假设持仓数量为0，可以根据实际情况修改
    df["当前市值"] = df["当前价"] * df["持仓数量"]
    df["盈亏"] = (df["当前价"] - df["成本价"]) * df["持仓数量"]
    
    return df.to_dict(orient='records')

# 调用雪球API，得到返回的json数据
def xueqiu_api(lis):
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }
    # 雪球API的URL后，股票可以用逗号隔开，并一次性返回所有股票的值
    url_parameter = ""
    for shares in lis:
        url_parameter = url_parameter + shares + ","
    # 发送API请求
    url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=" + url_parameter
    r = requests.get(url, headers=headers)
    r_dat = r.text
    return r_dat

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks', methods=['POST'])
def get_stocks():
    stocks = request.json.get('stocks', [])
    data = xueqiu_data(xueqiu_api(stocks))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
