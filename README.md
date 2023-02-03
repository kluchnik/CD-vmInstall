# CD-vmInstall
## Автоматическая развёртывание стенда на виртуальных машинах

### Описание функционирования

Даннный скрип выполняет следующие действия:  
* Подключается (через bash или ssh) к ОС на базе Linux для выполнение команд, параметры подключения задаются в файле ```config.connect```
* Выполнение заданного набора скриптов написанных на bash, набор скриптов задается в файле ```config.scripts```
* Заданные скрипты выполняются последовательно (наборы preinstall, install, postinstall), условием завершения является: оканчание всех скриптов из набора или появление ошибки в ```stderr``` при выполнение скрипта

Подключение через bash:  
![img not found](img/work_1.png "Подключение через bash")  
Подключение через ssh:  
![img not found](img/work_2.png "Подключение через ssh")  

### Установка зависимостей
```
apt install python3
apt install python3-pip

pip3 install -r requirements.txt
```

### Запуск

Запуск с настройками по умолчанию (в качестве параметров соединения будут использоватся файл ```config.connect```, в качестве набора скриптов будет использоватся файл ```config.scripts```)
```
pytest --maxfail=1 ./vmInstaller.py
```
Запуск с настройками по умолчанию (в качестве параметров соединения будут использоватся файл ```config.connect```, в качестве набора скриптов будет использоватся файл ```config.scripts```) с выводом ```stdin```, ```stdout```, ```stderr``` для каждого теста:
```
pytest -s --maxfail=1 ./vmInstaller.py
```
Запуск с переопределением файла с набором скриптов:
```
pytest --maxfail=1 ./vmInstaller.py --scripts config.scripts
```
Запуск с переопределением файла параметров соединения и набора скриптов:
```
pytest --maxfail=1 ./vmInstaller.py --connect config.connect --scripts config.scripts
```

### Архитектура проекта

| Объект | Описание |
| - | - |
| ![img not found](img/ico_vmInstall.png) | Скрипт запуска процедуры выполнения скриптов |
| - | !img not found](img/vmInstall_1.png) |
| ![img not found](img/ico_conftest.png) | Формирование параметров подключения и наборов скриптов |
| - | ![img not found](img/conftest_1.png) |
| ![img not found](img/ico_config_connect.png) | Формирование параметров подключения и наборов скриптов |
| - | ![img not found](img/config_connect_1.png) |
| ![img not found](img/ico_config_scripts.png) | Формирование параметров подключения и наборов скриптов |
| - | ![img not found](img/config_scripts_1.png) |
| - | ![img not found](img/config_scripts_2.png) |
| - | ![img not found](img/config_scripts_3.png) |
| ![img not found](img/ico_lib_bash.png) | Выполнение команд через bash |
| ![img not found](img/ico_lib_ssh.png) | Выполнение команд через ssh |
