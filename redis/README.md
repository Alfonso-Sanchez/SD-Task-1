# Guía para la Ejecución de Proyectos Redis

Esta guía proporciona instrucciones detalladas para ejecutar proyectos que utilizan Redis.

---

## Requisitos Previos

1. **Instalar Dependencias**:
    - Asegúrate de tener instalados los siguientes componentes:
      - **Python** (versión 3.8 o superior).
      - **Redis Server**.
    - Instala las dependencias necesarias utilizando el archivo `requirements.txt`:
      ```bash
      pip install -r requirements.txt
      ```

2. **Configurar Puertos**:
    - Verifica que los puertos necesarios estén disponibles:
      - **Redis**: Por defecto, utiliza el puerto `6379`.
    - Si los puertos están ocupados, libera los puertos o configura otros en los archivos de configuración.

---

## Pasos para Ejecutar los Proyectos

### **Ejecución del Proyecto Redis**

#### **1. Iniciar los Servidores Redis**
   - Cada nodo Redis debe ejecutarse en un puerto diferente. Por ejemplo:
     - Nodo 1: `6379`
     - Nodo 2: `6380`
     - Nodo 3: `6381`
   - Ejecuta los nodos en diferentes terminales:
     ```bash
     python redis_node1/server_redis_node1.py
     python redis_node2/server_redis_node2.py
     python redis_node3/server_redis_node3.py
     ```

#### **2. Iniciar el Monitor Redis**
   - El monitor muestra estadísticas en tiempo real de los nodos Redis. Ejecútalo después de iniciar los servidores:
     ```bash
     python redis_node1/monitor.py
     ```

#### **3. Iniciar el Broadcaster**
   - El broadcaster distribuye insultos a los nodos Redis. Ejecútalo después de iniciar los servidores y el monitor:
     ```bash
     python redis_node1/broadcaster.py
     ```

#### **4. Iniciar los Clientes Redis**
   - Los clientes interactúan con los nodos Redis para solicitar insultos o filtrar frases.
   - Cliente Redis:
     ```bash
     python redis_node1/client_redis.py
     ```
   - Cliente Filter:
     ```bash
     python redis_node1/client_filter.py
     ```

---

## Notas Adicionales

- **Cambiar Puertos**:
  - Si necesitas cambiar los puertos por conflictos, edita los archivos de configuración del servidor Redis (`redis.conf`).
  - Por ejemplo, para Redis:
     ```bash
     redis-server --port 6380
     ```

- **Logs y Depuración**:
  - Habilita logs para facilitar la depuración en caso de errores.

- **Pruebas Unitarias**:
  - Ejecuta los tests para verificar que las funcionalidades principales funcionan correctamente:
    ```bash
    python test_server_redis_node1.py
    python test_server_redis_node2.py
    python test_server_redis_node3.py
    python test_client_redis.py
    ```

- **Reiniciar Redis**:
  - Si necesitas limpiar los datos de Redis, puedes reiniciar el servidor Redis:
    ```bash
    redis-cli FLUSHALL
    ```

---

## Orden de Ejecución Recomendado

### **Para Redis**:
1. Inicia los servidores Redis (`server_redis_node1.py`, `server_redis_node2.py`, etc.).
2. Inicia el monitor (`monitor.py`).
3. Inicia el broadcaster (`broadcaster.py`).
4. Inicia el cliente Redis (`client_redis.py`).
5. Inicia el cliente Filter (`client_filter.py`).

---

Siguiendo estos pasos, deberías poder ejecutar el proyecto Redis sin problemas. Si encuentras algún error, revisa los logs y asegúrate de que los puertos estén configurados correctamente.