# Documentación: Práctica PYRO4 Dynamic Cluster

Esta documentación detalla cómo configurar y ejecutar un proyecto basado en Pyro4 que implementa un clúster de servidores de insultos con escalado dinámico (`DynamicCluster`), un cliente que envía insultos (`Broadcaster`), un visualizador de estadísticas (`StatsDisplay`) y pruebas automatizadas (`TestInsultFilterScaling`). El sistema utiliza un entorno virtual de Python y el Name Server de Pyro4, con un archivo `servers.txt` para gestionar la lista de servidores activos.

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

### Paso 3: Instalar dependencias
Instala las dependencias listadas en `requirements.txt`:
```bash
pip install -r requirements.txt
```
Contenido de `requirements.txt`:
```
Pyro4==4.82
serpent==1.41
```

### Paso 4: Configurar el Name Server de Pyro4
Inicia el Name Server en una terminal separada (con el entorno activado):
```bash
python -m Pyro4.naming
```
Deja esta terminal abierta durante toda la ejecución del proyecto.

### Paso 5: Preparar el archivo `servers.txt`
El proyecto usa `servers.txt` para listar los servidores activos. Crea o verifica que exista este archivo en el directorio raíz con un servidor inicial:
```
example.insultserver1
```

### Paso 6: Desactivar el entorno (opcional)
Cuando termines, desactiva el entorno con:
```bash
deactivate
```

---

## 2. Ejecución del Código

El proyecto tiene tres componentes principales: el gestor de escalado dinámico (`DynamicCluster`), el cliente (`Broadcaster`) y el visualizador de estadísticas (`StatsDisplay`). Sigue este orden para ejecutarlos.

### 2.1. Ejecutar el Gestor de Escalado Dinámico (`DynamicCluster`)
El gestor inicia servidores y ajusta su número según la carga.

#### Paso 1: Iniciar el gestor
En una terminal (con el entorno activado y el Name Server corriendo), ejecuta:
```bash
python dynamic_cluster.py
```
- `dynamic_cluster.py` es el nombre sugerido para el archivo del gestor.
- Verás mensajes como `[Scaler] Servidor X iniciado` o `[Scaler] Servidor X detenido`.
- Usa `Ctrl+C` para detener el gestor y apagar todos los servidores.

#### Notas
- Inicia con `MIN_SERVERS=1` y escala hasta `MAX_SERVERS=5` según la carga (máximo 5 mensajes/segundo por servidor).
- Actualiza `servers.txt` automáticamente con los nombres de los servidores activos (ej. `example.insultserver1`, `example.insultserver2`, etc.).

### 2.2. Ejecutar el Cliente (`Broadcaster`)
El cliente envía insultos a los servidores activos listados en `servers.txt`.

#### Paso 1: Iniciar el cliente
En otra terminal (con el entorno activado y el gestor corriendo), ejecuta:
```bash
python broadcaster.py
```
- `broadcaster.py` es el nombre sugerido para el archivo del cliente.
- Verás mensajes como `[Cliente] Insulto '[texto]' enviado -> Resultado: [resultado]`.
- Usa `Ctrl+C` para detener el cliente y mostrar los insultos guardados en todos los servidores.

#### Notas
- Lee `servers.txt` periódicamente para actualizar la lista de servidores.
- Si no hay servidores disponibles, espera y reintenta cada 2 segundos.

### 2.3. Ejecutar el Visualizador de Estadísticas (`StatsDisplay`)
El visualizador muestra las métricas de todos los servidores activos.

#### Paso 1: Iniciar el visualizador
En otra terminal (con el entorno activado y el gestor corriendo), ejecuta:
```bash
python stats_display.py
```
- `stats_display.py` es el nombre sugerido para el archivo del visualizador.
- Muestra estadísticas (insultos por segundo, 10 segundos, minuto y tiempo de respuesta) para cada servidor y un total por segundo.
- Presiona `q` para salir.

#### Notas
- Lee `servers.txt` para determinar qué servidores monitorear.
- Si un servidor no responde, muestra un mensaje de error.

---

## 3. Ejecución de las Pruebas

El archivo de pruebas (`TestInsultFilterScaling`) verifica la funcionalidad básica y el escalado dinámico. Requiere que el gestor esté activo.

### Paso 1: Asegurarse de que el gestor esté corriendo
Ejecuta `dynamic_cluster.py` como se describe en la sección 2.1.

