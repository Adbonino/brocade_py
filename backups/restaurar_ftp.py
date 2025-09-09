import paramiko
import time

SWITCH_IP = '10.0.0.100'
SWITCH_USER = 'admin'
SWITCH_PASS = 'clave_switch'

SERVER_IP = '192.168.1.10'
SERVER_USER = 'backupuser'
SERVER_PASS = 'clave_backup'
BACKUP_PATH = '/home/backupuser/brocade_g720_backup.cfg'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SWITCH_IP, username=SWITCH_USER, password=SWITCH_PASS, look_for_keys=False)

shell = client.invoke_shell()
time.sleep(1)
shell.recv(1000)

shell.send('configdownload -protocol ftp\n')
time.sleep(2)
shell.send(f'{SERVER_IP}\n')
time.sleep(1)
shell.send(f'{SERVER_USER}\n')
time.sleep(1)
shell.send(f'{BACKUP_PATH}\n')
time.sleep(1)
shell.send(f'{SERVER_PASS}\n')
time.sleep(15)

output = shell.recv(50000).decode('utf-8')
print(output)

client.close()
