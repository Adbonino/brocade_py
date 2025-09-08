# BROCADE - fos

## tools

### creacion.py

Uso: script.py host usuario clave fabric_name alias_add.yml zonas_add.yml

```
# python creacion.py 10.1.1.10 admin pass FABRIC_D ../datos/alias.yml ../zonas.yml
```

### creacion.py

Uso: script.py host usuario clave fabric_name alias_add.yml zonas_add.yml

```
# python agregar.py 10.1.1.10 admin pass FABRIC_D ../datos/alias.yml ../zonas.yml
```

## formato de archivos

archivo de alias:

```
aliases:
  - name:   AIX73_DELFOS_DESA_v1_fcs1   
    wwn:    c0:50:76:0b:c3:a3:00:24
  - name:   AIX73_DELFOS_DESA_v2_fcs1  
    wwn:    c0:50:76:0b:c3:a3:00:26
  - name:   AIX73_DWH_HML_v1_fcs1   
    wwn:    c0:50:76:0b:c3:a3:00:2e
  - name:   AIX73_DWH_HML_v2_fcs1   
    wwn:    c0:50:76:0b:c3:a3:00:2c
  - name:   AIX73_DWH_PRD_34   
    wwn:    c0:50:76:0b:c3:a3:00:34
...
```

Archivo de zonas: 

```
ones:       
  - name:   AIX72_ORCLX_DESA_v2_fcs4_V9000   
    members:   
      - AIX72_ORCLX_DESA_v2_fcs4      
      - SVC_V9000_N1_PORT_7_2      
      - SVC_V9000_N2_PORT_7_2      
      - SVC_V9000Conti_N1_PORT_3_3      
      - SVC_V9000Conti_N1_PORT_4_4
  - name: AIX72_ORCLX_PROD_V1_fcs1_V7300   
    members:   
      - Orclx72_Prod_VIOS1_Fcs1      
      - V7300F_N1_PORT4      
      - V7300F_N2_PORT4      
      - V7300F_N3_PORT4      
      - V7300F_N4_PORT4   
  - name:   AIX72_ORCLX_PROD_V2_fcs1_V7300   
    members:   
     - Orclx72_Prod_VIOS2_Fcs1      
     - V7300F_N1_PORT4      
     - V7300F_N2_PORT4      
     - V7300F_N3_PORT4      
     - V7300F_N4_PORT4
...
```

