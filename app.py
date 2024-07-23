
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from realtime_price import stock_data as df

app = Flask(__name__)

# 如果本地保存的文件存在，读取成本价和持仓数量
if os.path.exists('current_stock.csv'):
    saved_data = pd.read_csv('current_stock.csv', dtype={'成本价': float, '持仓数量': int})
    df = df.merge(saved_data[['股票代码', '成本价', '持仓数量']], on='股票代码', how='left')

@app.route('/', methods=['GET', 'POST'])

# 定义主页索引函数
def index():
    # 检查请求方法是否为POST
    if request.method == 'POST':
        # 从请求的表单数据中获取成本价和持仓数量列表，并存储到DataFrame中
        # 获取表单数据
        df['成本价'] = request.form.getlist('cost_price')
        df['持仓数量'] = request.form.getlist('quantity')
        
        # 将成本价和持仓数量转换为浮点型，并计算当前市值和盈亏
        # 计算当前市值和盈亏
        df['成本价'] = df['成本价'].astype(float)
        df['持仓数量'] = df['持仓数量'].astype(float)
        df['当前市值'] = df['当前价'] * df['持仓数量']
        df['盈亏'] = (df['当前价'] - df['成本价']) * df['持仓数量']
        
        # 将DataFrame保存到CSV文件
        # 保存成本价和持仓数量到本地文件
        df.to_csv('current_stock.csv', index=False)
        
        # 重定向到主页
        return redirect(url_for('index'))
    
    # 如果请求方法不是POST，则渲染并返回主页模板
    return render_template('index.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)
