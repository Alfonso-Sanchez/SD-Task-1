# Documentación: Práctica PYRO4 2 NODES

Esta documentación explica cómo configurar y ejecutar un proyecto basado en Pyro4 con dos servidores de insultos (`InsultServer1` y `InsultServer2`), un cliente que envía insultos a ambos servidores (`Broadcaster`), un visualizador de estadísticas (`StatsDisplay`) y un conjunto de pruebas automatizadas (`TestInsultFilter`). El proyecto utiliza un entorno virtual de Python y requiere que el Name Server de Pyro4 esté activo.

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

### Paso 5: Desactivar el entorno (opcional)
Cuando termines, desactiva el entorno con:
```bash
deactivate
```

---

## 2. Ejecución del Código

El proyecto tiene cuatro componentes principales: dos servidores (`InsultServer1` y `InsultServer2`), el cliente (`Broadcaster`) y el visualizador de estadísticas (`StatsDisplay`). Sigue este orden para ejecutarlos.

### 2.1. Ejecutar los Servidores
Cada servidor gestiona insultos, censura palabras ofensivas y calcula métricas.

#### Servidor 1 (`InsultServer1`)
En una terminal (con el entorno activado y el Name Server corriendo), ejecuta:
```bash
python insult_server1.py
```
- `insult_server1.py` es el nombre sugerido para el primer servidor.
- Se registra como `example.insultserver1` en el Name Server.

#### Servidor 2 (`InsultServer2`)
En otra terminal (con el entorno activado), ejecuta:
```bash
python insult_server2.py
```
- `insult_server2.py` es el nombre sugerido para el segundo servidor.
- Se registra como `example.insultserver2` en el Name Server.

#### Notas
- Mantén ambas terminales abiertas mientras usas el cliente, el visualizador o las pruebas.

### 2.2. Ejecutar el Cliente (`Broadcaster`)
El cliente envía insultos aleatorios a uno de los servidores de forma continua.

#### Paso 1: Iniciar el cliente
En una nueva terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python broadcaster.py
```
- `broadcaster.py` es el nombre sugerido para el archivo del cliente.
- Verás mensajes como `Insulto '[texto]' enviado al servidor con resultado: [resultado]`.
- Usa `Ctrl+C` para detener el cliente y mostrar los insultos guardados en ambos servidores.

#### Notas
- El cliente elige aleatoriamente entre `example.insultserver1` y `example.insultserver2`.
- Si hay errores de conexión, verifica que el Name Server y los servidores estén activos.

### 2.3. Ejecutar el Visualizador de Estadísticas (`StatsDisplay`)
El visualizador muestra las métricas de ambos servidores en una interfaz curses.

#### Paso 1: Iniciar el visualizador
En otra terminal (con el entorno activado y los servidores corriendo), ejecuta:
```bash
python stats_display.py
```
- `stats_display.py` es el nombre sugerido para el archivo del visualizador.
- Verás estadísticas como insultos por segundo, cada 10 segundos y por minuto para ambos servidores.
- Presiona `q` para salir.

#### Notas
- Si un servidor no está disponible, se mostrará un mensaje de error en la interfaz.

---

## 3. Ejecución de las Pruebas

El archivo de pruebas (`TestInsultFilter`) verifica el comportamiento de ambos servidores. Requiere que ambos estén corriendo.

### Paso 1: Asegurarse de que los servidores estén activos
Ejecuta `insult_server1.py` y `insult_server2.py` como se describe en la sección 2.1.

### Paso 2: Ejecutar las pruebas
En una terminal (con el entorno activado), ejecuta:
```bash
python -m unittest test_insult_filter.py
```
- `test_insult_filter.py` es el nombre sugerido para el archivo de pruebas.
- Verás los resultados de las pruebas en la terminal (éxitos o fallos).

### Detalles de las pruebas
- **Pruebas para Server1 y Server2** (duplicadas para cada servidor):
  - Verifica que frases sin insultos se guarden correctamente.
  - Comprueba que los insultos se censuren como `CENSORED`.
  - Asegura que frases duplicadas no se guarden.
  - Confirma que múltiples frases se recuperen correctamente.

### Notas adicionales
- Las pruebas usan `clearSentences()` para limpiar los servidores antes de cada prueba. Asegúrate de que ambos servidores estén recién iniciados o que este método funcione.
- Si un servidor no está activo, las pruebas fallarán con un error de conexión.

---

## Notas Finales
- **Requisitos**: Python 3.8 o superior (compatible con Pyro4 4.82).
- **Estructura sugerida**:
  - `insult_server1.py`: Primer servidor.
  - `insult_server2.py`: Segundo servidor.
  - `broadcaster.py`: Cliente.
  - `stats_display.py`: Visualizador de estadísticas.
  - `test_insult_filter.py`: Pruebas.
  - `requirements.txt`: Dependencias.
- **Flujo típico**:
  1. Inicia el Name Server (`python -m Pyro4.naming`).
  2. Inicia ambos servidores (`python insult_server1.py` y `python insult_server2.py`).
  3. Inicia el cliente (`python broadcaster.py`), el visualizador (`python stats_display.py`) o las pruebas (`python -m unittest test_insult_filter.py`).
- **Errores comunes**:
  - Name Server no iniciado: "Cannot connect to Pyro name server".
  - Servidor no activo: "Connection refused".