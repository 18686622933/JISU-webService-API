#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from DataItem import *

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)
# 将初始化的FLask绑定到api
api = Api(app)

# 使用flask_restful内置的reqparse库来做数据验证
parser = reqparse.RequestParser()
# 添加验证参数
# 第一个参数： 传递的参数的名称
# 第二个参数（location）： 传递参数的方式
# 第三个参数（type）： 验证参数的函数(可以自定义验证函数)
# parser.add_argument('username', location='args', type=str)
parser.add_argument('task')

# 配置路由
api.add_resource(Department, '/department', '/department/<code>')
api.add_resource(Teacher, '/teacher', '/teacher/<code>')

if __name__ == '__main__':
    app.run(host='192.168.2.200', debug=True)
