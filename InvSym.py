import requests
import pandas as pd
import os

# Configuración del SEPM (debes definir estas variables)
SEPM_IP = "127.0.0.1"      # IP o hostname del SEPM
USERNAME = "usuario"       # Usuario SEPM
PASSWORD = "Password"    # Contraseña SEPM
PAGE_SIZE = 10000            # Tamaño de página para paginación

def obtener_token():
    """Autentica en SEPM y obtiene un token de acceso."""
    url = f"https://{SEPM_IP}:8446/sepm/api/v1/identity/authenticate"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}

    # Desactiva advertencias por certificados SSL no verificados
    requests.packages.urllib3.disable_warnings()

    response = requests.post(url, headers=headers, json=payload, verify=False)

    if response.status_code == 200:
        token = response.json().get("token")
        print(f"Token obtenido correctamente.")
        return token
    else:
        print(f"Error al obtener token: {response.status_code} - {response.text}")
        return None

def obtener_todos_los_equipos(token):
    """Obtiene la información de todos los equipos desde SEPM usando paginación y guarda los resultados en un archivo Excel."""
    page_index = 1
    equipos = []

    while True:
        print(f"Procesando página {page_index}...")
        api_endpoint = f"https://{SEPM_IP}:8446/sepm/api/v1/computers?pageIndex={page_index}&pageSize={PAGE_SIZE}"
        
        response = requests.get(
            api_endpoint,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            verify=False
        )

        if response.status_code != 200:
            print(f"Error en la consulta: {response.status_code} - {response.text}")
            break

        data = response.json()
        computers = data.get("content", [])

        # Extrae datos relevantes de cada equipo
        for comp in computers:
            nombre = comp.get("computerName", "Desconocido")
            ip = ", ".join(comp.get("ipAddresses", ["No disponible"]))
            so = comp.get("operatingSystem", "No disponible")
            version = comp.get("deploymentRunningVersion", "No disponible")
            """
            #Opcional: puedes incluir más campos útiles como los siguientes:
            macs = ", ".join(comp.get("macAddresses", []))  # Dirección MAC
            hardware_key = comp.get("hardwareKey", "No disponible")  # Clave única del hardware
            domain_name = comp.get("domainName", "No disponible")  # Nombre de dominio
            last_update = comp.get("lastUpdateTime", "No disponible")  # Última vez que se actualizó
            group_name = comp.get("groupName", "No disponible")  # Nombre del grupo al que pertenece
            os_version = comp.get("osVersion", "No disponible")  # Versión exacta del sistema operativo
            online_status = comp.get("onlineStatus", "Desconocido")  # Estado en línea/desconectado

            # parametros disponibles:
            https://apidocs.securitycloud.symantec.com/#/doc?id=computers
            """

            equipos.append({
                "Computer Name": nombre,
                "IP": ip,
                "Sistema Operativo": so,
                "Deployment Version": version
                # Descomenta los campos que desees incluir en el Excel:
                # "MAC Address": macs,
                # "Hardware Key": hardware_key,
                # "Domain Name": domain_name,
                # "Última Actualización": last_update,
                # "Grupo": group_name,
                # "Versión OS": os_version,
                # "Estado": online_status
            })

        # Verifica si hay más páginas por procesar
        if page_index >= data.get("totalPages", 1):
            break
        page_index += 1

    # Guardar resultados en archivo Excel
    df = pd.DataFrame(equipos)
    salida_excel = "reporte_equipos.xlsx"
    ruta_completa = os.path.abspath(salida_excel)
    df.to_excel(ruta_completa, index=False)
    print(f"Archivo generado en: {ruta_completa}")

# Ejecutar el script
if __name__ == "__main__":
    token = obtener_token()
    if token:
        obtener_todos_los_equipos(token)