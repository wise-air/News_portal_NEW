# Настройки логгирования по заданию13.4

Настройки логгирования согласно задания 13.4
В файле Settings.py
Строки: 73-186

При установке DEBUG = False (строка 30) необходимо также раскомментировать allowed hosts в строке 32

Для проверки логгирования
News/Views.py
Строки: 32-45
Url для принудительного вызова лога:
http://127.0.0.1:8000/news/log_view/
