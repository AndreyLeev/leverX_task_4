import pymysql


def create_table(table_name, create_table_sql, SETTINGS):
    connection = pymysql.connect(**SETTINGS)
    try:
        with connection.cursor() as cursor:    
            cursor.execute(create_table_sql)
        connection.commit()
    finally:
        connection.close()


def dump_data(table_name, data_labels, data, SETTINGS):
    connection = pymysql.connect(**SETTINGS)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM {}".format(table_name))
            values = ",".join(["%({})s".format(label) for label in data_labels]) 
            sql = "INSERT INTO {} VALUES ({})".format(table_name, values)
            cursor.executemany(sql, data) 
        connection.commit()
    finally:
        connection.close()


def execute_query(sql_query, SETTINGS):
    connection = pymysql.connect(**SETTINGS)
    result = ()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
    finally:
        connection.close()
        return result
