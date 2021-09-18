# 操作数据库类
import pymysql
from config.settings import db_cfg
from pprint import *


class MysqlUtil:
    # 初始化参数
    def __init__(self, table_name=None, my_cfg=db_cfg):
        self.db_cfg = my_cfg
        self.connection = 0
        self.table = table_name

    # 建立连接
    def connect_db(self):
        try:
            self.db = pymysql.connect(**self.db_cfg)
        except pymysql.Error as e:
            print(e)
            print('error with connect_db')
        else:
            self.connection = 1
            return self.db

    # 获得游标对象
    def get_cur(self):
        try:
            self.connect_db()
            self.cursor = self.db.cursor()
        except pymysql.Error as e:
            print(e)
            print('error with get_cur')
        else:
            return self.cursor

    # 关闭连接
    def close_db(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
        except pymysql.Error as e:
            print(e)
            print('error with close_db')
        else:
            self.connection = 0
            return True

    # 增数据一条
    def __insert_one(self, sql, value):
        try:
            handler = self.get_cur()
            res = handler.execute(sql, value)
            self.db.commit()
        except pymysql.Error as e:
            print(e)
            print('error with insert')
            self.cursor.rollback()  # 如果有错误，就回滚
        else:
            self.close_db()
            return res

    # 增数据批量
    def __insert_many(self, sql, value):
        '''
        调用这个方法，value应该是[(),(),]的形式，且[]中的元组的结构应该要相同，否则会报错。
        :param sql:
        :param value:
        :return:
        '''
        try:
            self.get_cur()  # 开连接，获取游标
            handler = self.get_cur()
            print(sql)
            print(type(value[0]))
            print(len(value[0]))
            res = handler.executemany(sql, value)
            self.db.commit()
        except pymysql.Error as e:
            # self.handler.commit()  # 如果上面的提交有错误，那么只执行对的那一个提交
            self.cursor.rollback()  # 如果有错误，就回滚
            print('error with insert')
            self.close_db()  # 发生错误就关连接
            return e
        else:
            self.close_db()  # 执行成功就关连接
            return res

    # 查数据一条
    def __get_one(self, sql, params=()):
        result = None
        try:
            self.get_cur()
            self.cursor.execute(sql, *params)
            result = self.cursor.fetchone()
            self.close_db()
        except Exception as e:
            print(e)
            self.close_db()
        return result

    # 查数据批量
    def __get_all(self, sql, params=()):
        list_data = ()
        try:
            self.get_cur()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close_db()
            return list_data
        except Exception as e:
            return e


    # 查数据批量
    def __get_many(self, sql, n=1, params=()):
        list_data = ()
        try:
            self.get_cur()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchmany(n)
            self.close_db()
        except Exception as e:
            print(e)
        return list_data

    # 更新数据
    def update(self, sql, *value):
        return "unfinished function"
        handler = self.get_cur()
        res = handler.excute(sql, *value)
        self.db.commit()
        self.close_db()
        return res

    # 删除数据
    def delete(self, sql, *value):
        return "unfinished function"
        handler = self.get_cur()
        res = handler.excute(sql, *value)
        self.db.commit()
        self.close_db()
        return res

    # 增数据批量（列表——字典）
    def insert_many_dict(self, list_dict):
        '''
        调用该方法，list_dict应该是什么[{},{},]的形式，且[]中的每个字典的格式应该相同。
        :param list_dict:
        :return:
        '''
        if isinstance(list_dict, list) and isinstance(list_dict[0], dict):
            if list_dict[0] and self.table is not None:
                insert_arg_key = list(list_dict[0].keys())
                insert_arg_key_string = ', '.join(insert_arg_key)
                insert_arg_placeholder = ', '.join(['%s' for x in insert_arg_key])
                insert_arg_value = []
                for item in list_dict:
                    value = item.values()
                    value = tuple(value)
                    insert_arg_value.append(value)
                sql = 'insert into {}({}) values({});'.format(self.table, insert_arg_key_string, insert_arg_placeholder)
                self.__insert_many(sql=sql, value=insert_arg_value)

    # 增数据批量循环调用（列表——字典）
    def insert_many_dict_loop(self, list_dict):
        if isinstance(list_dict, list):
            for item in list_dict:
                if isinstance(item, dict):
                    insert_arg_key = list(item.keys())
                    insert_arg_key_string = ', '.join(insert_arg_key)
                    insert_arg_placeholder = ', '.join(['%s' for x in insert_arg_key])
                    insert_arg_value = tuple(item.values())
                    sql = 'insert into {}({}) values({});'.format(self.table, insert_arg_key_string,
                                                                  insert_arg_placeholder)
                    self.__insert_one(sql=sql, value=insert_arg_value)
                else:
                    continue
            self.close_db()  # 执行成功关连接

    # 根据不同参数调用查数据方法并返回
    def __select_agency(self, sql, params, n=0):
        if n == 1:
            return self.__get_one(sql, params)
        elif n == 0:
            return self.__get_all(sql, params)
        else:
            return self.__get_many(sql, n, params)

    # 查数据
    def select(self, n=0, show_list=None, condition=None):
        params = ()
        if  show_list is None and condition is None:
            sql = "select * from {table}".format(table=self.table)
            return self.__select_agency(sql, params, n)

        elif show_list is None and condition is not None:
            sql = "select * from {table} where "
            if len(condition) == 1:
                sql += condition[0]
                print(sql)
            elif len(condition) > 1:
                condition_temp = ['('+i+')' for i in condition]
                cdt_or = " or ".join(condition_temp)
                sql += cdt_or
            sql = sql.format(table=self.table)
            return self.__select_agency(sql, params, n)

        elif show_list is not None and condition is None:
            if len(show_list) == 1:
                sql_key = show_list[0]
                sql = "select " + sql_key + " from {table}"
            elif len(show_list) > 1:
                sql_key = ", ".join(show_list)
                sql = "select " + sql_key + " from {table}"
            sql = sql.format(table=self.table)
            print(sql)
            return self.__select_agency(sql, params, n)

        elif show_list is not None and condition is not None:
            if len(show_list) == 1:
                sql_key = show_list[0]
                sql = "select " + sql_key + " from {table}"
            elif len(show_list) > 1:
                sql_key = ", ".join(show_list)
                sql = "select " + sql_key + " from {table} where "
            if len(condition) == 1:
                sql += condition[0]
            elif len(condition) > 1:
                condition_temp = ['('+i+')' for i in condition]
                cdt_or = " or ".join(condition_temp)
                sql += cdt_or
            sql = sql.format(table=self.table)
            print(sql)
            return self.__select_agency(sql, params, n)


def test(**value):
    print(value)


if __name__ == "__main__":
    # print(db_cfg)
    db = MysqlUtil(table_name='doclist_table')
    #
    # # print(db.db_cfg)
    # db.get_cur()
    # print(db.cursor)
    # print(db.connection)
    # db.close_db()
    # print(db.connection)
    # print(db.update())
    # di = [{'visitedTimeStr': '1', 'dueDateStr': 2, 'lightFlag': 'hello'},
    #       {'visitedTimeStr': '1', 'dueDateStr': 2, 'lightFlag': 'hello'},
    #       {'visitedTimeStr': '1', 'dueDateStr': 2, 'lightFlag': 'hello'}]
    # db.insert_many_dict(di)
    # res = db.select(n=10)
    # res = db.select(10, show_list=['typeName', 'title'], condition=["workItemId=1266344018 and titleHTML ='<span>云南电网有限责任公司后勤管理办法（修订）</span>'"])
    # res = db.select(10, show_list=['typeName', 'title'])
    res = db.select(10,condition=["workItemId=1266344018 and titleHTML ='<span>云南电网有限责任公司后勤管理办法（修订）</span>'"])
    # print(res)
    pprint(res)
