# SD-Task-1: Escalado de Sistemas Distribuidos con Middlewares

Este repositorio contiene la resolución completa de la **Tarea 1** de la asignatura de **Sistemas Distribuidos**, cuyo objetivo es implementar versiones escalables de un sistema de insultos utilizando cuatro middlewares diferentes: **XML-RPC**, **Pyro4**, **Redis** y **RabbitMQ**.

La tarea incluye implementaciones para:

- **InsultService**: recibe insultos, los almacena si son únicos y permite recuperarlos.
- **InsultFilter**: reemplaza palabras ofensivas por "CENSORED".
- Broadcaster, Clientes, Visualizadores de Estadísticas y Pruebas.

## Estructura del Proyecto

```
SD-Task-1/
├── Pyro4/
├── XMLRPC/
├── Redis/
├── RabbitMQ/
├── Docs/
├── README.md
```

Cada carpeta representa una implementación del sistema con distinta tecnología middleware. Todas las versiones comparten una lógica común adaptada a las capacidades de cada sistema de comunicación.

---

## Tecnologías Empleadas

- **Lenguaje**: Python 3.8+
- **Middlewares**: Pyro4, XML-RPC, Redis, RabbitMQ
- **Visualización**: matplotlib, curses
- **Dependencias**: serpent, pika, redis, etc. (ver `requirements.txt` en cada subproyecto)

---

## Instrucciones por Tecnología

### 1. Pyro4 (Single Node / Multi Node / Dynamic Cluster)

- `insult_server.py`, `broadcaster.py`, `stats.py`, `test_insult_filter.py`
- Usa `Pyro4.naming` como Name Server
- Versiones:
  - **Single Node**: un servidor
  - **2 Nodos / 3 Nodos**: servidores separados y cliente que enví a peticiones de forma balanceada. 
  - **Cluster Dinámico**: escalado según carga usando `multiprocessing`

### 2. RabbitMQ

- Requiere Docker (`rabbitmq:3-management`)
- Versiones:
  - **Single Node**: un único servidor Rabbit
  - **Multi Node (2-3 nodos)**: servidores independientes con colas dedicadas
  - **Clientes**: `broadcaster.py`, `client_filter.py`, `insult_client.py`, `stats_monitor.py`

### 3. Redis

- Usa instancias en puertos `6379`, `6380`, `6381`
- Módulos: `server_redis_node*.py`, `client_redis.py`, `monitor.py`, `broadcaster.py`
- Cada nodo almacena insultos y realiza filtrado

### 4. XML-RPC

- Servidores en puertos `8001`, `8002`, `8003`
- Cliente: `xmlrpc_client.py`
- Monitor: `monitor.py`
- Pruebas: `test_server_xmlrpc_node*.py`, `test_client_xmlrpc.py`

---

## Ejecución General

1. **Crear entorno virtual** (una vez por tecnología):

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

2. **Ejecutar middleware (según versión)**:

- Pyro4: `python -m Pyro4.naming`
- RabbitMQ: `docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
- Redis: `redis-server --port 6379`, etc.

3. **Lanzar servidores y clientes**:

```bash
python insult_server.py
python broadcaster.py
python stats_display.py
```

4. **Ejecutar pruebas unitarias**:

```bash
python -m unittest *test.py
```

---

## Resultados y Experimentos

Se incluyen scripts de carga que permiten:

- Analizar rendimiento en **modo single node**
- Comparar tecnologías en **modo multi nodo estático (1, 2, 3 servidores)**
- Medir la eficiencia del **escalado dinámico (Pyro4)**
- Graficar resultados de rendimiento con `matplotlib`

---

## Documentación Incluida

- `/docs`/: enunciado de la tarea
- Cada middleware tiene sus guías .md. 

---

## Autores

**Eduard Vericat y Alfonso Sánchez**

---

> Proyecto para la asignatura de Sistemas Distribuidos — Curso 2024-2025.

Para dudas o mejoras, contactar al autor (alfonso.sanchez\@estudiants.urv.cat y eduard.vericat\@estudiants.urv.cat) o abrir un issue en el repositorio.

