import psycopg2
from config import base_dir, db_config

class PostgreConnection(object):
    """Класс-менеджер соединения.
    Открывает и закрывает соединение с сервером БД"""
    def __init__(self, db_config=db_config):
        self.db_config = db_config
        self.connector = None

    def __enter__(self):
        self.connector = psycopg2.connect(self.db_config)
        self.cursor = self.connector.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.connector.commit()
        else:
            print ("Error while connecting to PostgreSQL", exc_tb)
            self.connector.rollback()
        self.cursor.close()
        self.connector.close()
        print("PostgreSQL connection is closed")

# Команда для создания двух дополнительных таблиц project и server
server_and_project_tables_query = """
                            CREATE TABLE IF NOT EXISTS project(
                                    id SERIAL PRIMARY KEY,
                                    name varchar(30),
                                    description text
                            );
                            CREATE TABLE IF NOT EXISTS server(
                                    id SERIAL PRIMARY KEY,
                                    name varchar(30),
                                    ip_adress text,
                                    description text
                            );"""

# Команда для создания основной таблицы для записи параметров аудио
main_table_query = """
                            CREATE TABLE IF NOT EXISTS audio_parameters_list(
                                    date date,
                                    time time,
                                    id   integer PRIMARY KEY,
                                    call_result varchar(30),
                                    phone_number text,
                                    audio_duration real,
                                    text_body text,
                                    project_id integer REFERENCES project(id),
                                    server_id integer REFERENCES server(id)
                            );"""
                            
# список команд для создания базовых таблиц для работы приложения
initial_sql_operators = [server_and_project_tables_query,
                        main_table_query]

# Команда для копирования данных в таблицу из временного файла
record_result_to_db = """
                            COPY audio_parameters_list (
                                    date, time, id, call_result,
                                    phone_number, audio_duration, text_body)
                                    FROM '{}/log_files/temp_container'
                                    DELIMITER ',';
                            """.format(base_dir)
# Список, для выполнения команд в цикле
insert_query = [record_result_to_db]
