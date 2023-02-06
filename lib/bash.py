'''
Выполнение команд в оболочке bash

Пример использования:

>>> import lib.bash

>>> lib.bash.exec_cmd('echo тест')
{'stdin': 'echo тест', 'stdout': 'тест\\n', 'stderr': ''}

>>> lib.bash.exec_cmd('echo тест', False)
{
  'stdin': 'echo тест',
  'stdout': b'\\xd1\\x82\\xd0\\xb5\\xd1\\x81\\xd1\\x82\\n',
  'stderr': b''
}

>>> cmd = \'''
... whoami
... pwd
... \'''

>>> lib.bash.exec_cmd(cmd)
{
  'stdin': '\\nwhoami\\npwd\\n',
  'stdout': 'user\\n/home/user/CI-QA-rub\\n',
  'stderr': ''
}
'''

import subprocess
import os

def exec_cmd(cmd:str, decode:bool=True, fdecode:str='utf8') -> dict:
  ''' Выполнение комманды bash и вывод результата в dict '''
  try:
    dialog = subprocess.Popen(['/bin/bash', '-c', cmd],
             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = dialog.communicate()
  except Exception as exc:
    out, err = '', exc
  if decode:
    result = {
      'stdin': cmd,
      'stdout': out.decode(fdecode),
      'stderr': err.decode(fdecode)
      }
  else:
    result = {
      'stdin': cmd,
      'stdout': out,
      'stderr': err
    }
  return result


def get_dir() -> dict:
  ''' Вывод полного пути
  out:
      {
        master - полный путь до основной директории где находятся все файлы
        lib - полный путь до директории lib
      }
  '''
  path_file = os.path.abspath(__file__)
  cdir = '/'.join(path_file.split('/')[:-1])
  mdir = '/'.join(path_file.split('/')[:-2])
  result = {
    'master': mdir,
    'lib': cdir
  }
  return result
