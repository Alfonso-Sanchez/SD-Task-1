# Documentación: Práctica RabbitMQ Single Node

Esta documentación explica cómo configurar y ejecutar un proyecto basado en RabbitMQ con un único nodo que incluye un broadcaster de insultos (`broadcaster.py`), un cliente que envía y recibe frases filtradas (`client_filter.py`), un servidor que procesa insultos y frases (`server.py`), un cliente que solicita insultos (`insult_client.py`) y pruebas automatizadas (`test_rabbitmq_client.py`). El sistema usa un entorno virtual de Python y RabbitMQ como sistema de mensajería.

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
Contenido optimizado de `requirements.txt`:
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

El proyecto tiene cuatro componentes ejecutables: el servidor (`server.py`), el broadcaster (`broadcaster.py`), el cliente de filtrado (`client_filter.py`) y el cliente de insultos (`insult_client.py`). Sigue este orden para ejecutarlos.

### 2.1. Ejecutar el Servidor (`server.py`)
El servidor escucha insultos, filtra frases y responde solicitudes de insultos, mostrando estadísticas en una interfaz curses.

#### Paso 1: Iniciar el servidor
En una terminal (con el entorno activado y RabbitMQ corriendo), ejecuta:
```bash
python server.py
```
- Escucha las colas `insultos`, `filtrar` y `solicitudes_insulto`, y publica en `filtradas`.
- Muestra estadísticas como insultos únicos, frases filtradas y peticiones por segundo.
- Usa `Ctrl+C` para detenerlo (puede requerir cerrar la terminal si curses no responde).

### 2.2. Ejecutar el Broadcaster (`broadcaster.py`)
El broadcaster envía insultos aleatorios a la cola `insultos`.

#### Paso 1: Iniciar el broadcaster
En otra terminal (con el entorno activado y el servidor corriendo), ejecuta:
```bash
python broadcaster.py
```
- Envía un insulto cada 5 segundos (ej. "Tonto", "Gilipollas", "Maricon").
- Usa `Ctrl+C` para detenerlo.

### 2.3. Ejecutar el Cliente de Filtrado (`client_filter.py`)
El cliente envía frases a la cola `filtrar` y recibe las frases filtradas desde `filtradas`.

#### Paso 1: Iniciar el cliente de filtrado
En otra terminal (con el entorno activado y el servidor corriendo), ejecuta:
```bash
python client_filter.py
```
- Envía frases aleatorias (ej. "Edu es Tonto", "Eres un Gilipollas") y muestra las versiones filtradas.
- Usa `Ctrl+C` para detenerlo.

### 2.4. Ejecutar el Cliente de Insultos (`insult_client.py`)
El cliente solicita insultos al servidor y muestra estadísticas de respuestas por segundo.

#### Paso 1: Iniciar el cliente de insultos
En otra terminal (con el entorno activado y el servidor corriendo), ejecuta:
```bash
python insult_client.py
```
- Solicita insultos continuamente y muestra la tasa de respuestas por segundo.
- Usa `Ctrl+C` para detenerlo.

---

## 3. Ejecución de las Pruebas

El archivo de pruebas (`test_rabbitmq_client.py`) verifica el comportamiento del servidor con conexiones reales a RabbitMQ.

### Paso 1: Asegurarse de que el servidor esté corriendo
Ejecuta `server.py` como se describe en la sección 2.1.
Ejecuta `broadcaster.py` como se describe en la seccion 2.2.

### Paso 2: Ejecutar las pruebas
En una terminal (con el entorno activado y RabbitMQ corriendo), ejecuta:
```bash
python -m unittest test_rabbitmq_client.py
```
- Verifica:
  - Solicitar un insulto y recibir uno válido.
  - Filtrar una frase con insulto (censura correcta).
  - Filtrar una frase sin insulto (sin cambios).

### Notas adicionales
- Las pruebas pre-pueblan la cola `insultos` con datos de prueba.
- Si el servidor no está activo, las pruebas fallarán por falta de respuesta.

---

## Notas Finales
- **Requisitos**: Python 3.8 o superior, Docker para RabbitMQ.
- **Estructura sugerida**:
  - `broadcaster.py`: Envía insultos.
  - `client_filter.py`: Envía y recibe frases filtradas.
  - `server.py`: Procesa insultos, filtra frases y responde solicitudes.
  - `insult_client.py`: Solicita insultos y muestra estadísticas.
  - `test_rabbitmq_client.py`: Pruebas.
  - `requirements.txt`: Dependencias optimizadas.
- **Flujo típico**:
  1. Inicia RabbitMQ con Docker (`docker run ...`).
  2. Inicia el servidor (`python server.py`).
  3. Inicia el broadcaster (`python broadcaster.py`), el cliente de filtrado (`python client_filter.py`) y/o el cliente de insultos (`python insult_client.py`).
  4. Opcionalmente, ejecuta las pruebas (`python -m unittest test_rabbitmq_client.py`).
- **Errores comunes**:
  - RabbitMQ no iniciado: "Connection refused" o "Unable to connect".
  - Servidor no activo: Las pruebas o clientes no reciben respuestas.
