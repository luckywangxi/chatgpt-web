from flask import Flask, request, jsonify
import random
import string
import pymysql.cursors
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# 连接数据库
conn = pymysql.connect(
    host='124.221.74.11',
    user='onebot',
    password='onebot',
    db='onebot',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/api/tokens', methods=['POST'])
def generate_tokens():
    # 解析请求参数
    data = request.get_json()
    at = data.get('at')
    js = data.get('js')
    jishu = data.get('jishu','')
    count = data.get('count', 1)

    # 生成 Token
    tokens = []
    for i in range(count):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        tokens.append(token)

    # 将 Token 存储到数据库中
    with conn.cursor() as cursor:
        sql = 'INSERT INTO auth_token (at, js, jishu, token_value) VALUES (%s, %s, %s, %s)'
        values = [(at, js, jishu, token) for token in tokens]
        cursor.executemany(sql, values)
    conn.commit()

    return jsonify(tokens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)