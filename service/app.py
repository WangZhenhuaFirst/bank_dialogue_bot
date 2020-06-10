import datetime
from flask import Flask, session, redirect, Response, request, render_template, url_for, flash
from redis import StrictRedis

app = Flask(__name__)

# session cookie密钥
app.secret_key = 'pardon110'

# 连接redis数据库,默认是零号库,可随便更改
rds = StrictRedis(db=3)


def event_stream():
    '''消息生成器'''

    # 从数据库连接上获取发布订阅管理对象实例
    pub = rds.pubsub()

    # 在管理订阅(建立通道)频道
    pub.subscribe('chat')

    # 监听频道信息
    for message in pub.listen():
        print(type(message['data']), type(message), message)

        # 只响应有消息的（字节），首次无消息返回的为int状态码对象，直接忽略
        if isinstance(message['data'], bytes):
            # 转为utf8字符串，发送 SSE（Server Send Event）协议格式的数据
            yield 'data: %s\n\n' % message['data'].decode()


# 首次访问需要登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['user']
        # 重定向到home处理器
        flash('您已经成功登录！')
        return redirect(url_for('home'))
    return '<p><strong>登录</strong></p><form action="" method="post">用户名: <input name="user">'


# 接收js发送过来的消息
@app.route('/post', methods=['POST'])
def post():
    # 获取表单提交内容
    message = request.form['message']
    # 获取当前请求对象的session实例
    user = session.get('username', 'anonymous')
    # 返回一个指定字段的时间值
    now = datetime.datetime.now().replace(microsecond=0).time()
    # 通过频道发布消息
    rds.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    # 响应对象
    return Response(status=204)


# 事件流接口
@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/')
@app.route('/<name>')
def home(name=None):
    # 通过路由参数或querystring注册为当前用户
    if name or len(request.args) > 0:
        session['username'] = name if name else request.args.get('user', '')
        # 消息闪现（存储在session内，模板页用完即丢）
        flash(session['username']+'已经成功登录，加入聊天室！')
    # 否则强制用户登录
    if 'username' not in session:
        return redirect('/login')

    # 模板渲染
    data = {
        "username": session['username'],
        "tip": "正在聊天中..."
    }

    # 关键字参数解包，返回元组（框架会自动解析为一个完整的response对象）
    return render_template('home.html', **data), 200


@app.route('/logout')
def logout():
    # 清空当前session信息
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', debug=True)
