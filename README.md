<h1>Программа для распознавания аудио-файлов и записи полученной информации в базу данных Postgre.</h1>

<ul><h2>Для установки и работы:</h2>

<li><h4>Клонировать репозиторий:</h4>
  
```
git clone https://github.com/NikoPushkin/audio-info-logger
```

</li>
<li><h4>Запустить install.sh с указанием интерпретатора:</h4>

```
./install.sh
```

</li>
<li><h4>Указать все необходимые ключи для работы с API в config.py</h4></li>

<li><h4>Указать необходимые настройки распознавания в config.py/audio_config</h4></li>

<li><h4>Указать необходимые настройки для базы данных в config.py/db_config</h4></li>
</ul>


<h4> Программа запускается через терминал вызовом основного файла "main.py" с передачей ряда обязательных параметров, описание которых необходимо получить через:
  
  ```
  python main.py -h
  ```
  
Все файлы, в которые ведется служебная запись находятся в папке log_files.
<br>
Описание схемы и основные команды для работы с БД находятся в файле model.py</h4>
