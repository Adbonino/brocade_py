#!/usr/bin/env python3
import paramiko
import time
import yaml
import sys

def read_until_prompt(channel, prompt="switch_fabric_D1:FID128:admin>"):
    buffer = ""
    while True:
        if channel.recv_ready():
            output = channel.recv(1024).decode('utf-8')
            buffer += output
            if buffer.strip().endswith(prompt): # leo hasta que aparece el prompt al final del output.
                print("Saliendo de read_until_prompt")
                break
        else:
            # Si no hay datos, espera un poco para no consumir CPU innecesariamente
            time.sleep(0.1)
    return buffer

# Verificamos que se pasaron suficientes argumentos
if len(sys.argv) != 7:
    print("Uso: script.py host usuario clave fabric_name alias_add.yml zonas_add.yml")
    sys.exit(1)

# === Configuración de conexión ===
host = sys.argv[1]
usuario = sys.argv[2]
clave = sys.argv[3]
fabric_name = sys.argv[4]
arch_alias = sys.argv[5]
arch_zonas = sys.argv[6]

print("*************************************")
print("Iniciando proceso ...")
print("Cargando archivos ...")
# === Cargar aliases desde YAML ===
with open(arch_alias, "r") as file:
    data = yaml.safe_load(file)
    aliases = data.get("aliases", [])

# === Cargar zonas ===
with open(arch_zonas , "r") as file:
    zona_data = yaml.safe_load(file)
    zonas = zona_data.get("zones", [])

print("*************************************")
print("Abriendo Conexion ...")
# === Conexión SSH ===
cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cliente.connect(hostname=host, username=usuario, password=clave, look_for_keys=False, allow_agent=False)
shell = cliente.invoke_shell()
time.sleep(1)

# Limpiar buffer inicial
if shell.recv_ready():
    shell.recv(1000)

print("*************************************")
print("Creaondo Alias ...")
# === Crear alias en bucle ===
for alias in aliases:
    nombre = alias["name"]
    wwn = alias["wwn"]
    comando = f'alicreate "{nombre}", "{wwn}"'
    shell.send(comando + "\n")
    time.sleep(1)

print("*************************************")
print("Creando Zonas ...")
# === Crear zonas en bucle ===
for zona in zonas:
    zona_name = zona["name"]
    miembros = zona["members"]

    if miembros:
        #miembros_str = ";".join(f'"{m}"' for m in miembros)
        miembros_str = ";".join(f'{m}' for m in miembros)
        comando = f'zonecreate "{zona_name}", "{miembros_str}"'
        shell.send(comando + "\n")
    time.sleep(1)


print("*************************************")
print("Agregando Zonas a la  configuracion ...")
# === Crear cgf ===
# switch:admin> cfgadd "Test_cfg", "greenzone;bluezone"
zonas_str =  ";".join(f'{m["name"]}' for m in zonas)
comando = f' cfgadd "{fabric_name}", "{zonas_str}"'
print(comando)
shell.send(comando + "\n")
output = read_until_prompt(shell, prompt="admin>")

print("fin de comando cfgadd")

print("*************************************")
print("Guardando configuracion ...")
# === Guardar configuración ===
shell.send("cfgsave\n")

output = ""
while True:
    if shell.recv_ready():
        output += shell.recv(5000).decode("utf-8")
        print(output.strip())
    # Responder al prompt si es necesario
    if "Do you want to save" in output:
        print("↪ Respondiendo 'y' al prompt de cfgsave...")
        shell.send("y\n")
        break
    time.sleep(0.1)

print("*************************************")
print("Habilitando configuracion ...")
# === enable configuración ===
shell.send(f'cfgenable "{fabric_name}"\n')
time.sleep(5)

output = ""
while True:
    if shell.recv_ready():
        output += shell.recv(5000).decode("utf-8")
    # Responder al prompt si es necesario
    if "Do you want to enable" in output:
        print("↪ Respondiendo 'y' al prompt de cfgsave...")
        shell.send("y\n")
        break
    time.sleep(0.1)


print("*************************************")
print("Cerrando configuracion ...")
# === Cerrar sesión ===
shell.send("exit\n")
cliente.close()
print("*************************************")
print("Operación finalizada.")
print("*************************************")
print("...")
