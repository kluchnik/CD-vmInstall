'''
Выполнение удаленных команд по ssh

Для работы необходимо установить paramiko: pip3 install paramiko

Пример использования:

>>> import lib.ssh
>>> pc = lib.ssh.UNION()
>>> ssh_cfg = {
... 'hostname': '10.0.4.213',
... 'port': 22,
... 'username': 'user',
... 'password': '12345678'
... }
>>> pc.set_connParam(**ssh_cfg)
True
>>> pc.connect()
True

>>> cmd = \'''
... whoami
... ls /var/
... echo 'test msg 1'
... echo
... run_not_cmd
... echo 'test msg 2'
... \'''

>>> pc.run_command(cmd)
True

>>> pc.get_line_std('stdin')
"\\nwhoami\\nls /var/\\necho 'test msg 1'\\necho 'run_not_cmd'\\n
echo 'test msg 2'"

>>> pc.get_line_std('stdout')
"user\\nbackups\\ncache\\nlib\\nlocal\\nlock\\nlog\\nmail\\n 
opt\\nrun\\nspool\\ntmp\\ntest msg 1\\n\\ntest msg 2\\n)

>>> pc.get_line_std('stderr')
"bash: line 5: run_not_cmd: command not found\\n"

>>> pc.disconnect()
True

P.S. Подключится можно с использованием ключа, для этого необходимо выполнить команду:
$ ssh-copy-id <Имя пользователя>@<IP-адрес>

'''

import paramiko

class UNION():
  ''' Удаленое выполнение ssh команд'''
  def __init__(self):
    self.__ssh = paramiko.SSHClient()
    self.__connect = {
      'hostname': '127.0.0.1',
      'port': '22',
      'username': 'user',
      'password': '12345678'}
    self.__line_stdin = ''
    self.__line_stdout = ''
    self.__line_stderr = ''
    self.__type_command = None

  def set_hostname(self, hostname:str) -> None:
    ''' Задать hostname '''
    self.__connect['hostname'] = hostname

  def set_port(self, port:str) -> None:
    ''' Задать порт '''
    self.__connect['port'] = port

  def set_password(self, password:str) -> None:
    ''' Задать пароль '''
    self.__connect['password'] = password

  def set_username(self, username:str) -> None:
    ''' Задать пароль '''
    self.__connect['username'] = username

  def set_connParam(self, **kwarg) -> None:
    '''
    Задать новое значение параметрам:
    example-1: <class>.set_parameters(hostname='192.168.1.11', login='user', password='12345678')
    example-2: <class>.set_parameters(**{'hostname':'192.168.1.11', 'login':'user', 'password':'12345678'})
    '''
    status = False
    try:
      for item in kwarg.keys():
        self.__connect[item] = kwarg[item]
      status = True
    except Exception as exc:
      stderr = 'ERROR: failed set connect parameters:\n{}'.format(exc)
      self.set_line_std('stderr', stderr)
      status = False
    return status

  def get_connParam(self) -> dict:
    ''' Вернуть параметры соединения '''
    return self.__connect
    
  def get_sConnParam(self, select:str) -> str:
    ''' Вернуть выбранный параметр соединения
    in:
        select: ['hostname'|'port'|'username'|'password']
    '''
    if select == 'hostname':
      connParam = self.__connect['hostname']
    elif select == 'port':
      connParam = self.__connect['port']
    elif select == 'username':
      connParam = self.__connect['username']
    elif select == 'password':
      connParam = self.__connect['password']
    else:
      connParam = ''
    return connParam

  def get_line_std(self, select:str='stdout') -> tuple:
    ''' Вернуть ввод std
    in:
        select: ['stdin'|'stdout'|'stderr']
    '''
    if select == 'stdin':
      return self.__line_stdin
    elif select == 'stdout':
      return self.__line_stdout
    elif select == 'stderr':
      return self.__line_stderr
    else:
      return ()

  def connect(self) -> bool:
    ''' Соединение по ssh '''
    try:
      self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.__ssh.connect(hostname=self.__connect['hostname'], 
        port=self.__connect['port'],
        username=self.__connect['username'], 
        password=self.__connect['password'])
      return True
    except Exception as exc:
      stderr = 'ERROR: failed to connect via ssh:\n{}'.format(exc)
      self.set_line_std('stderr', stderr)
      return False

  def disconnect(self) -> bool:
    ''' Разрыв соединения по ssh '''
    if self.__ssh:
      self.__ssh.close()
    return True

  def set_line_std(self, select:str, std:str, fdecode:str='utf8') -> None:
    ''' Задать значение ssh вывода
    in:
        select: ['stdin'|'stdout'|'stderr']
        std: str
    '''
    if isinstance(std, bytes):
      std_list = std.decode(fdecode)
    elif isinstance(std, str):
      std_list = std
    else:
      std_list = ('ERROR: format not defined',)
    # set std -> stdin | stdout | stderr
    if select == 'stdin':
      self.__line_stdin = std_list
    elif select == 'stdout':
      self.__line_stdout = std_list
    elif select == 'stderr':
      self.__line_stderr = std_list

  def run_command(self, cmd:str) -> bool:
    ''' Выполнение команд по ssh '''
    status = False
    try:
      _, ssh_stdout, ssh_stderr = self.__ssh.exec_command(str(cmd))
      stdin = cmd
      stdout = ssh_stdout.read()
      stderr = ssh_stderr.read()
      status = True
    except Exception as exc:
      stdin = cmd
      stdout = ''
      stderr = 'ERROR: commands cannot be executed:\n{}'.format(exc)
      status = False
    self.set_line_std('stdin', stdin)
    self.set_line_std('stdout', stdout)
    self.set_line_std('stderr', stderr)
    return status

  def run_command_daemon(self, cmd:str) -> bool:
    ''' Выполнение команды без вывода в режиме демона '''
    status = False
    try:
      _, _, _ = self.__ssh.exec_command(cmd)
      status = True
    except Exception as exc:
      stdin = cmd
      stdout = ''
      stderr = 'ERROR: commands cannot be executed:\n{}'.format(exc)
      self.set_line_std('stdin', stdin)
      self.set_line_std('stdout', stdout)
      self.set_line_std('stderr', stderr)
      status = False
    return status

def exec_cmd(cmd:str, ssh_cfg:dict) -> dict:
  ''' Выполнеие bash команд по ssh
    cmd = 'whoami'
    ssh_cfg = {
      'hostname': '10.0.4.213',
      'port': 22,
      'username': 'user',
      'password': '12345678'
    }
    out: {'stdout': 'user\\n', 'stderr': ''}
  '''
  pc = UNION()
  if pc.set_connParam(**ssh_cfg):
    if pc.connect():
      _ = pc.run_command(cmd)
      _ = pc.disconnect()
  return {
    'stdout': pc.get_line_std('stdout'),
    'stderr': pc.get_line_std('stderr')
  }
