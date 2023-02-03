'''Параметры подключения'''

def get_type() -> str:
  ''' Возвращает тип подключения: bash | ssh '''
  return 'ssh'

def get_ssh_cfg():
  ''' Возвращает параметры подключения по ssh '''
  ssh_cfg = {
    'hostname': '10.0.5.172',
    'port': 22,
    'username': 'user',
    'password': '12345678'
  }
  return ssh_cfg