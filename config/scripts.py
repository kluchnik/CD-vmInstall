'''
Скрипты которые необходимо выполнить на хосте
'''

# ===========================================================
# Параметры для формирования списка скриптов
# ===========================================================

def get_preinstall() -> tuple:
  ''' preinstall - список bash-скриптов до установки '''
  return (
    check_cpu64, check_cpu_virt, check_cpu_ihw, check_kvm_mod,
    check_pkgs, download, create_bridges, show_bridges,
    network_config
    )

def get_install() -> tuple:
  ''' install - список bash-скриптов установки '''
  return (
    vm_stop, vm_del_snapshots, vm_delete,
    vm_1_install,
    waiting_install
    )

def get_postinstall() -> tuple:
  ''' postinstall - спсиок bash-скриптов после установки '''
  return (
    enable_forward, vm_add_snp, iptables_flash, iptables_add_prert,
    iptables_add_postrt, iptables_show, vm_start
    )

# ===========================================================
# Префикс для комманд
# ===========================================================
# Префикс для команд определеят утилиту перед командой, например: '', 'sudo'
pref_cmd = 'sudo'

# ===========================================================
# Проверка поддержки аппаратной виртуализации
# ===========================================================

check_cpu64 = '''
cpu_64=$( {0} egrep -wo 'lm' /proc/cpuinfo | uniq )
if [[ -z ${{cpu_64}} ]];
  then echo 'Поддержка CPU 64bit - ERROR' >> /dev/stderr
  else echo 'Поддержка CPU 64bit - OK'
fi
'''.format(pref_cmd)

check_cpu_virt = '''
cpu_virt=$( {0} lscpu | grep 'Virtualization:' )
if [[ -z ${{cpu_virt}} ]];
  then echo 'Поддержка виртуализации - ERROR' >> /dev/stderr
  else echo 'Поддержка виртуализации - OK'
fi
'''.format(pref_cmd)

check_cpu_ihw = '''
cpu_hwv=$( {0} egrep -wo 'vmx' /proc/cpuinfo | uniq )
if [[ -z ${{cpu_hwv}} ]];
  then echo 'Поддержка Intel hardware виртуализации - ERROR' >> /dev/stderr
  else echo 'Поддержка Intel hardware виртуализации - OK'
fi
'''.format(pref_cmd)

check_kvm_mod = '''
kvm_modules=$( {0} lsmod | grep -i kvm )
if [[ -z ${{kvm_modules}} ]];
  then echo 'Наличие подключенного kvm модуля - ERROR' >> /dev/stderr
  else echo 'Наличие подключенного kvm модуля - OK'
fi
'''.format(pref_cmd)

# ===========================================================
# Проверка установленных зависимостей на хосте
# ===========================================================
PKGs = 'iptables wget python3 python3-pip chromium \
qemu qemu-system-x86 libvirt-clients bridge-utils libvirt-daemon-system \
libguestfs-tools genisoimage virtinst libosinfo-bin'

check_pkgs = '''
PKGs='{}'
for pkg in ${{PKGs}}; do 
  pkg_status=$( dpkg -s ${{pkg}} 2>&1 | grep Status );
  if [[ -z ${{pkg_status}} ]];
    then echo "Наличие пакета: ${{pkg}} - ERROR" >> /dev/stderr
    else echo "Наличие пакета: ${{pkg}} - OK"
  fi;
done
'''.format(PKGs)

# ===========================================================
# Загрузка внешних файлов по URL
# ===========================================================
# Example:
# URLs = '''
# URLs[0]='https://test.ru/1/download /tmp/rubicon1.iso'
# URLs[1]='https://test.ru/2/download /tmp/rubicon2.iso'
# '''
URLs = '''
'''

download = '''
declare -A URLs
{1}
for item in ${{!URLs[@]}}; do
  parameters=(${{URLs[$item]}})
  url=${{parameters[0]}}
  path=${{parameters[1]}}
  {0} rm -f ${{path}}
  {0} wget --no-check-certificate --quiet -O ${{path}} ${{url}}
  if [[ $? -eq 0 ]];
    then echo "Скачивание ${{url}} -> ${{path}} - OK"
    else echo "Скачивание ${{url}} -> ${{path}} - ERROR" >> /dev/stderr
  fi
done
'''.format(pref_cmd, URLs)

# ===========================================================
# Создание сетевых мостов для подключения виртуальной машины
# ===========================================================
BRIDGES = 'none vmbr1 vmbr2 vmbr3'

create_bridges = '''
echo 'Создание сетевых мостов:'

bridges='{1}'
cmd_brctl='{0} /usr/sbin/brctl'

for bridge in ${{bridges}}; do
  find_br=$(${{cmd_brctl}} show | grep ${{bridge}} | awk '{{print $1}}')
  if [[ ${{bridge}} == ${{find_br}} ]];
  then
    echo "${{bridge}} - сетевой мост уже существует"
  else
    ${{cmd_brctl}} addbr ${{bridge}}
    if [[ $? -eq 0 ]];
      then echo "${{bridge}} - создание сетевого моста - OK"
      else echo "${{bridge}} - создание сетевого моста - ERROR" >> /dev/stderr
    fi
  fi
done
'''.format(pref_cmd, BRIDGES)

