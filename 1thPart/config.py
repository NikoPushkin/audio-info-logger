import sys
import logging
import argparse
import os


# пути к базовым директориям
base_dir = os.path.dirname(__file__)
log_folder_dir = base_dir + '/log_files/'

# Ключи для доступа к API
API_KEY = ''
SECRET_KEY = ''

# Конфигурация для распознавания файла
audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

# Настройки аргументов командной строки
parser = argparse.ArgumentParser(prog='Voice message recognizer',
                                            conflict_handler='resolve')
parser.add_argument('path', type=str,help='Specify path to audio file')
parser.add_argument('phone', type=str, help='Specify phone number')
parser.add_argument('db_Flag', type=int, choices=range(0,2),
    help='Use 1 or 0 to define is it necesarry to record in database or not')
parser.add_argument('call_stage', type=int, choices=range(1,3),
    help='Use 1 or 2 to define stage of call - greeting or continuing')
parameters_from_terminal = parser.parse_args()

# Настройки логера
logging.basicConfig(filename=log_folder_dir + 'exeptions.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger = logging.getLogger(__name__)


# Настройки базы данных
db_config = """ user=user
                password=password
                host=host
                port=port
                dbname=dbname """
