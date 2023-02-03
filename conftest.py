import importlib

def pytest_addoption(parser):
  parser.addoption("--connect", action="store", default="config.connect")
  parser.addoption("--scripts", action="store", default="config.scripts")

def pytest_generate_tests(metafunc):
  # This is called for every test. Only get/set command line arguments
  # if the argument is specified in the list of test "fixturenames".
  option_value = metafunc.config.option.connect
  if 'connect' in metafunc.fixturenames and option_value is not None:
    #metafunc.parametrize("connect", [option_value])
    m_connect = importlib.import_module(option_value)
    type_connect = m_connect.get_type()
    try:
      ssh_cfg = m_connect.get_ssh_cfg()
    except:
      ssh_cfg = {}
    connect = {
      'type_connect': type_connect,
      'ssh_cfg': ssh_cfg
    }
    metafunc.parametrize("connect", (connect, ))

  option_value = metafunc.config.option.scripts
  if 'scripts' in metafunc.fixturenames and option_value is not None:
    #metafunc.parametrize("scripts", [option_value])
    m_scripts = importlib.import_module(option_value)
    preinstall = m_scripts.get_preinstall()
    install = m_scripts.get_install()
    postinstall = m_scripts.get_postinstall()
    scripts = preinstall + install + postinstall
    metafunc.parametrize("scripts", scripts)