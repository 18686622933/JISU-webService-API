#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)
# 将初始化的FLask绑定到api
api = Api(app)

teachers = {'2014800185': '陈博文'}


def abort_if_data_doesnt_exist(data, id):
    """如果未找到数据则终止"""
    if id not in data:
        abort(404, message="{} doesn't exist".format(id))


# 使用flask_restful内置的reqparse库来做数据验证
parser = reqparse.RequestParser()
# 添加验证参数
# 第一个参数： 传递的参数的名称
# 第二个参数（location）： 传递参数的方式
# 第三个参数（type）： 验证参数的函数(可以自定义验证函数)
# parser.add_argument('username', location='args', type=str)
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Teacher(Resource):
    def get(self, tid):
        abort_if_data_doesnt_exist(teachers, tid)
        return teachers[tid]

    def delete(self, tid):
        abort_if_data_doesnt_exist(teachers, tid)
        del teachers[tid]
        return '', 204

    def put(self, tid):
        args = parser.parse_args()  # 验证数据，得到一个字典
        # result = args.get('task')  # 获得验证后的数据
        # print(result)
        task = {'task': args['task']}
        teachers[tid] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class AllTeacher(Resource):
    def get(self):
        return teachers


## Actually setup the Api resource routing here
api.add_resource(AllTeacher, '/teacher')
api.add_resource(Teacher, '/teacher/<tid>')

if __name__ == '__main__':
    app.run(host='192.168.14.200', debug=True)