# ===========================================================
# Просмотр сетевых мостов
# ===========================================================

show_bridges = '''
echo 'Полный список сетевых мостов:'
{0} /usr/sbin/brctl show
'''.format(pref_cmd)

# ===========================================================
# Настройка сети
# ===========================================================

NETs = '''
declare -A NETs
NETs[0]='vmbr1 192.168.1.101/24'
NETs[1]='vmbr2 192.168.2.100/24'
NETs[2]='vmbr3 192.168.3.100/24'
'''

network_config = '''
echo "Выполнение сетевой настройки:"
{1}
for item in ${{!NETs[@]}}; do
  parameters=(${{NETs[$item]}})
  if_name=${{parameters[0]}}
  if_net=${{parameters[1]}}
  {0} ip link set dev ${{if_name}} up
  {0} ip a flush dev ${{if_name}}
  {0} ip a change dev ${{if_name}} ${{if_net}}
  if [[ $? -eq 0 ]];
  then
    echo "${{if_name}} -> ${{if_net}} - OK"
    {0} ip a show dev ${{if_name}};
  else
    echo "${{if_name}} -> ${{if_net}} - ERROR" >> /dev/stderr
  fi
done
'''.format(pref_cmd, NETs)

# ===========================================================
# Конфигурация виртуальной машины виртуальной машины
# ===========================================================

VM1 = {
  'name': 'rubicon',
  'iso': '/tmp/rubicon.iso',
  'disk': '/home/user/qemu/disk.qcow2',
  'com_port': '4001',
  'net1': 'bridge:vmbr1',
  'net2': 'bridge:none',
  'net3': 'bridge:none',
  'net4': 'bridge:none',
  'net5': 'bridge:none',
  'net6': 'bridge:none',
}

VMs_install = (VM1, )

VMs_name = tuple(map(lambda x: x['name'], VMs_install))
VMs_disk = tuple(map(lambda x: x['disk'], VMs_install))

# ===========================================================
# Остановка виртуальных машин
# ===========================================================

vm_stop_old = '''
for vm in {1}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} " | awk '{{print $3}}')
  {0} virsh destroy ${{vm}} 2>&1
done
'''.format(pref_cmd, ' '.join(VMs_name))

vm_stop = '''
for vm in {1}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} " | awk '{{print $3}}')
  if [[ "${{status_vm}}" == "работает" || "${{status_vm}}" == "running" ]];
  then
    echo "Выключение виртуальной машины ${{vm}}"
    {0} virsh destroy ${{vm}}
  else
    echo "Виртуальная машина ${{vm}} выключина"
  fi
done
'''.format(pref_cmd, ' '.join(VMs_name))

# ===========================================================
# Удаление snapshot виртуальных машин
# ===========================================================

vm_del_snapshots = '''
for vm in {1}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} ")
  if [[ -z ${{status_vm}} ]];
  then
    echo 'Виртуальная машина ${{vm}} - отсутсует'
  else
    snapshots=$({0} virsh snapshot-list ${{vm}} | sed '1,2d' | awk '{{print $1}}')
    for sp_name in ${{snapshots}}; do
      echo "Удаление snapshot ${{vm}} - ${{sp_name}}" 
      {0} virsh snapshot-delete ${{vm}} --metadata ${{sp_name}}
    done
  fi
done
'''.format(pref_cmd, ' '.join(VMs_name))

# ===========================================================
# Удаление виртуальных машин
# ===========================================================

vm_delete = '''
for vm in {1}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} " | awk '{{print $3}}')
  if [[ "${{status_vm}}" == "выключен" || "${{status_vm}}" == "shut off" ]]; then
    echo "Удаление виртуальной машины ${{vm}}"
    {0} virsh undefine ${{vm}}
  fi
done
'''.format(pref_cmd, ' '.join(VMs_name))

# ===========================================================
# Установка виртуальной машины
# ===========================================================

vm_1_install = '''
echo "Запуск установки виртуальной машины: {name}" 
{0} virt-install --connect qemu:///system \
  --name {name} \
  --hvm \
  --virt-type kvm \
  --arch x86_64 \
  --memory 2048 \
  --vcpus 1 \
  --boot menu=on,useserial=on \
  --os-type linux \
  --os-variant generic \
  --disk path={disk},size=10,bus=sata,snapshot=external \
  --cdrom {iso} \
  --network {net1},model=e1000,mac=00:50:DA:82:8A:01 \
  --network {net2},model=e1000,mac=00:50:DA:82:8A:02 \
  --network {net3},model=e1000,mac=00:50:DA:82:8A:03 \
  --network {net4},model=e1000,mac=00:50:DA:82:8A:04 \
  --network {net5},model=e1000,mac=00:50:DA:82:8A:05 \
  --network {net6},model=e1000,mac=00:50:DA:82:8A:06 \
  --nographics \
  --serial tcp,host=0.0.0.0:{com_port},mode=bind,protocol=telnet \
  --console pty,target_type=serial \
  --autoconsole none \
  --autostart
if [[ $? -eq 0 ]];
  then echo "Установка виртуальной машины {name} - OK"
  else echo "Установка виртуальной машины {name} - ERROR" >> /dev/stderr
fi
'''.format(pref_cmd, **VM1)

