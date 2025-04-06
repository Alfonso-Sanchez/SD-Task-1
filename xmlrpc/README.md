# Guía para la Ejecución de Proyectos XML-RPC

Esta guía proporciona instrucciones detalladas para ejecutar proyectos que utilizan XML-RPC.

---

## Requisitos Previos

1. **Instalar Dependencias**:
    - Asegúrate de tener instalados los siguientes componentes:
      - **Python** (versión 3.8 o superior).
    - Instala las dependencias necesarias utilizando el archivo `requirements.txt`:
      ```bash
      pip install -r requirements.txt
      ```

2. **Configurar Puertos**:
    - Verifica que los puertos necesarios estén disponibles:
      - **XML-RPC**: Define un puerto específico en tu código (por ejemplo, `8000`).
    - Si los puertos están ocupados, libera los puertos o configura otros en los archivos de configuración.

---

## Pasos para Ejecutar los Proyectos

### **Ejecución del Proyecto XML-RPC**

#### **1. Iniciar los Servidores XML-RPC**
   - Cada servidor XML-RPC debe ejecutarse en un puerto diferente. Por ejemplo:
     - Servidor 1: `8001`
     - Servidor 2: `8002`
     - Servidor 3: `8003`
   - Ejecuta los servidores en diferentes terminales:
     ```bash
     python xmlrpc_node1/xmlrpc_server1.py
     python xmlrpc_node2/xmlrpc_server2.py
     python xmlrpc_node3/xmlrpc_server3.py
     ```

#### **2. Iniciar los Clientes XML-RPC**
   - Los clientes interactúan con los servidores XML-RPC para solicitar insultos o filtrar frases:
     ```bash
     python xmlrpc_node1/xmlrpc_client.py
     ```

#### **3. Iniciar el Monitor XML-RPC**
   - El monitor muestra estadísticas en tiempo real de los servidores XML-RPC:
     ```bash
     python xmlrpc_node1/monitor.py
     ```

---

## Notas Adicionales

- **Cambiar Puertos**:
  - Si necesitas cambiar los puertos por conflictos, edita el código del servidor XML-RPC.
  - Por ejemplo, para XML-RPC, modifica el puerto en el archivo `servidor.py`:
     ```python
     server = SimpleXMLRPCServer(("localhost", 9000))
     ```

- **Logs y Depuración**:
  - Habilita logs para facilitar la depuración en caso de errores.

- **Pruebas Unitarias**:
  - Ejecuta los tests para verificar que las funcionalidades principales funcionan correctamente:
    ```bash
    python test_server_xmlrpc_node1.py
    python test_server_xmlrpc_node2.py
    python test_server_xmlrpc_node3.py
    python test_client_xmlrpc.py
    ```

---

## Orden de Ejecución Recomendado

### **Para XML-RPC**:
1. Inicia los servidores XML-RPC (`xmlrpc_server1.py`, `xmlrpc_server2.py`, etc.).
2. Inicia los clientes XML-RPC (`xmlrpc_client.py`).
3. Inicia el monitor XML-RPC (`monitor.py`).

---

Siguiendo estos pasos, deberías poder ejecutar el proyecto XML-RPC sin problemas. Si encuentras algún error, revisa los logs y asegúrate de que los puertos estén configurados correctamente.