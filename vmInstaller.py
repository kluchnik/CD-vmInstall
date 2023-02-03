'''
Сценарий развертывания виртуальных машин
Запуск:
$: pytest --maxfail=1 ./vmInstaller.py
$: pytest -s --maxfail=1 ./vmInstaller.py
$: pytest --maxfail=1 ./vmInstaller.py --scripts config.scripts
$: pytest --maxfail=1 ./vmInstaller.py --connect config.connect --scripts config.scripts
'''

import pytest
import lib.bash
import lib.ssh

def exec_cmd(type_connect:str, cmd:str, ssh_cfg:dict={}) -> dict:
  ''' Выполнеие bash команд в зависимости от типа подключения bash | ssh '''
  if type_connect == 'bash':
    return lib.bash.exec_cmd(cmd)
  elif type_connect == 'ssh':
    return lib.ssh.exec_cmd(cmd, ssh_cfg)
  else:
    exit(1)

def print_result(input_txt:dict) -> None:
  ''' Вывод текста в stdout '''
  try:
    print('> stdin:\n', input_txt['stdin'])
    print('> stdout:\n', input_txt['stdout'])
    print('> stderr:\n', input_txt['stderr'])
    print('-'*40)
  except:
    print(input_txt)

def test_exec_cmd(connect:dict, scripts:tuple) -> None:
  ''' Подключение в соответсвии с connect и выполнение scripts '''
  type_connect = connect['type_connect']
  ssh_cfg = connect['ssh_cfg']
  result = exec_cmd(type_connect, scripts, ssh_cfg)
  result['stdin'] = scripts
  print_result(result)
  assert result['stderr'] == ''
