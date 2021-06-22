#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import json
import dataSource

items = {'teachers': {'name': '全体在职教师',
                      'titles': ['工号', '单位号', '所在科室', '姓名', '性别', '出生地', '身份证件号', '政治面貌', '职称', '联系电话', '办公电话', '工作状态',
                                 '职务'],
                      'sql': """SELECT GH,DWH,SZKS,XM,XBM,CSDM,SFZJH,ZZMMM,ZC,LXDH,BGDH,GZZT,ZW 
                FROM DLAKE_PERSONNEL_TEACHER_ALL  WHERE GH='2014800185' or GH='2010800037'"""},
         'department': {'name': '部门信息',
                        'titles': ['单位号', '上级单位号', '单位名称', '单位可用标识'],
                        'sql': """SELECT dwh,lsdwh,dwmc,dwyxbs FROM DLAKE_PERSONNEL_DEPARTMENT"""},
         }


class Item:
    def __init__(self, ):
        self.


data = dataSource.select(sql)


def toJson(titles, data):
    dic = [dict(zip(titles, i)) for i in data]
    res = json.dumps(dic, ensure_ascii=False, indent=4, separators=(',', ': '))

    return res