### Paso 2: Ejecutar las pruebas
En una terminal (con el entorno activado), ejecuta:
```bash
python -m unittest test_insult_filter_scaling.py
```
- `test_insult_filter_scaling.py` es el nombre sugerido para el archivo de pruebas.
- Verás los resultados de las pruebas en la terminal (éxitos o fallos).

### Detalles de las pruebas
- **Pruebas de servidor único**:
  - Verifica que frases sin insultos se guarden correctamente.
  - Comprueba que los insultos se censuren como `CENSORED`.
  - Asegura que frases duplicadas no se guarden.
- **Pruebas de escalado**:
  - `test_scale_to_max_servers`: Genera carga alta (400 solicitudes/segundo) y verifica que escale a 5 servidores.
  - `test_scale_down`: Escala a 5 servidores y luego elimina la carga, verificando que regrese a 1 servidor.

### Notas adicionales
- Las pruebas generan carga simulada y leen `servers.txt` para detectar servidores activos.
- Si `servers.txt` no existe o el gestor no está activo, las pruebas fallarán.

---

## Uso de `servers.txt` y Comparación con Alternativas

### Por qué usamos `servers.txt`
El proyecto utiliza un archivo `servers.txt` para mantener una lista dinámica de servidores activos. Este enfoque tiene las siguientes ventajas:
- **Simplicidad**: No requiere dependencias adicionales ni infraestructura externa (como Redis o un sistema de mensajería).
- **Compatibilidad con Pyro4**: Los nombres de los servidores (ej. `example.insultserver1`) se registran en el Name Server de Pyro4, y `servers.txt` actúa como un punto central para que el cliente y el visualizador los descubran sin necesidad de un protocolo complejo.
- **Escalado local**: Al ejecutarse en una sola máquina, un archivo local es suficiente para coordinar los procesos sin latencia de red.
- **Actualización dinámica**: El gestor actualiza `servers.txt` cada vez que inicia o detiene un servidor, permitiendo que los clientes y el visualizador se adapten en tiempo real.

### Comparación con alternativas como Pub/Sub con Redis
Otros métodos, como un sistema de publicación/suscripción (pub/sub) con Redis, podrían haberse considerado, pero no se usaron por las siguientes razones:
- **Complejidad adicional**: Redis requiere instalación, configuración y una dependencia extra en `requirements.txt` (ej. `redis-py`), lo que aumenta la complejidad del proyecto frente a un simple archivo de texto.
- **Sobrecarga innecesaria**: Pub/Sub es ideal para sistemas distribuidos en múltiples máquinas con alta concurrencia, pero este proyecto opera en un solo nodo, haciendo que Redis sea excesivo para la tarea.
- **Latencia y recursos**: Aunque Redis es rápido, introduce una capa adicional de comunicación que consume más recursos (memoria, CPU) en comparación con leer un archivo local.
- **Dependencia externa**: Usar Redis implica depender de un servicio externo o un proceso adicional, mientras que `servers.txt` es autónomo y no requiere configuración externa.
- **Escalabilidad limitada del diseño**: El proyecto está diseñado para un máximo de 5 servidores en un solo nodo, por lo que un sistema como pub/sub no aporta beneficios significativos frente a la simplicidad de un archivo.

En resumen, `servers.txt` es una solución práctica y eficiente para este caso de uso específico, evitando la sobrecarga de sistemas más complejos como pub/sub con Redis, que serían más adecuados para un entorno distribuido real con múltiples nodos.

---

## Notas Finales
- **Requisitos**: Python 3.8 o superior (compatible con Pyro4 4.82).
- **Estructura sugerida**:
  - `dynamic_cluster.py`: Gestor de escalado y servidores.
  - `broadcaster.py`: Cliente.
  - `stats_display.py`: Visualizador de estadísticas.
  - `test_insult_filter_scaling.py`: Pruebas.
  - `requirements.txt`: Dependencias.
  - `servers.txt`: Lista inicial de servidores.
- **Flujo típico**:
  1. Inicia el Name Server (`python -m Pyro4.naming`).
  2. Inicia el gestor (`python dynamic_cluster.py`).
  3. Inicia el cliente (`python broadcaster.py`) y/o el visualizador (`python stats_display.py`).
  4. Opcionalmente, ejecuta las pruebas (`python -m unittest test_insult_filter_scaling.py`).
- **Errores comunes**:
  - Name Server no iniciado: "Cannot connect to Pyro name server".
  - `servers.txt` no encontrado: "No hay servidores disponibles" o fallos en las pruebas.
  - Gestor no activo: Las pruebas fallarán si no hay servidores iniciales.