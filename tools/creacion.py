#!/usr/bin/env python3
import paramiko
import time
import yaml
import sys


# Verificamos que se pasaron suficientes argumentos
if len(sys.argv) != 7:
    print("Uso: script.py host usuario clave fabric_name alias_add.yml zonas_add.yml")
    sys.exit(1)

# === Configuración de variables ===
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
with open(arch_alias , "r") as file:
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
print("Creando Alias ...")
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
        # miembros_str = ";".join(f'"{m}"' for m in miembros)
        miembros_str = ";".join(f'{m}' for m in miembros)
        comando = f'zonecreate "{zona_name}", "{miembros_str}"'
        enviar_comando(shell, comando)
    time.sleep(1)


print("*************************************")
print("Creando configuracion ...")
# === Crear cgf ===
# switch:admin> cfgcreate "USA_cfg","Purple_zone;Blue_zone;Green_zone"
zonas_str =  ";".join(f'{m["name"]}' for m in zonas)
comando = f'cfgcreate "{fabric_name}", "{zonas_str}"'
print(comando)
enviar_comando(shell, comando)

print("*************************************")
print("Guardando configuracion ...")
# === Guardar configuración ===
shell.send("cfgsave\n")
time.sleep(5)

output = ""
if shell.recv_ready():
    output = shell.recv(5000).decode("utf-8")
    print(output.strip())

# Responder al prompt si es necesario
if "Do you want to save" in output:
    shell.send("y\n")
    time.sleep(2)

output += shell.recv(5000).decode('utf-8')
print(output)

print("*************************************")
print("Habilitando configuracion ...")
# === enable configuración ===
shell.send(f'cfgenable "{fabric_name}"\n')
time.sleep(5)

output = ""
if shell.recv_ready():
    output = shell.recv(5000).decode("utf-8")
    print(output.strip())

# Responder al prompt si es necesario
if "Do you want to enable" in output:
    print("↪ Respondiendo 'y' al prompt de cfgsave...")
    shell.send("y\n")
    time.sleep(2)

output += shell.recv(5000).decode('utf-8')
print(output)

print("*************************************")
print("Cerrando sesion ...")
# === Cerrar sesión ===
shell.send("exit\n")
cliente.close()
print("*************************************")
print("Operación finalizada.")
print("*************************************")
print("...")
