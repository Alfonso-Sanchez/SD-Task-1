# Documentación: Práctica RabbitMQ Multi-Node (2 Nodos)

Esta documentación explica cómo configurar y ejecutar un proyecto basado en RabbitMQ con dos nodos servidores (`server1.py` y `server2.py`), un broadcaster de insultos (`broadcaster.py`), un cliente que envía y recibe frases filtradas (`client_filter.py`), un cliente que solicita insultos (`insult_client.py`), un monitor centralizado de estadísticas (`stats_monitor.py`) y pruebas automatizadas (`test_servers.py`). El sistema usa un entorno virtual de Python y RabbitMQ como sistema de mensajería.

La fecha actual considerada para esta documentación es **31 de marzo de 2025**.

---

## 1. Configuración del Entorno Virtual en Python

### Paso 1: Crear el entorno virtual
Abre una terminal en el directorio raíz del proyecto y ejecuta:
```bash
python -m venv venv
```
Esto creará una carpeta `venv` con el entorno virtual.

### Paso 2: Activar el entorno virtual
Activa el entorno según tu sistema operativo:
- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/MacOS**:
```bash
source venv/bin/activate
```
Verás `(venv)` en la terminal si se activa correctamente.

### Paso 3: Instalar dependencias de Python
Instala las dependencias listadas en `requirements.txt`:
```bash
pip install -r requirements.txt
```
Contenido de `requirements.txt`:
```
pika==1.3.2
```

### Paso 4: Instalar RabbitMQ con Docker
El proyecto utiliza RabbitMQ como sistema de mensajería. Sigue estos pasos para instalarlo con el plugin de gestión (`rabbitmq-management`) usando Docker:

