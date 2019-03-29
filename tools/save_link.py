# coding=utf8
import time, datetime
import sqlite3, json

link_file = './static/link_file.sqlite'
data_store_path = './static/data/'
model_store_path = './static/model/'
sql_insert = """INSERT INTO {tableName} ( model_id, data_id, data_path,model_path,update_time) VALUES ( {model_id}, {data_id}, {data_path},{model_path},{update_time})"""

create_table_sql = """
CREATE TABLE link
(
    id INTEGER PRIMARY KEY NOT NULL,
    data_id varchar ,
    model_id varchar ,
    data_path varchar ,
    model_path varchar ,
    update_time varchar
);
"""


def execute_sqlite(sqlfile, sql, fetch=False):
    res = None
    with sqlite3.connect(sqlfile) as conn:
        c = conn.cursor()
        if fetch:
            res = c.execute(sql).fetchall()
        else:
            c.execute(sql)

        conn.commit()

        return res


def insert_data(sqlfile, model_id, data_id, model_path=model_store_path, data_path=data_store_path, tableName='link'):
    sql_comm = sql_insert.format(tableName=tableName, model_id=json.dumps(model_id), data_id=json.dumps(data_id),
                                 model_path=json.dumps(model_path),
                                 data_path=json.dumps(data_path),
                                 update_time=json.dumps(today()))
    print(sql_comm, json.dumps(model_path))
    return execute_sqlite(sqlfile, sql_comm)


def today(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.today().strftime(fmt)


if __name__ == '__main__':
    sqlfile = 'link_file.sqlite'
    model_id = '1213'
    data_id = '12312'

    print(insert_data(sqlfile, model_id, data_id))

    pass
