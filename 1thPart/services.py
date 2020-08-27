import random
import datetime
import soundfile as sf
import os
from model import insert_query, PostgreConnection
from config import log_folder_dir


def _check_audio_stage(text_body: dict, stage_value: int):
    """Функция проверяет значение этапа и определяет соответствующие параметры"""
    if stage_value == 1:
        if 'автоответчик' in text_body:
            return (0, 'AO')
        else:
            return (1, 'человек')
    else:
        if 'нет' or 'неудобно' in text_body:
            return (0, 'отрицательно')
        else:
            return (1, 'положительно')


def _create_unique_id():
    """Создает уникальный ID для записей в файле"""
    id = random.getrandbits(16)
    while True:
        yield id
        id += 1


def _get_sound_duration(filename: str):
    """Функцию возвращает продолжительность аудио в секундах"""
    file = sf.SoundFile(filename)
    return len(file) / file.samplerate


def _record_recognized_audio_in_file(
                            response: dict, call_result: str,
                            parameters, text_body: str
                            ):
    """Записывает данные о распознанном файле в файл"""
    date_and_time = datetime.datetime.now().strftime(
                                    '%Y-%m-%d, %H:%M:%S'
                                    )
    record_id = next(_create_unique_id())
    phone_number = parameters.phone
    call_duration = _get_sound_duration(parameters.path)
    record_body = str('{}, {}, {}, {}, {}, {}\n'.format(
                        date_and_time, record_id, call_result,
                        phone_number, call_duration, text_body
                        )
                    )
    _context_manager_function(log_folder_dir + 'container.log',
                                                record=record_body)
    # Записывает полученную информацию в БД при соответствии флага
    if parameters.db_Flag == 1:
        _context_manager_function(log_folder_dir + 'temp_container',
                                                record_body, mode='w')
        _execute_queries(insert_query)
    else:
        pass


def _execute_queries(list_of_queries):
    """Выполняет команды, полученные в виде списка"""
    with PostgreConnection() as conn:
        connection = conn.connector
        cursor = conn.cursor
        try:
            for query in list_of_queries:
                cursor.execute(query)
        except Exception as err:
            print(err)


def _delete_wav_file(path_to_file: str):
    """Удаляет файл, с которым была проведена операция"""
    os.remove(path_to_file)


def _context_manager_function(filename: str, record, mode='a'):
    """Запускает контекстный менеджер с
    необходимым файлом и заданными параметрами"""
    with open(filename, mode) as f:
        f.write(record)