1. **Asegúrate de tener Docker instalado**: Verifica ejecutando `docker --version`. Si no lo tienes, instálalo desde [docker.com](https://www.docker.com/get-started).
2. **Ejecuta RabbitMQ con el plugin de gestión**:
   En una terminal, ejecuta el siguiente comando para iniciar un contenedor de RabbitMQ:
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```
   - `-d`: Ejecuta el contenedor en segundo plano.
   - `--name rabbitmq`: Nombra el contenedor como "rabbitmq".
   - `-p 5672:5672`: Expone el puerto de mensajería AMQP.
   - `-p 15672:15672`: Expone el puerto de la interfaz web de gestión.
   - `rabbitmq:3-management`: Usa la imagen oficial con el plugin de gestión habilitado.
3. **Verifica que RabbitMQ esté corriendo**:
   - Abre un navegador y visita `http://localhost:15672`. Usa las credenciales por defecto: usuario `guest`, contraseña `guest`.
   - Si no carga, verifica el estado del contenedor con `docker ps` y asegúrate de que esté activo.
4. **Detener RabbitMQ (opcional)**:
   Para detener el contenedor cuando termines:
   ```bash
   docker stop rabbitmq
   ```

### Paso 5: Desactivar el entorno (opcional)
Cuando termines, desactiva el entorno con:
```bash
deactivate
```

---

## 2. Ejecución del Código

El proyecto tiene seis componentes ejecutables: dos servidores (`server1.py` y `server2.py`), el broadcaster (`broadcaster.py`), el cliente de filtrado (`client_filter.py`), el cliente de insultos (`insult_client.py`) y el monitor de estadísticas (`stats_monitor.py`). Sigue este orden para ejecutarlos.

### 2.1. Ejecutar los Servidores

#### Servidor 1 (`server1.py`)
Procesa insultos de `insultos1`, filtra frases de `filtrar1` y responde solicitudes de `insultame1`.

En una terminal (con el entorno activado y RabbitMQ corriendo), ejecuta:
```bash
python server1.py
```
- Escucha `insultos1`, `filtrar1` y `insultame1`, publica en `filtradas1`, `insultar1` y `stats`.
- Muestra estadísticas locales con curses.
- Usa `Ctrl+C` para detenerlo.

#### Servidor 2 (`server2.py`)
Procesa insultos de `insultos2`, filtra frases de `filtrar2` y responde solicitudes de `insultame2`.

En otra terminal (con el entorno activado), ejecuta:
```bash
python server2.py
```
- Escucha `insultos2`, `filtrar2` y `insultame2`, publica en `filtradas2`, `insultar2` y `stats`.
- Muestra estadísticas locales con curses.
- Usa `Ctrl+C` para detenerlo.

### 2.2. Ejecutar el Broadcaster (`broadcaster.py`)
Envía insultos aleatorios a las colas `insultos1` y `insultos2`.

#### Paso 1: Iniciar el broadcaster
En otra terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python broadcaster.py
```
- Envía un insulto cada 5 segundos (ej. "Tonto.", "Gilipollas.", "Maricon").
- Usa `Ctrl+C` para detenerlo.

### 2.3. Ejecutar el Cliente de Filtrado (`client_filter.py`)
Envía frases a `filtrar1` o `filtrar2` y recibe las versiones filtradas de `filtradas1` o `filtradas2`.

#### Paso 1: Iniciar el cliente de filtrado
En otra terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python client_filter.py
```
- Envía frases aleatorias (ej. "Edu es Tonto.", "Eres un Gilipollas.") y muestra las respuestas filtradas.
- Usa `Ctrl+C` para detenerlo.

### 2.4. Ejecutar el Cliente de Insultos (`insult_client.py`)
Solicita insultos a `insultame1` o `insultame2` y recibe respuestas de `insultar1` o `insultar2`.

#### Paso 1: Iniciar el cliente de insultos
En otra terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python insult_client.py
```
- Solicita insultos aleatoriamente a uno de los servidores y muestra las respuestas.
- Usa `Ctrl+C` para detenerlo.

### 2.5. Ejecutar el Monitor de Estadísticas (`stats_monitor.py`)
Muestra estadísticas centralizadas de ambos servidores desde la cola `stats`.

#### Paso 1: Iniciar el monitor
En otra terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python stats_monitor.py
```
- Muestra estadísticas de "Servidor1" y "Servidor2" en una interfaz curses.
- Usa `Ctrl+C` para detenerlo.

---

## 3. Ejecución de las Pruebas

El archivo de pruebas (`test_servers.py`) verifica el comportamiento de ambos servidores con conexiones reales a RabbitMQ.

### Paso 1: Asegurarse de que los servidores estén corriendo
Ejecuta `server1.py` y `server2.py` como se describe en la sección 2.1.
Ejecuta `broadcaster.py` como se describe en la seccion 2.2.
### Paso 2: Ejecutar las pruebas
En una terminal (con el entorno activado y RabbitMQ corriendo), ejecuta:
```bash
python -m unittest test_servers.py
```
- **Pruebas para Server1**:
  - Solicitar un insulto desde `insultame1` y verificar la respuesta.
  - Filtrar una frase con insulto desde `filtrar1`.
  - Filtrar una frase sin insulto desde `filtrar1`.
- **Pruebas para Server2**:
  - Solicitar un insulto desde `insultame2` y verificar la respuesta.
  - Filtrar una frase con insulto desde `filtrar2`.
  - Filtrar una frase sin insulto desde `filtrar2`.

### Notas adicionales
- Las pruebas pre-pueblan las colas `insultos1` y `insultos2` con datos de prueba.
- Si un servidor no está activo, las pruebas correspondientes fallarán por falta de respuesta.

---

## Notas Finales
- **Requisitos**: Python 3.8 o superior, Docker para RabbitMQ.
- **Estructura sugerida**:
  - `broadcaster.py`: Envía insultos a ambos servidores.
  - `client_filter.py`: Envía y recibe frases filtradas de ambos servidores.
  - `server1.py`: Servidor 1 (procesa `insultos1`, `filtrar1`, `insultame1`).
  - `server2.py`: Servidor 2 (procesa `insultos2`, `filtrar2`, `insultame2`).
  - `insult_client.py`: Solicita insultos a ambos servidores.
  - `stats_monitor.py`: Monitor centralizado de estadísticas.
  - `test_servers.py`: Pruebas para ambos servidores.
  - `requirements.txt`: Dependencias optimizadas.
- **Flujo típico**:
  1. Inicia RabbitMQ con Docker (`docker run ...`).
  2. Inicia ambos servidores (`python server1.py` y `python server2.py`).
  3. Inicia el broadcaster (`python broadcaster.py`), el cliente de filtrado (`python client_filter.py`), el cliente de insultos (`python insult_client.py`) y el monitor (`python stats_monitor.py`).
  4. Opcionalmente, ejecuta las pruebas (`python -m unittest test_servers.py`).
- **Errores comunes**:
  - RabbitMQ no iniciado: "Connection refused" o "Unable to connect".
  - Servidor no activo: Clientes o pruebas no reciben respuestas.
  - Cola mal configurada: Asegúrate de que los nombres de las colas coincidan entre componentes.

---