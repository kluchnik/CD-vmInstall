'''Параметры подключения'''

def get_type() -> str:
  ''' Возвращает тип подключения: bash | ssh '''
  return 'ssh'

def get_ssh_cfg() -> dict:
  '''
  Возвращает параметры подключения по ssh
  Также подключение по ssh можно выполнить с использованием ключа,
  для этого необходимо выполнить команду: ssh-copy-id <Имя пользователя>@<IP-адрес>
  При этом пароль может иметь любое значение
  '''
  ssh_cfg = {
    'hostname': '10.0.5.172',
    'port': 22,
    'username': 'user',
    'password': '12345678'
  }
  return ssh_cfg