# ===========================================================
# Ожидание завершения установки виртальной машины
# ===========================================================

# Время ожидания установки в минутах
waiting_time = 60

waiting_install = '''
echo 'Ожидание установки виртуальных машин'

# Подсчет реального количества виртуальных машин
number_of_rvm=0
for vm in {2}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} ")
  if [[ -z ${{status_vm}} ]];
    then echo "Виртуальная машина ${{vm}} отсутсвует" >> /dev/stderr
    else let number_of_rvm+=1
  fi
done

# Ожидание установки ВМ машин
finished=0
for item in {{1..{1}}}; do
  for vm in {2}; do
    status_vm=$({0} virsh list --all | grep "${{vm}} " | awk '{{print $3}}')
    if [[ "${{status_vm}}" == "выключен" || "${{status_vm}}" == "shut off" ]]; then
      echo "Виртуальная машина ${{vm}} установлена"
      let finished+=1
    fi
  done
  if [[ ${{finished}} -eq ${{number_of_rvm}} ]]; then
    break
  fi
  if [[ ${{item}} -eq {1} ]]; then
    echo "Превышено время ожидания установки ВМ > ${1} мин" >> /dev/stderr
    break
  fi
  sleep 60
done
'''.format(pref_cmd, waiting_time, ' '.join(VMs_name))

# ===========================================================
# Создание snapshot дисков ВМ
# ===========================================================

vm_add_snp = '''
for item in {{1..{1}}}; do
  name=$(echo {2} | awk -v n=${{item}} '{{print $n}}')
  disk=$(echo {3} | awk -v n=${{item}} '{{print $n}}')
  if [[ -f ${{disk}} ]]; then
    {0} qemu-img create -f qcow2 -b ${{disk}} ${{disk}}.work 2>&1
    {0} virt-xml ${{name}} --edit target=sda --disk driver_type=qcow2,path=${{disk}}.work
  fi
done
'''.format(pref_cmd, len(VMs_name), ' '.join(VMs_name), ' '.join(VMs_disk))

# ===========================================================
# Включение режима forward
# ===========================================================

enable_forward = '''
{0} bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
{0} sed -i 's/#net.ipv4.ip_forward=0/net.ipv4.ip_forward=1/' /etc/sysctl.conf
{0} sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
{0} sed -i 's/net.ipv4.ip_forward=0/net.ipv4.ip_forward=1/' /etc/sysctl.conf
{0} sysctl -w net.ipv4.ip_forward=1
{0} sysctl -p
status_forward=$({0} sysctl net.ipv4.ip_forward | awk '{{print $3}}')
if [[ ${{status_forward}} -eq 0 ]];
  then echo "Опция ядра ip_forward = ${{status_forward}}" >> /dev/stderr
  else echo "Опция ядра ip_forward = ${{status_forward}}"
fi
'''.format(pref_cmd)

# ===========================================================
# Очистка IPTables
# ===========================================================

iptables_flash = '''
{0} iptables -t nat -F PREROUTING
{0} iptables -t nat -F POSTROUTING
'''.format(pref_cmd)

# ===========================================================
# Добавление правил IPTables для доступа к виртуальным машинам
# ===========================================================

iptables_add_prert = '''
{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 8001 -j DNAT --to-destination 192.168.1.1:8443
{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 2201 -j DNAT --to-destination 192.168.1.1:22

{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 8002 -j DNAT --to-destination 192.168.2.1:8443
{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 2202 -j DNAT --to-destination 192.168.2.1:22

{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 8003 -j DNAT --to-destination 192.168.3.1:8443
{0} iptables -t nat -A PREROUTING -d 0.0.0.0/0 -p tcp \
--dport 2203 -j DNAT --to-destination 192.168.3.1:22
'''.format(pref_cmd)

iptables_add_postrt = '''
{0} iptables -t nat -A POSTROUTING -p tcp --dport 8443 -j MASQUERADE
{0} iptables -t nat -A POSTROUTING -p tcp --dport 22 -j MASQUERADE
'''.format(pref_cmd)

# ===========================================================
# Просмотр IPTables
# ===========================================================

iptables_show = '''
{0} iptables -t nat -L PREROUTING
{0} iptables -t nat -L POSTROUTING
'''.format(pref_cmd)

# ===========================================================
# Запуск виртуальных машин
# ===========================================================

vm_start = '''
for vm in {1}; do
  status_vm=$({0} virsh list --all | grep "${{vm}} " | awk '{{print $3}}')
  if [[ "${{status_vm}}" == "выключен" || "${{status_vm}}" == "shut off" ]]; then
    echo "Запуск виртуальной машины ${{vm}}"
    {0} virsh start ${{vm}}
  fi
done
'''.format(pref_cmd, ' '.join(VMs_name))
