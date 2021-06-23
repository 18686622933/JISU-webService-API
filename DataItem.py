#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import json
import dataSource
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

items = {'teacher': {'name': '全体在职教师',
                     'titles': ['工号', '单位号', '所在科室', '姓名', '性别', '出生地', '身份证件号', '政治面貌', '职称', '联系电话', '办公电话', '工作状态',
                                '职务'],
                     'sql': """SELECT GH,DWH,SZKS,XM,XBM,CSDM,SFZJH,ZZMMM,ZC,LXDH,BGDH,GZZT,ZW 
                FROM DLAKE_PERSONNEL_TEACHER_ALL  WHERE GH='2014800185' or GH='2010800037'"""},
         'department': {'name': '部门信息',
                        'titles': ['单位号', '上级单位号', '单位名称', '单位隐藏标识'],
                        'sql': """SELECT dwh,lsdwh,dwmc,dwyxbs FROM DLAKE_PERSONNEL_DEPARTMENT"""},
         'student': {'name': '学生信息',
                     'titles': [],
                     'sql': """"""},
         'score': {'name': '成绩表',
                   'titles': [],
                   'sql': """"""},
         }


def toJson(titles, data):
    """字典转json"""
    dic = [dict(zip(titles, i)) for i in data]
    res = json.dumps(dic, ensure_ascii=False, indent=4, separators=(',', ': '))

    return res


def abort_if_data_doesnt_exist(data, id):
    """如果未找到数据则终止"""
    if id not in data:
        abort(404, message="{} doesn't exist".format(id))


def getData(key):
    """按输出格式组织数据"""
    item = items[key]
    comment = item['titles']  # 字段注解
    columns = item['sql'].split(' ')[1].split(',')  # 字段名

    titles = dict(zip(columns, comment))
    data = dataSource.select(items[key]['sql'])
    data = [dict(zip(columns, d)) for d in data]

    res = {'titles': titles, 'data': data}
    return res


class Resource(Resource):
    """重新Resource类，增加获取类名的__init__函数"""

    def __init__(self):
        self.class_name = (str(self.__class__)[17:-2]).lower()  # 获取当前类名
        self.result = getData(self.class_name)
        self.data = self.result['data']


class Department(Resource):
    def get(self, code=None):
        if not code:
            return self.result
        else:
            data = {i[list(i.keys())[0]]: i for i in self.data}
            abort_if_data_doesnt_exist(data, code)
            return data[code]


class Teacher(Resource):
    def get(self, code=None):
        if not code:
            return self.result
        else:
            data = {i[list(i.keys())[0]]: i for i in self.data}
            abort_if_data_doesnt_exist(data, code)
            return data[code]


if __name__ == '__main__':
    # for k, v in getData('teacher').items():
    #     print(k, v)
    t = Teacher()
    print(t.class_name)
    print(t.get())
    print(t.get('2014800185'))