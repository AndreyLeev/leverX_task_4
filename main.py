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


def main(students_filename, rooms_filename, out_format):
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
        sql_func.create_table(**query, SETTINGS=SETTINGS)

    for query in CREATE_INDEX_SQL:
        sql_func.execute_query(query, SETTINGS=SETTINGS)
    
    sql_func.dump_data('rooms',('id','name'),rooms, SETTINGS=SETTINGS)
    sql_func.dump_data('students',('id','name','birthday','room','sex'), students, SETTINGS=SETTINGS)
    
    for task_num, query in enumerate(SELECT_QUERIES_SQL, 1):
        result = sql_func.execute_query(query, SETTINGS=SETTINGS)
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
    return parser 


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()
    main(args.students_file_path, args.rooms_file_path, args.out_format)