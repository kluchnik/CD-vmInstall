# CD-vmInstall
## Автоматическая развёртывание стенда на виртуальных машинах

### Описание функционирования

Даннный скрип выполняет следующие действия:  
* Подключается (через bash или ssh) к ОС на базе Linux для выполнение команд, параметры подключения задаются в файле ```config.connect```
* Выполнение заданного набора скриптов написанных на bash, набор скриптов задается в файле ```config.scripts```
* Заданные скрипты выполняются последовательно (наборы preinstall, install, postinstall), условием завершения является: оканчание всех скриптов из набора или появление ошибки в ```stderr``` при выполнение скрипта

### Установка зависимостей
```
apt install python3
apt install python3-pip

pip3 install -r requirements.txt
```

### Запуск

```

```

### Архитектура проекта