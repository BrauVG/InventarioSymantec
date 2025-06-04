Este script permite conectarse a un servidor Symantec Endpoint Protection Manager (SEPM) para extraer un listado completo de los equipos registrados. La información se guarda en un archivo Excel que incluye detalles como nombre del equipo, IP, sistema operativo y versión del cliente de Symantec.

## Requisitos previos
Acceso al servidor SEPM donde esté habilitada la API REST. Por defecto, la API responde por el puerto 8446.

Usuario con permisos sobre la API REST. El usuario debe tener permisos para autenticarse y consultar información de equipos.

Python 3.7 o superior instalado en el sistema.

Librerías necesarias:

- requests
- pandas
- openpyxl

Instalación de dependencias recomendadas:

pip install requests pandas openpyxl

## Configuración
Antes de ejecutar el script, edita las siguientes variables dentro del código:

SEPM_IP: Dirección IP o hostname del servidor SEPM
USERNAME: Usuario con permisos sobre la API
PASSWORD: Contraseña del usuario
PAGE_SIZE: Número máximo de registros por página (se recomienda usar 10000)

## Ejemplos de uso
Clona o descarga el archivo Python en tu máquina.

Abre el archivo y modifica los valores de configuración para que coincidan con tu entorno SEPM.

Ejecuta el script desde terminal o consola:

python InvSym.py

Si la autenticación es exitosa y se extraen los datos correctamente, se generará un archivo Excel llamado:

reporte_equipos.xlsx

El archivo estará en el mismo directorio donde se ejecutó el script.

## Salida esperada

El archivo reporte_equipos.xlsx tendrá las siguientes columnas por defecto:

Computer Name: nombre del equipo

IP: dirección IP asociada

Sistema Operativo: sistema operativo detectado

Deployment Version: versión del cliente de Symantec instalado

Campos adicionales disponibles
El script puede modificarse fácilmente para incluir campos opcionales

## Referencia de campos disponibles

Puedes consultar todos los campos disponibles para cada equipo en la documentación oficial de Symantec:
https://apidocs.securitycloud.symantec.com/#/doc?id=computers

## Notas adicionales
Este script está orientado a tareas de inventario, auditoría o integración con procesos automatizados. Puede adaptarse para aplicar filtros, exportar a otros formatos o integrarse con otras APIs o herramientas de monitoreo.

