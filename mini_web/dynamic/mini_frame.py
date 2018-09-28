import re
import pymysql
import random
dic={}
def route(url):
    def func(fun):
        dic[url]=fun
        def callfun():
            return fun()
        return callfun
    return func
@route('index.py')
def index():
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='mysql', database='Feng',
                               charset='utf8')#database 用你自己建的数据库的位置
        cur = conn.cursor()
        cur.execute('select name from group_name;')#python08 用你自己建的数据表的位置
        student_info = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        body = student_info[random.randint(0,8)][0]
        print(body)
        return body


def application(env, set_header):
    status = '200 OK\r\n'
    response_headers = [('Content-Type', 'text/html; charset=utf-8')]
    set_header(status, response_headers)
    file_name = env['file_name']
    if file_name in dic:
        return dic[file_name]()
    else:
        return 'dynamic request not found'
