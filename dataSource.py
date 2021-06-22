#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# !/usr/bin/env python3
# -*- coding:utf-8 -*-


import cx_Oracle
import pymysql
import pymssql
import sqlite3
import json

# test data
connect = {
    '教务': {'dbtype': 'oracle', 'account': 'zfxfzb/zfsoft_hqwy@orcl', 'is_sysdba': 0},
    '学工': {'dbtype': 'sqlserver', 'account': 'lx/Hqwy@edu2016/192.168.2.78', 'is_sysdba': 0},
    '迎新': {'dbtype': 'sqlserver', 'account': 'lx/Hqwy@edu2016/192.168.2.78', 'is_sysdba': 0},
    '中心库': {'dbtype': 'oracle', 'account': 'dbm/comsys123@dbm', 'is_sysdba': 0},
    '招生': {'dbtype': 'sqlserver', 'account': 'lx/Hqwy@edu2016/192.168.2.78', 'is_sysdba': 0},
    '离校': {'dbtype': 'sqlserver', 'account': 'lx/Hqwy@edu2016/192.168.2.78', 'is_sysdba': 0},
    '人事': {'dbtype': 'sqlserver', 'account': 'lx/Hqwy@edu2016/192.168.2.78', 'is_sysdba': 0},
    '数据湖': {'dbtype': 'oracle', 'account': 'dbm/comsys123/dbm', 'is_sysdba': 0},
}


class Database:
    def __init__(self, dbtype, account: str, is_sysdba=0):
        self.dbtype = dbtype
        self.account = account
        self.is_sysdba = is_sysdba

        if dbtype == 'oracle':
            if is_sysdba:
                self.connect = cx_Oracle.connect(account, mode=cx_Oracle.SYSDBA)
            else:
                self.connect = cx_Oracle.connect(account)
        elif dbtype == 'mysql':
            account = account.split('/')
            self.connect = pymysql.connect(host=account[-1], user=account[0], password=account[1])
        elif dbtype == 'sqlserver':
            account = account.split('/')
            self.connect = pymssql.connect(host=account[-1], user=account[0], password=account[1])
        elif dbtype == 'sqlite':
            self.connect = sqlite3.connect(self.account)

    def connClose(self):
        """创建类时会直接创建数据库连接，在执行完操作之后需要用该函数关闭数据库连接"""
        self.connect.close()

    def signin(self, dbtype, account: str, is_sysdba=0):
        """也可手动得到数据库连接的类"""
        if dbtype == 'oracle':
            if is_sysdba:
                conn = cx_Oracle.connect(account, mode=cx_Oracle.SYSDBA)
            else:
                conn = cx_Oracle.connect(account)
        elif dbtype == 'mysql':
            account = account.split('/')
            conn = pymysql.connect(host=account[-1], user=account[0], password=account[1])
        elif dbtype == 'sqlserver':
            account = account.split('/')
            conn = pymssql.connect(host=account[-1], user=account[0], password=account[1])
        elif dbtype == 'sqlite':
            conn = sqlite3.connect(self.account)
        else:
            return None

        return conn

    def query(self, sql) -> list:
        """查询数据，返回全部结果"""
        cursor = self.connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        return result

    def update(self, sql):
        """修改并查询修改结果，修改成功则返回True"""
        cursor = self.connect.cursor()
        # update
        cursor.execute(sql)
        cursor.close()
        self.connect.commit()

        # 查询比对修改结果
        cursor = self.connect.cursor()
        select_sql, value = self.updata2select(sql)
        cursor.execute(select_sql)
        result = cursor.fetchall()
        cursor.close()

        # print(result[0][0])
        # print(value)
        if result and result[0][0] == value:
            return True
        else:
            return False

    def updata2select(self, updata_sql) -> tuple:
        """将uptdata语句转换为select语句，用于修改后的查询"""
        words = updata_sql.split()
        upper_words = list(map(lambda x: x.upper(), words))

        if 'UPDATE' in upper_words and 'SET' in upper_words and 'WHERE' in upper_words:
            table = words[upper_words.index('UPDATE') + 1]
            conditional = ' '.join(words[upper_words.index('WHERE') + 1:])
            set = words[upper_words.index('SET') + 1]
            key = set.split('=')[0]
            value = set.split('=')[1].replace('\'', '')

        else:
            return None

        select_sql = "SELECT %s FROM %s WHERE %s" % (key, table, conditional)
        return select_sql, value


def select(sql):
    db = Database(**connect['中心库'])
    res = db.query(sql)
    db.connClose()
    return res


if __name__ == '__main__':
    # s = db.query("SELECT PASSWORD FROM uiadata.ut_users WHERE LOGINID='2014800185' AND CARDID='220103198903232171'")
    # u = db.update("update uiadata.ut_users set password='670b14728ad9902aecba32e22fa4f6bd'
    #                   WHERE LOGINID='2014800185' AND CARDID='220103198903232171'"))

    s = r"SELECT GH,DWH,SZKS,XM,XBM,CSDM,SFZJH,ZZMMM,ZC,LXDH,BGDH,GZZT,ZW " \
        r"FROM DLAKE_PERSONNEL_TEACHER_ALL  WHERE GH='2014800185' or GH='2010800037'"

    a = select(s)
    for i in a:
        print(i)
