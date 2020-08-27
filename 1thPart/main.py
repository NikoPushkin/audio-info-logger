from tinkoff_voicekit_client import ClientSTT
import argparse
import sys

from custom_exceptions import *
from jsonschema import exceptions as clientSTT_exceptions
from grpc import _channel
from psycopg2 import OperationalError

from services import _check_audio_stage, \
                     _create_unique_id, \
                     _record_recognized_audio_in_file, \
                     _delete_wav_file, \
                     _execute_queries

from model import initial_sql_operators

from config import API_KEY, \
                    SECRET_KEY, \
                    audio_config, \
                    parameters_from_terminal, \
                    logger


def get_response_with_recognized_file(audio_config: dict, path: str):
    """Функция обеспечивает распознавание голоса и возвращает результат"""

    try:
        # сожержит распознанный текст и параметры аудио
        response = client.recognize(path, audio_config)
        return response
    except ValueError as err:
        logger.error(err)
        raise PathException('Path is incorrected, please check it and try again')
    except clientSTT_exceptions.ValidationError as err:
        logger.error(err)
        raise AudioConfigException('\nPlease, check audio configuration parameters')
    except _channel._InactiveRpcError as err:
        logger.error(err)
        raise AuthException('\nPlease, check API KEY and SECRETE KEY in config.py')

if __name__ == '__main__':
    # создаст необходимые таблицы в БД, если их нет
    try:
        _execute_queries(initial_sql_operators)
    except OperationalError as err:
        logger.error(err)
        raise DBConfigException(
            '\nPlease, check values in db configuration (config.py/db_config)'
            )

    client = ClientSTT(API_KEY, SECRET_KEY)

    response = get_response_with_recognized_file(
            audio_config=audio_config,
            path=parameters_from_terminal.path
            )
    # Извлекает распознанный текст для дальнейшей записи
    text_body = response[0]['alternatives'][0]['transcript']

    _, call_result = _check_audio_stage(
            text_body=text_body,
            stage_value=parameters_from_terminal.call_stage
            )
    _record_recognized_audio_in_file(
            response=response, call_result=call_result,
            parameters=parameters_from_terminal, text_body=text_body
            )
    _delete_wav_file(path_to_file=parameters_from_terminal.path)
