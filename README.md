# BROCADE - fos

Como usar: 

Creación de la configuracion con una sola zona

```
#  ansible-playbook -i inv.ini creacion_cfg.yml -e "arch_alias=../datos/alias_creacion.yml arch_zonas=../datos/zona_creacion.yml fabric_name=FABRIC_D" 
```

Agregar agunos alias y zonas a la congiuracion creada, en este caso FABRIC_D 

```
#  ansible-playbook -i inv.ini agregar_cfg.yml -e "arch_alias=../datos/alias_add.yml arch_zonas=../datos/zonas_add.yml fabric_name=FABRIC_D" 
```

Agregar todos las alias y zonas a la congiuracion creada, en este caso FABRIC_D 

```
#  ansible-playbook -i inv.ini agregar_cfg.yml -e "arch_alias=../datos/alias_new.yml arch_zonas=../datos/zonas_new.yml fabric_name=FABRIC_D" 
```
