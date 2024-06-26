from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_sina_stock_data(ticker):
    url = f'http://hq.sinajs.cn/list={ticker}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        return data
    else:
        return None

@app.route('/stock/<ticker>', methods=['GET'])
def stock(ticker):
    data = get_sina_stock_data(ticker)
    if data:
        return jsonify({'data': data})
    else:
        return jsonify({'error': 'Failed to retrieve data'}), 404

if __name__ == '__main__':
    app.run(debug=True)
