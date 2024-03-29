import logging

import DataLoader as dl
import DataHandler as dh
import Factory

import sql_func 
from settings import SETTINGS
from sql_queries import *


DATA_LOADERS = {
    'json': dl.JSONLoader,
}
DATA_HANDLERS = {
    'json': dh.JSONHandler,
    'xml': dh.XMLHandler,
}
data_loader_factory = Factory.ObjectFactory()
data_handler_factory = Factory.ObjectFactory()
for key, builder in DATA_LOADERS.items():
    data_loader_factory.register_builder(key, builder)
for key, builder in DATA_HANDLERS.items():
    data_handler_factory.register_builder(key, builder)


def main(students_filename, rooms_filename, out_format, db_settings):
    in_format = 'json'

    loader = data_loader_factory.create(in_format)
    handler = data_handler_factory.create(out_format)
    
    try:
        rooms = loader.load(rooms_filename) 
        students = loader.load(students_filename)
    except FileNotFoundError as e:
        logging.error(e)
        return

    for query in CREATE_TABLE_QUERIES_SQL:
        sql_func.create_table(**query, SETTINGS=db_settings)

    for query in CREATE_INDEX_SQL:
        sql_func.execute_query(query, SETTINGS=db_settings)
    
    sql_func.dump_data(
        'rooms',
        ('id','name'),
        rooms,
        SETTINGS=db_settings,
    )
    sql_func.dump_data(
        'students',
        ('id','name','birthday','room','sex'),
        students,
        SETTINGS=db_settings,
    )
    
    for task_num, query in enumerate(SELECT_QUERIES_SQL, 1):
        result = sql_func.execute_query(query, SETTINGS=db_settings)
        handler.write(result, 'task'+str(task_num)+'.'+out_format)


def create_argparser():
    
    import argparse  

    parser = argparse.ArgumentParser(description='Process some json files.')
    parser.add_argument('students_file_path',
                        type=str,
                        help='Path to the students file.')
    parser.add_argument('rooms_file_path',
                        type=str,
                        help='Input path to the students file.')
    parser.add_argument('out_format',
                        type=str,
                        help='Choice the output format')
    
    parser.add_argument('--host',
                        type=str,
                        default=f"{SETTINGS['host']}",
                        help=f"Choice the host, (default: {SETTINGS['host']}")
    parser.add_argument('--user',
                        type=str,
                        default=f"{SETTINGS['user']}",
                        help=f"Choice the username, (default: {SETTINGS['host']}")
    parser.add_argument('--password',
                        type=str,
                        default=f"{SETTINGS['password']}",
                        help=f"Choice the username, (default: {SETTINGS['password']}")
    parser.add_argument('--database',
                        type=str,
                        default=f"{SETTINGS['database']}",
                        help=f"Choice the username, (default: {SETTINGS['database']}")
    return parser 


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()
    db_settings = {
        'host': args.host,
        'user': args.user,
        'password': args.password,
        'database': args.database,
    }
    main(args.students_file_path, args.rooms_file_path, args.out_format, db_settings)