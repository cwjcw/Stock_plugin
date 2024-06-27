import akshare as ak
import time
import csv



# 获取两市股票的名单
def get_stock_list():
    """
    获取并返回包含A股股票代码和名称的字典。    
    该函数尝试从数据源获取最新的股票代码和名称列表。如果遇到网络超时等异常情况，它将重试直到成功获取数据。    
    Returns:
        dict: 包含股票代码作为键，股票名称作为值的字典。
    """
    while True:
        try:
            # 从Akshare获取A股股票代码和名称的数据框
            df = ak.stock_info_a_code_name()
            # 根据股票代码的前两位数字添加交易所代码（上海或深圳）
            df['code'] = df['code'].apply(
                lambda x: 'SZ' + x if x.startswith(('0', '3')) else ('SH' + x if x.startswith('6') else x))
            # 将数据框转换为以代码为索引的字典，只包含名称字段
            result_dict = df.set_index('code').to_dict()['name']
            break  # 如果成功，跳出循环
        except:
            # 如果遇到异常，打印错误信息并等待一段时间后重试
            print("Encountered TimeoutError. Retrying in 10 seconds...")
            time.sleep(2)  # 等待10秒再次尝试
    return result_dict

stock_list = get_stock_list()

with open('stock.csv', 'w', newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name'])  # 写入表头
    for key, value in stock_list.items():
        writer.writerow([key, value])